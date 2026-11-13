#!/usr/bin/env python3
"""SLL Commons: collect the latest items from each Nest's feeds.

Crawls nest.json files starting from this Commons (same rules as commons.html),
reads every feed a Nest lists, keeps the newest few items per Nest, and writes
feeds.json next to commons.html.

Only the standard library is used.
"""
import json
import os
import re
import sys
import urllib.request
import xml.etree.ElementTree as ET
from collections import deque
from datetime import datetime, timezone
from email.utils import parsedate_to_datetime

def own_url():
    """この箱自身の公開住所。名札の url ではなく、箱から決める（写された箱でも、自分から仕入れが始まる）。"""
    if os.environ.get("DYXIS_START"):
        return os.environ["DYXIS_START"]
    if os.path.exists("CNAME"):  # 独自ドメインの箱
        dom = open("CNAME", encoding="utf-8").read().strip()
        if dom:
            return f"https://{dom}/"
    repo = os.environ.get("GITHUB_REPOSITORY", "")
    if "/" in repo:
        owner, name = repo.split("/", 1)
        if name.lower() == f"{owner.lower()}.github.io":
            return f"https://{owner.lower()}.github.io/"
        return f"https://{owner.lower()}.github.io/{name}/"
    return "https://ittekiou.github.io/dyxis/"


START = own_url()
OUT = os.environ.get("DYXIS_OUT", "feeds.json")
PER_NEST = int(os.environ.get("DYXIS_PER_NEST", "3"))
MAX_NODES, MAX_DEPTH, TIMEOUT = 60, 1, 20   # 新着を仕入れるのは1段目（名札に書いた巣）まで
UA = "SLL-Commons-collector/0.3 (+https://ittekiou.github.io/dyxis/)"
ATOM = "{http://www.w3.org/2005/Atom}"


def now():
    return datetime.now(timezone.utc)


def norm(u):
    u = (u or "").split("#")[0].split("?")[0]
    return u if u.endswith("/") else u + "/"


def get(url, headers=None):
    req = urllib.request.Request(url, headers={"User-Agent": UA, **(headers or {})})
    with urllib.request.urlopen(req, timeout=TIMEOUT) as r:
        return r.read()


def parse_date(s):
    if not s:
        return None
    s = s.strip()
    try:
        d = parsedate_to_datetime(s)
    except (TypeError, ValueError):
        try:
            d = datetime.fromisoformat(s.replace("Z", "+00:00"))
        except ValueError:
            return None
    if d.tzinfo is None:
        d = d.replace(tzinfo=timezone.utc)
    return d


TITLE_LEN = 30  # 題のない便り（Bluesky など）は、本文の頭をこの字数だけ題にする


def title_or_text(title, *texts):
    """題があれば題。なければ本文（タグとURLを外して）の頭を題にする。"""
    title = (title or "").strip()
    if title:
        return title
    for t in texts:
        t = re.sub(r"<[^>]+>", " ", t or "")
        t = re.sub(r"https?://\S+", " ", t)  # 本文のURLは題に入れない
        t = re.sub(r"\s+", " ", t).strip()
        if t:
            return t if len(t) <= TITLE_LEN else t[:TITLE_LEN] + "…"
    return ""


def parse_feed(raw):
    root = ET.fromstring(raw)
    items = []
    if root.tag == ATOM + "feed":
        for e in root.findall(ATOM + "entry"):
            link = ""
            for l in e.findall(ATOM + "link"):
                if l.get("rel", "alternate") == "alternate":
                    link = l.get("href", "")
                    break
            items.append({
                "title": title_or_text(e.findtext(ATOM + "title"), e.findtext(ATOM + "summary"), e.findtext(ATOM + "content")),
                "link": link,
                "published": parse_date(e.findtext(ATOM + "published") or e.findtext(ATOM + "updated")),
            })
    else:
        for it in root.iter("item"):
            items.append({
                "title": title_or_text(it.findtext("title"), it.findtext("description")),
                "link": (it.findtext("link") or "").strip(),
                "published": parse_date(it.findtext("pubDate") or it.findtext("{http://purl.org/dc/elements/1.1/}date")),
            })
    return items


