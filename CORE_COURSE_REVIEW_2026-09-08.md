# マクロ経済学B・再レビュー（2026年9月8日）

**2026-09-09追記：指摘1・2に続き、指摘3〜6、表記の6項目、描画環境の指摘7を反映した。** 問題設定・導出の確定と前段階の修正は[指摘1・2の反映記録](/Users/kenjimyzk/work/gradmacro2026/reviews/2026-09-09/IMPLEMENTATION.md)、今回の修正・再生成・確認範囲は[残る指摘の反映記録](/Users/kenjimyzk/work/gradmacro2026/reviews/2026-09-09/remaining/IMPLEMENTATION.md)を参照。HTMLは生成・静的検査を完了したが、ブラウザ表示はセキュリティ制限により未確認。以下は修正前のレビュー記録である。

対象：第1〜12回、全演習解答、共通の仮定・記号表、GDP図のデータとPythonスクリプト、第5・8・9回のRコード、保存済みHTML/PDF。

**講義全体の構成と主要な均衡式はよく整っている。ただし、第4回の実行可能性条件と第10回のMarkov裁量政策には、最適化問題の成立・解に関わる修正が必要である。前回の「Ready for use」を無条件では維持しない。** 本レビューは指摘のみで、講義原稿、解答、データ、配布用HTML/PDFは変更していない。新規の報告書と検証資料のみを追加した。

## 維持すべき長所

- 第2回のHP循環成分と理論上の需給ギャップの区別、政府支出の二つの尺度と近似次数の説明は適切である。保存データのチェックサムと作図計算も一致した。
- 第4〜8回の固定資本・政府購入・補助金・名目硬直性の追加が、定常状態と対数線形化に対応している。第8回の3ショックの数値解は、独立に構成した均衡条件を満たす。
- 第9回の自然産出量と効率的産出量の区別、第10回の価格・賃金のRotemberg費用からの二次厚生近似は基本的に整合している。後述する政策最適化の指摘は、厚生損失の基本形を否定するものではない。
- 第11〜12回の所得会計、消費格差の消去、自然利子率、純配当移転、条件付き増幅率は整合している。条件付き需要反応と金融政策の完全均衡・厚生順位を区別している点も適切である。

## 優先修正

### 1. [P1] 家計自身の限界効用SDFではNo-Ponzi制約を定義できない

対象：[lecture04.qmd:103](/Users/kenjimyzk/work/gradmacro2026/lecture04.qmd:103)、[lecture04.qmd:117](/Users/kenjimyzk/work/gradmacro2026/lecture04.qmd:117)。

本文は候補消費経路から計算する

\[
Q_{t,t+N}(h)=\beta^N U_{C,t+N}(h)/U_{C,t}(h)
\]

を用い、\(\liminf E_t[Q(h)A^F]\geq0\) を実行可能集合の制約としている。この条件は、消費を急増させて限界効用を低下させる借金の無限先送りを排除しない。

反例として、本文で許される対数効用・\(\alpha=0\) の場合をとり、所与の価格を \(W=1,R=1/\beta>1\)、労働を1、初期債務をゼロとする。候補消費を \(C_t=K\kappa^t\)、\(K>0,\kappa>R\) とすれば、予算制約から

\[
B_t=\frac{R^{t+1}-1}{R-1}
-K\frac{\kappa^{t+1}-R^{t+1}}{\kappa-R}
\sim-\frac{K\kappa^{t+1}}{\kappa-R}.
\]

市場価格による評価では \(B_t/R^t\to-\infty\) だが、本文の割引因子では \(Q_{0,t}(h)B_t\to0\) となり、掲載した両条件を満たす。各 \(K\) の生涯効用は有限でも、\(K\) を大きくすると効用は上限なく増加する。これは実行可能性に対する反例であり、Euler条件や市場清算を満たす均衡の候補と主張するものではない。

**修正方針：** 実行可能性は所与の市場価格に基づく適切な借入限度・債務制約で定める。家計自身の限界効用SDFによる条件は、最適経路上の横断性条件として分離する。市場価格との対応は最適条件・均衡を導いた後に説明する。

証拠：[再現コード](/Users/kenjimyzk/work/gradmacro2026/reviews/2026-09-08/noponzi_counterexample.py)、[結果](/Users/kenjimyzk/work/gradmacro2026/reviews/2026-09-08/noponzi_counterexample.json)。

### 2. [P1] Markov裁量政策のFOCに将来政策関数の状態依存性が欠落

