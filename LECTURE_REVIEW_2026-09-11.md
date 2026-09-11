# 講義ノート再レビュー・PDF確認（2026-09-11）

> 修正対応完了：この文書は修正前のレビュー記録です。全指摘への対応と配布用PDF・HTMLの再検証は [修正報告](/Users/kenjimyzk/work/gradmacro2026/LECTURE_FIXES_2026-09-11.md) を参照してください。

第1〜12回と解答集を現行原稿から再レビューした。**PDFは全13文書・412ページの再生成に成功したが、第5回の数式切断、第8回の記号欠落など、配布前に直すべき箇所が残る。** 内容面でも、CESの代替弾力性の符号、図の数値、説明とモデルの条件の食い違いが見つかった。

今回の作業はレビューと再レンダリングであり、講義原稿の修正は行っていない。ルートにある既存PDF/HTMLも保全し、再生成PDF・ログ・点検画像を [reviews/2026-09-11](/Users/kenjimyzk/work/gradmacro2026/reviews/2026-09-11/) に保存した。以下のページ番号はすべて今回再生成したPDFの物理ページ番号である。

## PDFで確認した修正対象

| 優先度 | 箇所 | 確認結果と最小修正案 |
|---|---|---|
| P2 | **第5回 p17** — [lecture05.qmd:396](/Users/kenjimyzk/work/gradmacro2026/lecture05.qmd:396) | 政府支出乗数の数値代入を1行に並べた式が紙面右端を越え、末尾 `0.349` が途中で切れる。文字の最大x座標609.43ptに対し紙幅595.28pt。数値代入を2〜3行に分ける。 |
| P2 | **第8回 p23** — [lecture08.qmd:841](/Users/kenjimyzk/work/gradmacro2026/lecture08.qmd:841) | 図3のキャプションで `γ=ϕ=1` のϕが欠落し、`γ= =1` と見える。LuaLaTeXもU+03D5の欠字を報告。図注のパラメータを `$\gamma=\varphi=1$` 等の数式表記にする。図本体の9パネルは描画されている。 |
| P3 | **第8回 p9** — [lecture08.qmd:240](/Users/kenjimyzk/work/gradmacro2026/lecture08.qmd:240) | `eta` のTeX命令の前にバックスラッシュが二重に入り、意図したηにならない。`$\eta=0$` に直す。 |
| P2 | **第1回 p16・p22** — [phillips_curve_expectations.svg:45](/Users/kenjimyzk/work/gradmacro2026/figures/lecture01/phillips_curve_expectations.svg:45)、[lucas_critique_flow.svg:43](/Users/kenjimyzk/work/gradmacro2026/figures/lecture01/lucas_critique_flow.svg:43) | 図内下部の太字タイトルと補足説明が同じ高さで重なり、文字を読みにくくしている。説明を次行へ送るか開始位置を広げる。PDFのコンパイル警告では検出されない。 |
| P2 | **第1回 p11** — [is_lm_equilibrium.svg:36](/Users/kenjimyzk/work/gradmacro2026/figures/lecture01/is_lm_equilibrium.svg:36) | 黒い均衡点と破線がIS・LM曲線の実際の交点から右下にずれる。曲線の交点にマーカーと破線を合わせる。 |
| P2 | **第6回 p8・p9・p13・p16** — [lecture06.qmd:159](/Users/kenjimyzk/work/gradmacro2026/lecture06.qmd:159)、[178](/Users/kenjimyzk/work/gradmacro2026/lecture06.qmd:178)、[297](/Users/kenjimyzk/work/gradmacro2026/lecture06.qmd:297)、[388](/Users/kenjimyzk/work/gradmacro2026/lecture06.qmd:388) | CESの仮定・生産関数・企業のラグランジュ関数・配当の長式が右余白や説明枠へ侵入。ページ内には残るが、最大64.51ptのoverfull。連続等式と制約を改行する。 |
| P3 | **第9回 p6** — [lecture09_overview_infographic.svg:39](/Users/kenjimyzk/work/gradmacro2026/figures/lecture09/lecture09_overview_infographic.svg:39)、[79](/Users/kenjimyzk/work/gradmacro2026/figures/lecture09/lecture09_overview_infographic.svg:79) | 全体図の説明が箱の右端へ出るほか、6→7の矢印先端が「政策評価の基準」に重なる。箱内の文章を改行し、矢印を箱の境界で止める。 |
| P2 | **第10回 p8** — [lecture10.qmd:185](/Users/kenjimyzk/work/gradmacro2026/lecture10.qmd:185) | 価格設定条件の長式が41.78ptのoverfullとなり、本文の右端を越える。期待項を次行へ送る。 |
| P3 | **第11回 p22〜23** — [lecture11.qmd:667](/Users/kenjimyzk/work/gradmacro2026/lecture11.qmd:667) | 「金融政策ショックへの含意」の説明枠が「フィー」で分かれ、次ページ上部の図2を挟んで「ドバック」から再開する。図を枠の前後へ固定し、枠全体に必要な残り高さを確保する。 |
| P3 | 第4・5・6・10・11回のその他の長式 | 全体ではoverfull警告12件。紙外切断と余白への侵入は区別して評価した。小さな超過も、式の途中で改行すれば整えられる。各ページと元のTeX行は下記の詳細視覚報告に記録。 |
| P3 | **解答集 p26** | 第8回問6の最後の式と短文のみが独立ページに残る。前ページの同解答ブロックの間隔調整または問全体の改ページを検討。p7・p21にも短い末尾だけのページがある。文字欠落ではない。 |
| P3 | **第4回 p18、第5回 p28、第10回 p21** | 第4回の比較表は説明列が狭すぎて細かな改行が連続する。第5回は演習末尾2行だけが独立ページ、第10回は問4見出しだけがページ末に孤立する。表の列幅、演習ブロックの改ページ位置を調整する。 |