# GitHub の書き込み（コミット）のリンクを、読める公開ページへ付け替える。
# 例：kyoei/diary/2026-11-06.md を足した書き込み → https://ittekiou.github.io/EAT-IF/kyoei/diary/2026-11-06.html
COMMIT = re.compile(r"^https://github\.com/([^/]+)/([^/]+)/commit/([0-9a-f]{7,40})$", re.I)
TOKEN = os.environ.get("GITHUB_TOKEN", "")


def readable_link(link, nest_url):
    m = COMMIT.match(link or "")
    if not m:
        return link
    owner, repo, sha = m.groups()
    base = f"https://{owner.lower()}.github.io/{repo}/"
    if not nest_url.lower().startswith(base.lower()):
        return link  # この巣が、そのリポジトリの公開ページでなければ、そのまま
    base = nest_url[:len(base)]
    try:
        h = {"Accept": "application/vnd.github+json", **({"Authorization": f"Bearer {TOKEN}"} if TOKEN else {})}
        files = json.loads(get(f"https://api.github.com/repos/{owner}/{repo}/commits/{sha}", h)).get("files") or []
    except Exception:  # noqa: BLE001
        return link
    md = [f for f in files if f.get("filename", "").lower().endswith(".md") and f.get("status") != "removed"]
    pick = ([f for f in md if f["status"] == "added" and not f["filename"].lower().endswith("readme.md")]
            or [f for f in md if not f["filename"].lower().endswith("readme.md")]
            or md)
    if not pick:
        return nest_url  # 日記などの文章が変わっていなければ、巣の入口へ
    path = pick[0]["filename"]
    if path.lower().endswith("readme.md"):
        return base + path[: -len("readme.md")]
    return base + path[:-3] + ".html"


def crawl():
    nests, queue = {}, deque([(norm(START), 0)])
    while queue and len(nests) < MAX_NODES:
        url, depth = queue.popleft()
        if url in nests:
            continue
        try:
            data = json.loads(get(url + "nest.json"))
        except Exception as e:  # noqa: BLE001
            nests[url] = {"error": f"nest.json: {e}"}
            continue
        nests[url] = {"data": data}
        if depth < MAX_DEPTH:
            for n in data.get("nests") or []:
                if n and n.get("url") and norm(n["url"]) not in nests:
                    queue.append((norm(n["url"]), depth + 1))
    return nests


def main():
    started = now()
    out = {"sll": "0.1", "commons": norm(START), "collected_at": started.isoformat(timespec="seconds"), "nests": {}}
    for url, info in crawl().items():
        data = info.get("data")
        if not data or not data.get("feeds"):
            continue
        items, errors = [], []
        for f in data["feeds"]:
            furl = (f or {}).get("url")
            if not furl:
                continue
            try:
                fetched = now()
                for it in parse_feed(get(furl)):
                    it["feed"] = f.get("title") or furl
                    it["fetched"] = fetched
                    items.append(it)
            except Exception as e:  # noqa: BLE001
                errors.append(f"{furl}: {e}")
        epoch = datetime.min.replace(tzinfo=timezone.utc)
        items.sort(key=lambda x: x["published"] or epoch, reverse=True)
        out["nests"][url] = {
            "name": data.get("name", url),
            "items": [{
                "title": it["title"], "link": readable_link(it["link"], url), "feed": it["feed"],
                "published": it["published"].isoformat(timespec="seconds") if it["published"] else None,
                "fetched": it["fetched"].isoformat(timespec="seconds"),
            } for it in items[:PER_NEST]],
            **({"errors": errors} if errors else {}),
        }
    with open(OUT, "w", encoding="utf-8") as fh:
        json.dump(out, fh, ensure_ascii=False, indent=2)
        fh.write("\n")
    print(f"{len(out['nests'])} nests with feeds -> {OUT}")


if __name__ == "__main__":
    sys.exit(main())
