# 講義ノートの参考文献再確認

**対応状況（2026年9月9日）**：ユーザーの修正依頼に基づき、指摘と補足提案を各回・シラバスへ反映した。[修正内容・生成物・検証結果](reviews/2026-09-09/reference-revision/IMPLEMENTATION.md)。以下は修正前の監査記録として保存している。

2026年9月9日。対象：第1〜12回、関連する解答・共通表、現行シラバスの参考文献。開始時の HEAD は `266fc15053da463712ffea642b6aea7f400e3db6`。講義原稿・解答・配布用HTML/PDFは変更していない。

**現在の講義範囲に対する文献の選択は概ね妥当。ただし、第11・12回の訂正文献への案内、第1回の教科書著者表記、第2回のHPフィルター原典は、修正・補足を勧める。** 内容の異なる論文へ飛ぶDOIは、掲載30種類の照合では見つからなかった。

## 優先して直す3点

### 1. 第11・12回：Bilbiie (2008) の2019年訂正を併記する

対象：[第11回780行](/Users/kenjimyzk/work/gradmacro2026/lecture11.qmd:780)、[第12回1014行](/Users/kenjimyzk/work/gradmacro2026/lecture12.qmd:1014)。

Sciteで、基本文献 Bilbiie (2008) に2019年の Corrigendum があることを検出し、出版社の訂正文を確認した。訂正は、原論文 §4.3 の利益再分配における労働供給の仮定と、Proposition 4 / Appendix C の二次厚生近似に関係する。第12回で配当再分配を学んだ学生が原論文を読む際に直接関わるため、2008年論文だけを案内するのは不十分である。[出版社の訂正本文](https://www.sciencedirect.com/science/article/abs/pii/S002205311930033X)。

追加すべき書誌：

> Bilbiie, Florin O. (2019). Corrigendum to “Limited asset markets participation, monetary policy and (inverted) aggregate demand logic” [J. Econ. Theory 140 (1) (2008) 162–196]. *Journal of Economic Theory*, **181**, 421–422. [DOI: 10.1016/j.jet.2019.03.008](https://doi.org/10.1016/j.jet.2019.03.008).

2008年の項目に「再分配の仮定と厚生近似については2019年の訂正を併読」と付記すれば、読むべき範囲が明確になる。

**現行講義の式が誤っているという指摘ではない。** 第12回の所得係数 \(\chi\)、Type Sの所得係数、PE曲線・乗数は、Bilbiie (2020) 刊行版 pp.97–98、式(8)–(13)と整合する。原論文の条件と講義での簡略化を区別した結果は、[第11・12回の詳細](reviews/2026-09-09/reference-audit/l11-l12.md)に記録した。[2020年刊行版](https://www.liuyanecon.com/wp-content/uploads/Bilbiie-2020.pdf)。

### 2. 第1回：Blanchard の第7版と Johnson の共著表記をそろえる

対象：`lecture01.qmd:554`。

現在は「Blanchard, Olivier, and David R. Johnson (2017), *Macroeconomics*, 7th ed.」。Pearsonの第7版・©2017の登録は **Olivier Blanchard単著**である。この版を参照するなら Johnson を削除する。2017年は著作権年として成立するため、年だけを2013年等に変更する修正は適切でない。[Pearson公式・第7版](https://www.pearson.com/en-us/subject-catalog/p/Blanchard-Macroeconomics-Student-Value-Edition-7th-Edition/P200000007659/9780133792935)。

修正案：

> Blanchard, Olivier (2017). *Macroeconomics* (7th ed.). Pearson.

Johnsonとの共著版を実際に使う場合は、その版・年・ISBNへ書誌全体を合わせる。ここでは現在記載されている第7版を基準に評価した。

### 3. 第2回：HPフィルターの方法の出典を加える

対象：`lecture02.qmd:45`、`49`、`57`、参考文献 `594–612`。

図と本文でHPフィルター、四半期データの \(\lambda=1600\)、データとモデル系列への同じ処理を説明しているが、参考文献にはHodrick–Prescottの原典がない。BEA/FREDの出典はデータを追跡するために適切だが、フィルターの方法を調べる参照先も必要である。

追加案：

> Hodrick, Robert J., and Edward C. Prescott (1997). “Postwar U.S. Business Cycles: An Empirical Investigation.” *Journal of Money, Credit and Banking*, **29**(1), 1–16. [DOI: 10.2307/2953682](https://doi.org/10.2307/2953682).

書誌はConsensus検索・fetchと著者公開資料で照合した。[著者所属機関の登録](https://asu.elsevierpure.com/en/publications/postwar-us-business-cycles-an-empirical-investigation/)。現行本文はHP循環成分を理論的産出ギャップと区別し、HP適用だけでは弱定常性を保証しないとも明記しているので、その説明を撤回する必要はない。

## 内容と出典の対応を改善する補足

以下は、既存の参考文献を誤りとする指摘ではない。原典から講義の説明へたどりやすくするための、少数の補足候補である。

| 箇所 | 補足候補 | 講義との関係 |
|---|---|---|
| 第4回477行 | King and Rebelo (1999) に編集者Taylor・Woodford、第14章、927–1007頁、[DOI](https://doi.org/10.1016/S1574-0048(99)10022-3)を追記 | 既存の題名・著者・年は正しいが、ハンドブック章の所在をより明確にできる |
| 第7回119行・第9回221–224行 | Lombardo and Vestin (2008), “Welfare implications of Calvo vs. Rotemberg-pricing assumptions,” *Economics Letters*, 100(2), 275–279. [DOI](https://doi.org/10.1016/j.econlet.2008.02.008) | Calvo・Rotembergの厚生比較を直接扱う。現行本文の「効率的なゼロインフレ定常状態の周り」という限定に対応する。[出版社](https://www.sciencedirect.com/science/article/abs/pii/S0165176508000396) |
| 第9回227行以降「神々の配剤」 | Blanchard and Galí (2007), “Real Wage Rigidities and the New Keynesian Model,” *Journal of Money, Credit and Banking*, 39(s1), 35–65. [DOI](https://doi.org/10.1111/j.1538-4616.2007.00015.x) | 用語と、その成立・不成立条件を調べる原典として有用。現在のGalí教科書やCGGによる案内も妥当 |
| 第10回1077–1078行 | EHL (2000) はCalvo型の賃金・価格硬直性と政策トレードオフ、Rotemberg (1982) は価格調整費用の原典、と役割を付記 | 講義独自のRotemberg型賃金費用までEHLがそのまま導出していると読ませない。現行の文献自体を差し替える必要はない |
| 第12回1013行 | Bilbiie (2020), §§2–3、Propositions 1–2を参照範囲として付記 | RANK/TANKのPE曲線に集中して読める。所得リスクを含む後半まで全員に課す必要はない |
| 第12回986行 | 第2回のBlanchard–Kahn (1980)への相互参照。QZ法を自習対象にする場合だけ、その解法文献を補足 | 現状は発展案内なので、一般DSGE解法を授業の必須範囲へ増やす必要はない |

第5回のDOIがない論文にも識別子・著者公開リンクを補えるが、リンクの欠落だけを誤引用とは判定していない。賃金のCalvo–Rotemberg比較を詳しく扱う場合には Born and Pfeifer (2020) が候補になるが、同論文にも2025年の訂正がある。追加する場合は両方を示す。今回は発展先としての提案にとどめ、詳細は[第5〜10回の記録](reviews/2026-09-09/reference-audit/l05-l10.md)を参照。

## 誤りと判定しなかった相違

- **Campbell and Mankiw (1989) の185–246頁**：第11・12回はNBERの章単位の表記に対応する。論文本体の出版社DOI登録は185–216頁で、216頁以降には他著者のコメント・討論がある。現行表記を架空のページ範囲とみなすのは誤り。DOI側へ統一するなら185–216にし、章全体を案内するなら「討論を含む」と補足すると明瞭。[出版社目次](https://www.journals.uchicago.edu/toc/ma/1989/4)、[NBER章PDFの表紙書誌](https://www.nber.org/system/files/chapters/c10965/c10965.pdf)。
- **Rotemberg and Woodford (1997) の297–346頁**：第6回の記載は論文本体として正しい。NBERの297–361頁はコメント等を含む範囲であり、それを根拠に346を361へ変える必要はない。[出版社目次](https://www.journals.uchicago.edu/toc/ma/1997/12)。
- **Bilbiie (2020) の年とDOI中の2019**：刊行巻114は2020年、オンライン公開は2019年。2020年表記でよい。[刊行版表紙](https://www.liuyanecon.com/wp-content/uploads/Bilbiie-2020.pdf)。
- **第4回のRBC文献**：現在の講義は固定資本で、資本蓄積を含むRBC文献を発展・比較用として掲げている。その範囲が明示されているため、RBC原典が講義の簡略モデルと同一でないことは誤引用ではない。
- **第11・12回のHANK文献**：Kaplan–Moll–Violante、Auclert、McKay–Nakamura–Steinsson、Werningは発展・比較先として適切。講義のTANKが各論文の全ての所得リスク・資産再分配経路を実装するという主張にはなっていない。
- **古い基本文献**：原典や指定版が現在の論点に合っていれば、刊行が古いだけでは不備ではない。最新論文への一括置換は不要。

## シラバスとの対応

現行シラバスは講義ノートを主教材、文献を論点別の復習先として位置づけており、原論文の全モデルを授業範囲とはしていない。これは現在の講義内容と整合する。

二神・堀の『マクロ経済学 第3版 基礎編』は2025年12月、二神・堀・祝迫の『応用編』は2026年8月刊で、現在の著者・年の記載に不備は確認できない。応用編は第7章がNK理論、第9章が家計異質性、第12・13章が離散時間最適化・動的計画法であり、復習範囲を示す候補になる。ただし今回確認したのは出版社の目次・書誌で、書籍全文ではない。[有斐閣・基礎編](https://www.yuhikaku.co.jp/genres/search/3303)、[有斐閣・応用編](https://www.yuhikaku.co.jp/book/b10190488.html)。

Walshの第4版・2017年も出版社で確認した。[MIT Press](https://mitpress.mit.edu/9780262035811/monetary-theory-and-policy/)。他の基本書の確認状況は[第1〜4回の記録](reviews/2026-09-09/reference-audit/l01-l04.md)と第5〜10回の記録に分けて示す。

## 実施した確認と限界

| 検証 | 結果 |
|---|---|
| 文献一覧の抽出 | **verified**：講義12回の掲載87項目、シラバス7項目を抽出。同一文献の重複を除くと57件（データ出典を含む）。[一覧](reviews/2026-09-09/reference-audit/inventory.json) |
| 掲載DOIの同定 | **verified**：30種類をSciteのDOI指定検索で全件取得。題名・著者・年・掲載先を比較し、別論文へのDOIを検出しなかった。[取得メタデータ](reviews/2026-09-09/reference-audit/scite-doi-metadata.json) |
| DOIメタデータの精度 | Sciteには終頁がない記録やCampbellの著者欠落がある。全項目の全フィールドが完全であるという意味の検証ではない。疑わしい箇所は出版社・原典へ戻して判定した |
| 訂正情報 | SciteでBilbiie (2008) の訂正通知を検出し、2019年の書誌と訂正対象を一次資料で確認。全書籍・全論文の訂正履歴を独立に網羅した監査ではない |
| 出典と講義内容 | **verified（主要論点）**：各回を分担して現行本文と引用の役割を照合。特にTANK再分配・NKクロスと名目硬直性の比較を重点確認。全参考文献の全文精読ではない |
| 保存HTMLとの対応 | **verified**：講義12回・87項目の参考文献本文と全記載URLをQMDと照合。引用符・ダッシュ等の表示上の正規化を除き不一致0、URL欠落0。[静的照合](reviews/2026-09-09/reference-audit/html-reference-check.json) |
| 原稿・配布物の保全 | レビュー資料だけを追加。開始前後のSHA-256とGit差分を確認。[保全結果](reviews/2026-09-09/reference-audit/preservation.json) |
| 再レンダー・PDF目視・ブラウザ実行・計算再実行 | **not run**：今回の参考文献監査では実施していない |

Consensusは論文発見とレコード確認に、SciteはDOI照合・訂正通知の検出に使用した。Consensusの検索結果は引用前にfetchした。検索サービスの要約・引用数・支持／反対分類だけで理論の正しさを判定していない。出版社の一部ページは直接取得が403となったため、検索経由の出版社本文または公開原論文で補った。取得できなかった数式等の限界は各分担記録に明記した。

分担記録：[第1〜4回](reviews/2026-09-09/reference-audit/l01-l04.md)、[第5〜10回](reviews/2026-09-09/reference-audit/l05-l10.md)、[第11・12回](reviews/2026-09-09/reference-audit/l11-l12.md)。
