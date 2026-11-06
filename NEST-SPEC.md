# nest.json 仕様案 v0.1

2026年11月5日｜DyXis（SLL｜Synchro-Lag LOCUS）👉 [DyXis の入口](https://ittekiou.github.io/dyxis/)

## 1｜唯一の約束

**`url` は必ず `/` で終える。データファイルは `url` + `nest.json` に置く。**

例：`https://ittekiou.github.io/dyxis/` → `https://ittekiou.github.io/dyxis/nest.json`

名前と置き場所を固定しておけば、URLさえわかれば誰でもそのNestのファイルを見つけられる。中央の登録台帳も、共通サーバーもいらない。

## 2｜形式

JSON。静的なページでも、JavaScriptでそのまま読める。他のRSSリーダーと行き来したくなったら、あとでOPMLに書き出す。

## 3｜項目

| 項目 | 必須 | 中身 |
|---|---|---|
| sll | ○ | この形式の版（今は `"0.1"`） |
| name | ○ | Nestの名前 |
| url | ○ | Nestの番地（`/` で終える） |
| about | ○ | 自己紹介 |
| lang | | 言語 |
| updated | | 最終更新日（人が書く） |
| feeds | | RSSのリスト（`title` と `url`） |
| links | | 外部リンクのリスト（`title` と `url`） |
| nests | | 他のNestのリスト（`name` と `url`）。これがあればCommonsとして振る舞える |

## 4｜例

```json
{
  "sll": "0.1",
  "name": "DyXis",
  "url": "https://ittekiou.github.io/dyxis/",
  "about": "LOCUS. Not One Next. SNS Next ≠ SNS.",
  "lang": "ja",
  "updated": "2026-11-05",
  "feeds": [],
  "links": [
    { "title": "camp-us.net", "url": "https://camp-us.net/" }
  ],
  "nests": [
    { "name": "EAT-IF", "url": "https://ittekiou.github.io/EAT-IF/" }
  ]
}
```

## 5｜読み方の限定

- **相互参照と相互認知は区別する。** AのnestsにB、BのnestsにAがあれば、確認できるのは相互参照まで。両者が相手を認めたのか、単にリンクを置いたのかは、JSONだけでは判定できない。
- **updated は自己申告の日付。** 取得時刻との差は計算できるが、それは「記載された更新日から取得時点までの経過時間」であって、実際の更新遅延とは限らない。
- **発見できることと、取得できることは別。** 前者はURLの約束が支え、後者は配信の条件（CORSなど）が左右する。GitHub Pages では別ドメインからの取得ができることを確認した（2026-11-05、camp-us.net から）。GitHub Pages 以外に置く場合は、配信側でCORSを許可すること。

## 6｜運用のヒント

- **発信先が多い人は、先にRSSを一本に束ねる。** note、Substack、ポッドキャスト、ブログなどの新着を自分の側で一本のRSSにまとめ（例：LiRax の `https://camp-us.net/rack/feed.xml`）、`feeds` にはその一本だけを書く。発信先が増えても、束ねる側に足すだけで、nest.json は触らなくてよい。番地を隠したいフィードも、束ねる側で読めば表に出ない。
- **束ねたRSSを読むと、時間差が一段増える。** 別荘が読むのは元の記事ではなく、束ねる側が集め直した写しになる。公開から束ねるまでの遅れに、別荘が取りに行くまでの遅れが重なる。
- **巣の玄関と新着の置き場は、別でよい。** 例：玄関は `camp-us.net/locus/`、新着は母屋（LiRax）の feed.xml。

## 7｜未決

- Commonsの名乗り方（「リストを持つ」と「入口として開いている」を区別する項目を足すか）
- 登録の受け付け方
- 運営者の名前の扱い（参加者とNestを分ける原則があるので、必須にはしない）
- 公開ライセンス
