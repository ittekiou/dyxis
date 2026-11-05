#!/usr/bin/env python3
"""DyXis Commons: collect the latest items from each Nest's feeds.

Crawls nest.json files starting from this Commons (same rules as commons.html),
reads every feed a Nest lists, keeps the newest few items per Nest, and writes
feeds.json next to commons.html.

Only the standard library is used.
"""
import json
import os
import sys
import urllib.request
import xml.etree.ElementTree as ET
from collections import deque
from datetime import datetime, timezone
from email.utils import parsedate_to_datetime

START = os.environ.get("DYXIS_START", "https://ittekiou.github.io/dyxis/")
OUT = os.environ.get("DYXIS_OUT", "feeds.json")
PER_NEST = int(os.environ.get("DYXIS_PER_NEST", "3"))
MAX_NODES, MAX_DEPTH, TIMEOUT = 60, 4, 20
UA = "DyXis-Commons-collector/0.1 (+https://ittekiou.github.io/dyxis/)"
ATOM = "{http://www.w3.org/2005/Atom}"


def now():
    return datetime.now(timezone.utc)


def norm(u):
    u = (u or "").split("#")[0].split("?")[0]
    return u if u.endswith("/") else u + "/"


def get(url):
    req = urllib.request.Request(url, headers={"User-Agent": UA})
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
                "title": (e.findtext(ATOM + "title") or "").strip(),
                "link": link,
                "published": parse_date(e.findtext(ATOM + "published") or e.findtext(ATOM + "updated")),
            })
    else:
        for it in root.iter("item"):
            items.append({
                "title": (it.findtext("title") or "").strip(),
                "link": (it.findtext("link") or "").strip(),
                "published": parse_date(it.findtext("pubDate") or it.findtext("{http://purl.org/dc/elements/1.1/}date")),
            })
    return items


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
                "title": it["title"], "link": it["link"], "feed": it["feed"],
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