対象：[lecture10.qmd:1885](/Users/kenjimyzk/work/gradmacro2026/lecture10.qmd:1885)、[lecture10.qmd:1981](/Users/kenjimyzk/work/gradmacro2026/lecture10.qmd:1981)、[solution.qmd:983](/Users/kenjimyzk/work/gradmacro2026/solution.qmd:983)。同じ条件を使う第10回の説明・発展問5・解答も対象になる。

当期に選ぶ \(mc_t\) が翌期の状態なら、裁量政策で所与とするのは将来の政策関数である。その引数が動くため、\(E_t\pi_{t+1}^{p,w}\) の値まで固定して微分することはできない。本文は継続価値 \(\Gamma_t^{mc}=\beta E_tV_s\) を残す一方、Phillips曲線側の期待の微分を落としている。状態遷移を通じて将来期待が当期政策に依存する扱いは、[Svensson, “Inflation Targeting”, §3.8・式(3.51)](https://larseosvensson.se/files/papers/HandbookIT.pdf)とも対応する。

\(F_p(mc_t,\xi_t)=E_t\pi^p(mc_t,\xi_{t+1})\)、\(F_w\) を同様に定義すると、正しい \(mc_t\) の条件には

\[
(\kappa_p+\beta F'_p)\Lambda_{1t}
+(-\kappa_w+\beta F'_w)\Lambda_{2t}
+\Lambda_{3t}+\Gamma_t^{mc}=0
\]

が必要である。IS制約側にも同種の微分が現れるが、この問題では政策金利のFOCから \(\Lambda_{4t}=0\) となる。明記された \(\Gamma_t^{mc}=\beta E_tV_s\) に制約側の微分を含めることはできない。

独立した2期間の後ろ向き最適化で確認した。\(\beta=.99,\kappa_p=\kappa_w=.1,\gamma+\varphi=2,\omega_p=\omega_w=30\)、初期状態0、当期技術変化.01のとき、真の最適配分で掲載FOCの残差は **0.003353578**、欠落項は **−0.003353578**。追加後の残差は \(1.74\times10^{-16}\)、全制約残差は \(2.98\times10^{-18}\) だった。無限期間均衡の数値解を報告したものではなく、掲載された一般的FOCに欠落があることを示す検証である。

**修正方針：** 将来政策関数を明示してMarkov裁量の条件を再導出する。現在の式を残すなら「期待を固定した条件付き問題」に限定する。一期間・終端期の静学条件はこの問題を受けない。

証拠：[再現コード](/Users/kenjimyzk/work/gradmacro2026/reviews/2026-09-08/markov_counterexample.py)、[結果](/Users/kenjimyzk/work/gradmacro2026/reviews/2026-09-08/markov_counterexample.json)。

### 3. [P2] 第6回問3の価格設定解答は利潤関数が誤っている

対象：[solution.qmd:557](/Users/kenjimyzk/work/gradmacro2026/solution.qmd:557)。本文の[lecture06.qmd:257](/Users/kenjimyzk/work/gradmacro2026/lecture06.qmd:257)からのラグランジュ関数による導出は正しい。

相対価格を \(s\)、需要を \(q=Ys^{-\psi}\) とすると、解答は利潤を \((s-MC(j))q\) と書き、\(MC(j)\) を一定として微分している。しかし第6回は \(\alpha>0\) を許し、総費用は

\[
WN=W(q/e^a)^{1/(1-\alpha)}=(1-\alpha)MC(j)q
\]

である。限界費用も企業自身の産出に依存する。正しい利潤 \(sq-W(q/e^a)^{1/(1-\alpha)}\) を微分すれば、掲載された最終的なマークアップ式を得る。**結論は正しいが、導出が成立しない。** 本文の導出にそろえるのがよい。

### 4. [P2] 安定化バイアスは両変数の変動が大きいことを意味しない

対象：[solution.qmd:917](/Users/kenjimyzk/work/gradmacro2026/solution.qmd:917)。

「コミットメントより大きなインフレ・産出変動と厚生損失」という説明は、産出変動について一般には成り立たない。第9回の掲載値 \((\beta,\kappa_x,\omega_p,\rho_u)=(.99,.08,20,.7)\) を使い、単位ショック、\(x_{-1}^e=0\)、以後のイノベーションなしで無限期間の安定解を独立計算した。

| 割引二乗和・損失 | 裁量 | コミットメント |
|---|---:|---:|
| \(\sum_t\beta^t(x_t^e)^2\) | 26.274748 | 53.283136 |
| \(\sum_t\beta^t\pi_t^2\) | 10.263573 | 2.536683 |
| \(\frac12\sum_t\beta^t[(x_t^e)^2+\omega_p\pi_t^2]\) | 115.773108 | 52.008395 |

これは確率的定常分散の表ではなく、同じ初期ショックに対する反応の割引二乗和である。コミットメントは産出低下を長く続けることで、インフレと総厚生損失を減らしている。説明は「総厚生損失が大きい」に限定する。本文の[lecture09.qmd:858](/Users/kenjimyzk/work/gradmacro2026/lecture09.qmd:858)の表現は正しい。

### 5. [P2] 当期の実質利子率ギャップだけでは需給ギャップの正負は決まらない

対象：[lecture07.qmd:598](/Users/kenjimyzk/work/gradmacro2026/lecture07.qmd:598)。

IS曲線は

\[
x_t-E_tx_{t+1}=-(r_t-r_t^f)/\gamma
\]

を与える。したがって、\(r_t>r_t^f\) から直ちに \(x_t<0\) を結論できない。同講義の範囲内で持続性の異なる金融・技術ショックを組み合わせると、**\(x_t=.005>0\)、\(E_tx_{t+1}=.009\)、\(r_t-r_t^f=.004>0\)** という合理的期待解が得られる。IS・NKPC・Taylorルールの残差も確認した。

「将来の需給ギャップ期待を所与とすれば、当期ギャップを押し下げる」と記すか、終端条件のもとで期待される将来の実質利子率ギャップの累積和に結び付ける。

指摘4・5および第8回の均衡式チェックの証拠：[再現コード](/Users/kenjimyzk/work/gradmacro2026/reviews/2026-09-08/lecture05_09_checks.py)、[結果](/Users/kenjimyzk/work/gradmacro2026/reviews/2026-09-08/lecture05_09_checks.json)。

### 6. [P2] 時間的不整合性の式で厚生ギャップの上付きが脱落

対象：[lecture09.qmd:634](/Users/kenjimyzk/work/gradmacro2026/lecture09.qmd:634)、[lecture09.qmd:640](/Users/kenjimyzk/work/gradmacro2026/lecture09.qmd:640)。

両式の \(x_1\) は \(x_1^e\) に直す必要がある。この章では自然産出量ギャップと厚生ギャップを \(x_t=x_t^e+u_t/\kappa_x\) と区別しているため、表記のままではコストプッシュショック下で別の条件になる。

### 7. [P2] 日本語描画の依存関係が不足するとPDFの図が壊れる

対象：[lecture05.qmd:650](/Users/kenjimyzk/work/gradmacro2026/lecture05.qmd:650)、[lecture09.qmd:903](/Users/kenjimyzk/work/gradmacro2026/lecture09.qmd:903)。

現環境のR 4.6.1では `showtext` と `sysfonts` がなく、コードが日本語対応をせずに描画を続ける。一時コピーを通常のQuarto設定でPDF化すると、第5回18ページの軸名・図タイトル、第9回26ページの軸名・凡例が点列になった。PDFのコンパイル自体は成功するため、終了コードだけでは検出できない。

**保存済み第5回PDFの同じ図は読めている。** 今回の問題は、現在の環境で再生成した場合に再現したものであり、配布済みPDFを壊したわけではない。必要パッケージ・フォントを再現手順に明記して事前検査するか、日本語を扱えるPDFデバイスを明示する必要がある。個人の絶対フォントパスだけに依存しない構成が望ましい。レビューではパッケージのインストールや原稿の変更はしていない。

証拠：[保存済み第5回の図](/Users/kenjimyzk/work/gradmacro2026/reviews/2026-09-08/lecture05-stored-p18.png)、[再生成した第5回](/Users/kenjimyzk/work/gradmacro2026/reviews/2026-09-08/lecture05-fresh-p18.png)、[再生成した第9回](/Users/kenjimyzk/work/gradmacro2026/reviews/2026-09-08/lecture09-fresh-p26.png)。

## あわせて直す局所的な表記・前提

| 箇所 | 確認事項・修正案 |
|---|---|
| [lecture03.qmd:852](/Users/kenjimyzk/work/gradmacro2026/lecture03.qmd:852) | 配当と無リスク金利の経路が確定していても、消費に不確実性が残ればSDF自体は確定しない。等号の左辺を \(E_tQ_{t,t+i}\) にするか、消費も確定する決定論的ケースと明記する。最終的な配当現在価値式は正しい。 |
| [notation-concordance.qmd:17](/Users/kenjimyzk/work/gradmacro2026/includes/notation-concordance.qmd:17) | 「是正補助金とコストプッシュ・ウェッジなし」は補助金もないと読める。「是正補助金で歪みを除き、コストプッシュ・ウェッジがなければ」とする。第9回本文の条件は正しい。 |
| [notation-concordance.qmd:40](/Users/kenjimyzk/work/gradmacro2026/includes/notation-concordance.qmd:40) | 第3回の \(R_t^f\) は無リスク粗実質収益率であり、自然利子率ではない。後続回の自然利子率を表す上付き \(f\) と区別する。 |
| [solution.qmd:1389](/Users/kenjimyzk/work/gradmacro2026/solution.qmd:1389) | \(\Theta_D=\Theta_T\) は集計Euler式の利子率係数の対応を意味する。「NKクロスの傾きとIS曲線の傾きが一致」とはならない。両者の縦軸・横軸と係数を区別する。 |
| [lecture09.qmd:1168](/Users/kenjimyzk/work/gradmacro2026/lecture09.qmd:1168) | 特性多項式を \(x_0^e(\lambda)\) と命名しており、厚生ギャップと衝突する。後続2箇所も含め \(q_0(\lambda)\) 等に変更する。 |
| [lecture09.qmd:167](/Users/kenjimyzk/work/gradmacro2026/lecture09.qmd:167) | \(C=N=\nu=1\) は第2回の単純形の説明に限定し、その後の一般形は \(U_CY\) による効用の正規化を明示するとよい。一般形の厚生係数自体は正しい。 |

## 検証した範囲と限界

| 検証 | 結果 |
|---|---|
| 全12回、共通include、全演習解答の理論・記号照合 | `verified`。上記の指摘を検出。第4回の反応係数、第8回の均衡、第10回の価格・賃金厚生近似、第11〜12回のTANK縮約などを独立に再導出した。 |
| ローカル図の参照、式・図・表ラベル | `verified`。対象13文書で検査した参照に未定義ラベル、重複ラベル、欠落画像なし。外部リンク全件の到達検査とは異なる。 |
| GDPデータ・HP分解 | `verified`。318観測、1947Q1〜2026Q2、READMEのSHA-256と一致。一時コピーで作図スクリプトを実行。独立の帯行列計算とのトレンド最大差は \(3.40\times10^{-12}\)。最新版データへの更新はしていない。 |
| 第5・8・9回のRコード | `verified`（数値）。各チャンクを独立した `Rscript --vanilla` で実行。第5回のピーク、第8回の実際のR出力と独立解、第9回の行列・NKPC残差を検査。最大残差はそれぞれ約 \(1.05\times10^{-10}\)、\(5.00\times10^{-16}\)、\(6.11\times10^{-16}\)。 |
| HTML再生成 | `verified`。一時コピーで全13文書が成功。保存済み版と、main内の正規化した本文・数式テキストが一致。CSSや全画像の同一性、ブラウザでの全ページ表示を保証する検査ではない。 |
| PDF再生成 | `verified`（コンパイル）。第2回22ページ、第5回21ページ、第9回30ページ、解答38ページ。原本は上書きしていない。 |
| 再生成PDFの図の日本語 | `failed`。第5・9回の点列化を画像と抽出テキストで確認。数値計算の失敗ではない。 |
| PDFテキスト・視覚検査 | 保存済み13 PDFの計360ページからテキストを抽出。保存済み版は各文書1ページ、再生成版は上記4文書の各1ページを視認した。全360ページの目視検査ではない。 |
| その他 | `not run`：残り9文書のPDF再生成、全PDFページの目視、全参考文献の書誌・帰属確認、別OS・新規受講者環境での再現、公開サイトへの配信確認。 |

初回の再レンダーはQuartoのSassキャッシュとLuaLaTeXのフォントキャッシュへの書込制限で停止した。TeXキャッシュを一時ディレクトリに置き、Quartoの標準キャッシュへの書込みを許可したうえで再実行し、上記の最終結果を得た。再実行ではTeXパッケージ自動インストールを無効にした。この環境上の初回停止を教材自体の不具合として数えていない。

検証環境・対象ソースのSHA-256・Git HEAD・目視ページは[検証マニフェスト](/Users/kenjimyzk/work/gradmacro2026/reviews/2026-09-08/review_manifest.json)、実行結果は[検証資料ディレクトリ](/Users/kenjimyzk/work/gradmacro2026/reviews/2026-09-08)に保存した。

修正する場合は、指摘1・2の問題設定／導出を先に確定し、対応する本文・演習・解答を同時に更新する。その後、指摘3〜6と表記を整理し、図の描画環境を整えて、影響するHTML/PDFを再生成・確認する。