## 内容・数値で確認した修正対象

| 優先度 | 箇所 | 指摘と最小修正案 |
|---|---|---|
| P2 | **第6回 CESの代替弾力性** — [lecture06.qmd:163](/Users/kenjimyzk/work/gradmacro2026/lecture06.qmd:163) | `MRTS ∝ (X₁/X₂)^(ρ−1)` なので、掲載された `d ln(X₁/X₂)/d ln MRTS` は `1/(ρ−1)`。正の弾力性 `1/(1−ρ)` を定義するには微分比の前に負号を加えるか、投入比を逆にする。後続のマークアップ式は正しい。 |
| P2 | **第6回 利益比例税の説明、p12** — [lecture06.qmd:256](/Users/kenjimyzk/work/gradmacro2026/lecture06.qmd:256) | 売上や利益に連動する税なら価格設定を再び歪めるとするが、全費用控除後の純利益に定率τ<1を課すだけなら目的関数は `(1−τ)D` となり、最適価格は変わらない。「売上に連動する税」に絞るか、利益税の控除条件を明示する。 |
| P2 | **第7回 事前・事後実質収益率、p7** — [lecture07.qmd:138](/Users/kenjimyzk/work/gradmacro2026/lecture07.qmd:138) | `Π_(t+1)` は実現インフレであり期待値ではなく、`Rᴺ_t/Π_(t+1)` は不確実な事後実質粗収益率。本文の「期待インフレ率」「事前的実質収益率」という読み下しを修正する。掲載Euler式と後半の一次近似 `r_t=rᴺ_t−E_tπ_(t+1)` は正しい。 |
| P2 | **第2回 AR(1)図、p10** — [ar1_irf_simulation.svg:46](/Users/kenjimyzk/work/gradmacro2026/figures/lecture02/ar1_irf_simulation.svg:46) | 緑のρ=0.8の曲線が `0.8^h` と不一致。h=12で描画値0.0545、正解0.0687195（約20.7%過小、原寸座標差4.55px）。該当ポリラインの座標を式から再生成する。本文式と演習解答は正しい。 |
| P2 | **第2回 技術ショックと雇用、p11** — [lecture02.qmd:210](/Users/kenjimyzk/work/gradmacro2026/lecture02.qmd:210) | 技術改善による「産出量や雇用の増加」の持続と断定するが、第4回モデルではγ=1で雇用不変、γ>1で減少する。「各変数の反応が長く残り、符号はモデルや選好に依存する」とする。 |
| P2 | **第2回 二次厚生評価、p22** — [lecture02.qmd:571](/Users/kenjimyzk/work/gradmacro2026/lecture02.qmd:571) | 確率的動学モデルなら政策関数も必ず二次まで必要と読める。制約を用いて政策依存の一次項を除いた純粋二次損失なら、一次政策関数で二次厚生を評価できる。本講義の第8・9回が使う例外を明示する。 |
| P2 | **第10回 純配当の尺度、p18** — [lecture10.qmd:652](/Users/kenjimyzk/work/gradmacro2026/lecture10.qmd:652) | 定常純配当はゼロなので、`d_t` は「対数乖離」ではなく「定常消費で規格化した純配当の一次偏差」。第11回と共通記号表に合わせる。式そのものは正しい。 |
| P2 | **第5回 引用研究の最大税収税率、p22** — [lecture05.qmd:525](/Users/kenjimyzk/work/gradmacro2026/lecture05.qmd:525) | Trabandt–Uhlig (2011) を「概ね50〜60%」とまとめるが、基準モデルは米国63%、EU-14 62%、感度分析では米国52〜72%、EU-14 51〜71%。特定の設定を明記するか、数値の一般化を避ける。ノート自身の76.9%という計算は正しい。原論文の表は著者公開PDFの検索抽出で確認、PDF本体の直接取得は404だったため、その限界も詳細報告に残した。 |
| P2 | **第12回 直接効果の説明** — [lecture12.qmd:45](/Users/kenjimyzk/work/gradmacro2026/lecture12.qmd:45)、[628](/Users/kenjimyzk/work/gradmacro2026/lecture12.qmd:628) | 所得固定のPE切片を直接効果と定義する一方、一般の期待閉鎖係数pに対しても「直接効果が1−λ倍」と説明。実際のPE切片比は `(1−λ)(1−βp)/[1−βp(1−λχ)]`。β=.99,p=.5,λ=.3,χ=2なら0.440773で、人口比0.7とは異なる。1−λ倍は期待を所与とする再帰式の当期係数、またはp=0の比較に限定する。総効果比1.75とp=0の既存図は正しい。 |

