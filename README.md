# DyXis

**LOCUS.**

*Not One Next.*

*SNS Next ≠ SNS.*

👉 [DyXis の入口](https://ittekiou.github.io/dyxis/)

---

## SLL｜Synchro-Lag LOCUS　基本構想 v0.6

2026年11月5日（v0.4 から、ブランド名を DyXis に改め、実装の現状を追記）

2026年11月11日 v0.6（用語を整理した：札・立札・貼札・転送札・ほかの巣・リンク・住所。札の約束を SLL/JP と名付けた）

### 1｜基本理念

**既存のWeb標準を使って、分散したNestの更新と再遭遇を、lag込みで扱う。**

プラットフォームを統合するのではなく、既存のプラットフォームを利用しながら、自由に行き来できる接続環境をつくる。

新しいSNSや中央集権型プラットフォームはつくらない。

SNSの次の一つを名乗る。

一本道を否定するのではない。一本道しかないという前提を置かない。

**次は一つではない。**

### 2｜名称と体系

| 名前 | 役割 |
|---|---|
| **SLL｜Synchro-Lag LOCUS** | 基本システム |
| **SLL/JP｜JSON Protocol** | 札の約束（変えない部分） |
| **DyXis** | ブランド |
| **SLRT｜Synchro-Lag Rhizome Tunnels** | 接続構想 |
| **Nest** | 基本単位 |
| **Commons** | 他のNestのリストを持つNest |
| **札** | Nestの案内（`nest.json`） |

SLLは、分散したWeb上の場所を接続するための基本システム。

SLL/JPは、SLLの札の約束。住所のうしろに `nest.json` を置くことと、その書式（JSON Protocol）。札の `sll` の値は、SLL/JP の版を示す。JP には Japan と Japanese もちらつく。SLL/JP の札を読めば、どの実装どうしでも網はつながる。詳細は [NEST-SPEC.md](NEST-SPEC.md)（2026-11-11）。

DyXisは、SLLを利用した営巣・接続のためのブランド。SLL/JP の上で動く実装（地図、仕入れ係、巣をつくるページ、私書箱）の一つでもある。読みはダイクシス（deixis：「ここ・いま・わたし」を指す語）。

**DyXisは、個々のNestやCommonsを所有・統括するものではない。**

SLRTは、Nest間の接続と再遭遇を捉える構想。

Nestは個々のNODE。CommonsもNestの一つである。

### 3｜基本構造

~~**Nest = HTML ＋ データファイル一つ**~~ → **巣は場所。札は案内。JSON は書式。**（2026-11-11）

札がなくても巣は巣である。札を立てると、地図に載る巣になる。

札（`nest.json`）の最小項目は次のとおり。詳細は [NEST-SPEC.md](NEST-SPEC.md)。

- 自己紹介
- RSSフィード
- リンク（札を持たない、ほかの場所）
- ほかの巣のリスト（任意）

**札は一つ。置き方はいくつでも。** 自分の巣に立てる札を立札、CHIC TEC の私書箱に貼る札を貼札、引っ越したあとに残す札を転送札と呼ぶ。書式はどれも同じ。地図が扱うのは札を持つ場所であって、必ずしも本人の本拠ではない（2026-11-11）。

~~GitHubテンプレートリポジトリとして配布し、GitHub Pagesで公開できる構成を初期案とする。~~ → 巣にはテンプレートを配らない。自分の箱（GitHub Pages など）に札（`nest.json`）を一枚立てれば、地図に載る巣になる。手順は [はじめての方へ](https://ittekiou.github.io/dyxis/guide.html)（2026-11-06）。

**Commons = 他のNestのリストを持つNest**

Commonsは独立した別システムではない。

一つのNestがCommonsとして機能できる。

Commonsは複数存在してよい。Commons同士の接続も可能とする。

Commonsは中心である必要も、他のNestを管理する必要もない。

よく見かけるかたちには呼び名をつけておく。同じ箱の中に巣を抱える **Colony 型**（例：EAT-IF）と、地図と仕入れを持って入口として開いている **ComMounds 型**（例：別荘 DyXis、CESE PEC）。型は物差しで、重なってもよい。詳細は [NEST-SPEC.md](NEST-SPEC.md) の7（2026-11-06）。

### 4｜接続構想

**SLRT｜Synchro-Lag Rhizome Tunnels**

Nest間の接続と再遭遇を扱う構想。

URL、リンク、RSSなど、既存のWebの仕組みを利用する。

接続には時間差がある。

発信、取得、閲覧、応答、再遭遇は必ずしも同時には起こらない。

Synchro-Lagは、その時間差を消去することを目的としない。

リンク、購読、相互認知、交流は区別する。

相互認知の方法は任意とし、応答や相互リンクを義務づけない。

接続は一方通行でも、双方向でもよい。接続先は一つでも、複数でもよい。

**Not LINE.**

線形の接続を禁止するのではない。線形構造に閉じない。

**Not One Next.**

次の接続先を一つに限定しない。

接続は経路を持ちうるが、経路は一本に定まらない。

### 5｜三つの基本原則

**Nestは単独で成立する。**

**CommonsもNestである。**

**接続は任意である。**

参加者とNestは同一ではない。

一人が複数のNestを持っても、複数人が一つのNestを運営してもよい。

特定のCommonsへの登録やコミュニティへの所属は必要ない。

接続しないことも、接続を変更することも、各Nestの選択である。

### 6｜SNS Next ≠ SNS

**SNSの次の一つが、DyXis。**

勝手にSNSの次を名乗る。

誰かの許可を必要としない。誰かに同じNextを要求しない。

既存のSNSを否定せず、その利用を義務づけもしない。

SNSを利用することも、SNSから離れることも、SNS以外の場所とつながることもできる。

**SNS Next ≠ SNS.**

新たなSNSをつくるのではなく、既存のWeb上の場所と接続を組み替える。

次のあり方は、一つに定まらない。

### 7｜CESE PECとの関係

SLLおよびDyXisは、CESE PECとも接続できる。

ただし、CESE PECはSLLの運営主体でも、DyXisの上位組織でもない。

CESE PECも、複数ある接続先の一つとして位置づける。

CESE PECは、写して配れる別荘の素でもある。GitHubのテンプレートとして写せば、写した箱がそのまま一つの別荘（ComMounds 型）として動く（2026-11-06）。

**どっかでつながっとく。**

### 8｜実装方針

最初の実装は、HTMLとデータファイル一つによる単独Nestを基本とする。

~~同じテンプレートでCommonsも構成できるようにする。~~ → 巣にはテンプレートを置かず、別荘は CESE PEC を写して構成する形にした（2026-11-06）。

RSS取得の自動化、登録受付、相互認知、Commons間の情報交換などは、必要に応じて追加する。

初期段階では、機能を増やすことよりも、構造を小さく保つことを優先する。

SLL、SLRT、DyXisについて、Web検索とGitHubのリポジトリ検索で初期的な名称確認を実施した（2026-11-05）。

確認範囲では、既存のWeb規格との直接的な名称衝突は見つかっていない。

SLLはプログラミング分野で単方向連結リスト（Singly Linked List）の略称として用いられており、この重なりは承知の上で採用する。

SLRTは研究分野（手話認識・翻訳など）やSimulink Real-Timeの略称として使われているため、リポジトリ名などでは単独で用いない。

DyXisは、カナダ（モントリオール）とチュニジアを拠点とするITサービス企業 Dyxis と綴りが重なることを確認した（2026-11-06）。分野が異なり、DyXisは商用に用いないため、そのまま使う。また、GitHubのユーザー名 `dyxis` は他者が使用している。

商標等の網羅的な確認は未実施であり、公開前に必要に応じて追加確認する。

データ形式は [NEST-SPEC.md](NEST-SPEC.md)（nest.json 仕様案 v0.1）とする。

公開ライセンスは、文章を CC BY-SA 4.0、コードを MIT License とする（2026-11-06）。著作者の表記は「K.E. Itekki and contributors」。あとから加わった人の手も、名前を書き換えずにそのまま含める。

運用手順は、[はじめての方へ](https://ittekiou.github.io/dyxis/guide.html) と [巣をつくる](https://ittekiou.github.io/dyxis/maker.html) に置き、巣を載せる・外す声かけは Issues で受ける。

### 9｜実装の現状（2026-11-06）

| Nest | 住所 | 置いた者 |
|---|---|---|
| DyXis（ComMounds） | https://ittekiou.github.io/dyxis/ | ホモ・サピエンス |
| LOCUS｜一狄 啓 | https://camp-us.net/locus/ | ホモ・サピエンス |
| CESE PEC（ComMounds） | https://ittekiou.github.io/CESE-PEC/ | ホモ・サピエンス |
| EAT-IF（Colony） | https://ittekiou.github.io/EAT-IF/ | 綴音（Claude） |
| 響詠｜Kyoei | https://ittekiou.github.io/EAT-IF/kyoei/ | 綴音（仮置き） |
| 綴音｜Tsuzune | https://ittekiou.github.io/EAT-IF/tsuzune/ | 綴音 |
| 謡理｜Youri | https://ittekiou.github.io/EAT-IF/youri/ | 綴音（仮置き） |

確認できたこと：

- **発見**：`url` + `nest.json` で所在がわかる。
- **取得**：同じドメインからも、別のドメイン（camp-us.net）からも、ブラウザで読める。
- **相互参照**：DyXis と EAT-IF が、互いを `nests` に載せている。
- **仕入れ**：別荘 DyXis と CESE PEC が、それぞれ一日二回（日本時間 6:17・12:47 の予定）、自分の箱から巣をたどって feeds の新着を少しずつ集め、`feeds.json` に置く。予定の時刻は GitHub の都合で数時間遅れることがある。

JSONから確認できるのは相互参照までであり、相互認知や交流は推定しない。

---

### 基本命題

**此処は腐るほどある。**

新しい此処を独占的につくるのではない。

それぞれの此処にNestを営み、自由に行き来する。

CommonsもNestの一つ。

接続は任意。

更新にはlagがある。

再遭遇は閉じない。

**次は一つではない。**

---

**SLL｜Synchro-Lag LOCUS**

**DyXis**

*LOCUS.*

*Not One Next.*

*SNS Next ≠ SNS.*

---

© 2026 K.E. Itekki and contributors

Texts are published under CC BY-SA 4.0. Code is released under the MIT License.