二次厚生評価の限定については、著者自身の [Schmitt-Grohé and Uribe (2004), Policy Evaluation in Macroeconomics](https://www.columbia.edu/~ss3501/research/sednewsletter.htm) も、効率的定常状態で一次解による二次厚生評価が可能であることを説明している。今回の指摘は「二次政策関数は不要」という一般論ではなく、一次項が残る場合と除去できる場合の区別である。

税率の記載との照合には [Trabandt and Uhlig (2011), The Laffer Curve Revisited](https://home.uchicago.edu/~huhlig/papers/uhlig.trabandt.jme.2011.pdf) のTable 5・9を用いた。これは参考文献全件の再監査ではなく、本文の特定の数値主張に限った確認である。

軽微な整合性の修正候補として、第2回551行の「一次項が完全にゼロ」という説明（価格調整費用の二次部分は残る）、第4回465行の対数近似の分母Rの欠落、第4回の自然利子率記号 `rⁿ` と解答の `rᶠ`、第10回45行の柔軟賃金なら賃金インフレ率が「存在しない」という表現、第11回1092行の金融政策ショックと移転の単位混在もある。詳細報告に最小修正案を記録した。

## 実施した検証

- **ソース確認：verified。** 第1〜12回の全文、対応する演習解答、共通の仮定表・記号表を照合。内部ラベルの重複、参照先欠落、画像ファイル欠落は全13文書で検出なし。原稿・共通部品・図・データ・スクリプト58ファイルのSHA-256が開始時と一致。
- **PDF再レンダリング：verified。** Quarto 1.10.18、LuaHBTeX 1.22.0 / TeX Live 2025、LuaLaTeXを使用。原稿のコピーと一時キャッシュで、全13文書が終了コード0。元の原稿と既存PDFを保全した。
- **PDF構造検査：verified、表示上の不備：failed。** 全412ページのテキスト抽出、紙面境界、欠字・overfullログを検査。未解決参照 `??` と置換文字はゼロだが、それだけでは欠字を検出できず、ϕ欠落はコンパイルログと目視で確認した。上記の切断・欠字・余白侵入は未修正。
- **PDF目視：verified with findings。** 全412ページをコンタクトシートで俯瞰し、図表・長式・警告箇所・改ページが疑わしい箇所を個別画像で拡大確認した。全ページの文字を拡大して一字ずつ校正したという意味ではない。図内の重なりや均衡点のずれは目視とSVGソースの照合で確認した。
- **Rコード実行：verified。** 第5・8・9回の現行チャンクを専用作業ディレクトリの新規 `Rscript --vanilla` プロセスで実行。既存の日本語フォント設定を使用し、図を目視確認した。R 4.6.1、Cairo、Hiragino Sans、systemfonts 1.3.2。
- **独立数値検算：verified。** 第4回の水準均衡192ケース、第8回のショック応答の連立方程式、第10回600ケース、第11回600ケース、第12回400組の検算などを実施。第11回の最大誤差・残差は約4.10×10⁻¹³、第12回は約2.74×10⁻¹³。上記の個別指摘を除き、検算した均衡式と数値解は整合。検算は全パラメータ域の存在一意性の証明ではない。
- **not run。** HTMLの再生成・ブラウザ検査、GDPの再取得、全参考文献の再監査、クラウド実行、WebClassへの公開は今回実施していない。

## 再生成PDFと証拠

| 文書 | ページ数 | 今回のPDF |
|---|---:|---|
| 第1回 | 31 | [lecture01.pdf](/Users/kenjimyzk/work/gradmacro2026/reviews/2026-09-11/pdf/lecture01.pdf) |
| 第2回 | 27 | [lecture02.pdf](/Users/kenjimyzk/work/gradmacro2026/reviews/2026-09-11/pdf/lecture02.pdf) |
| 第3回 | 34 | [lecture03.pdf](/Users/kenjimyzk/work/gradmacro2026/reviews/2026-09-11/pdf/lecture03.pdf) |
| 第4回 | 25 | [lecture04.pdf](/Users/kenjimyzk/work/gradmacro2026/reviews/2026-09-11/pdf/lecture04.pdf) |
| 第5回 | 28 | [lecture05.pdf](/Users/kenjimyzk/work/gradmacro2026/reviews/2026-09-11/pdf/lecture05.pdf) |
| 第6回 | 21 | [lecture06.pdf](/Users/kenjimyzk/work/gradmacro2026/reviews/2026-09-11/pdf/lecture06.pdf) |
| 第7回 | 25 | [lecture07.pdf](/Users/kenjimyzk/work/gradmacro2026/reviews/2026-09-11/pdf/lecture07.pdf) |
| 第8回 | 28 | [lecture08.pdf](/Users/kenjimyzk/work/gradmacro2026/reviews/2026-09-11/pdf/lecture08.pdf) |
| 第9回 | 33 | [lecture09.pdf](/Users/kenjimyzk/work/gradmacro2026/reviews/2026-09-11/pdf/lecture09.pdf) |
| 第10回 | 28 | [lecture10.pdf](/Users/kenjimyzk/work/gradmacro2026/reviews/2026-09-11/pdf/lecture10.pdf) |
| 第11回 | 38 | [lecture11.pdf](/Users/kenjimyzk/work/gradmacro2026/reviews/2026-09-11/pdf/lecture11.pdf) |
| 第12回 | 51 | [lecture12.pdf](/Users/kenjimyzk/work/gradmacro2026/reviews/2026-09-11/pdf/lecture12.pdf) |
| 解答集 | 43 | [solution.pdf](/Users/kenjimyzk/work/gradmacro2026/reviews/2026-09-11/pdf/solution.pdf) |

詳細な内容報告：[第1〜4回](/Users/kenjimyzk/work/gradmacro2026/reviews/2026-09-11/l01-l04/REVIEW.md)、[第5〜8回](/Users/kenjimyzk/work/gradmacro2026/reviews/2026-09-11/l05-l08/REVIEW.md)、[第9〜12回](/Users/kenjimyzk/work/gradmacro2026/reviews/2026-09-11/l09-l12/REVIEW.md)。

視覚確認記録：[第1〜4回](/Users/kenjimyzk/work/gradmacro2026/reviews/2026-09-11/l01-l04/VISUAL.md)、[第5〜8回](/Users/kenjimyzk/work/gradmacro2026/reviews/2026-09-11/l05-l08/VISUAL.md)、[第9〜12回](/Users/kenjimyzk/work/gradmacro2026/reviews/2026-09-11/l09-l12/VISUAL.md)、[解答集](/Users/kenjimyzk/work/gradmacro2026/reviews/2026-09-11/VISUAL-solution.md)。

再現用：[render_review.py](/Users/kenjimyzk/work/gradmacro2026/reviews/2026-09-11/render_review.py)、[check_pdf.py](/Users/kenjimyzk/work/gradmacro2026/reviews/2026-09-11/check_pdf.py)、[check_sources.py](/Users/kenjimyzk/work/gradmacro2026/reviews/2026-09-11/check_sources.py)。実行結果：[render-results.json](/Users/kenjimyzk/work/gradmacro2026/reviews/2026-09-11/render-results.json)、[pdf-checks.json](/Users/kenjimyzk/work/gradmacro2026/reviews/2026-09-11/pdf-checks.json)、[source-checks.json](/Users/kenjimyzk/work/gradmacro2026/reviews/2026-09-11/source-checks.json)。
