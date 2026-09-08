# 指摘3〜6・表記・描画環境の反映（2026-09-09）

再レビューの指摘3〜6、表記に関する6項目、および日本語の図の再生成に関する指摘7を反映した。影響する第1・3・5・7・9回と解答集のHTML/PDFを再生成した。先に確定・反映した指摘1・2は保持している。

## 本文・演習・解答

| 対象 | 修正内容 |
|---|---|
| 指摘3・第6回問3の解答 | 総費用を明示し、設問どおり制約付きラグランジュ関数から価格FOCを導出。生産量に依存する限界費用と総費用を区別した。最終的なマークアップ式は維持 |
| 指摘4・第9回問9の解答 | 安定化バイアスを、同じ初期条件からの期待割引総厚生損失の比較として説明。産出・インフレの変動がそれぞれ大きくなるという誤った含意を除いた |
| 指摘5・第7回本文、問5、解答 | 将来ギャップ期待を所与とした比較を明示。当期の金利差だけではギャップの符号は決まらないことを、IS式と数値例で説明 |
| 指摘6・第9回本文 | 時点1のコミットメント条件と再最適化条件の両方で、厚生ギャップを $x_1^e$ に統一 |
| 表記・第3回 | 配当と利子率が確定している場合もSDF自体は確率的であり得るため、割引係数の積と等置する対象を $E_tQ_{t,t+i}$ に修正 |
| 表記・共通記号表 | 自然配分と効率的配分が一致する条件を明確化。第3回の $R_t^f$ は無リスク収益率、後続回の $r_t^f$ は自然利子率と区別 |
| 表記・第9回 | 特性多項式を $q_0(\lambda)$ とし、厚生ギャップとの記号衝突を解消。一般定常状態では効用単位の損失を $U_CY$ で割り、その後に産出ギャップの重みを1にする手順を明示 |
| 表記・第12回問10の解答 | $\Theta_D=\Theta_T$ は集計Euler方程式の利子率係数の一致を表すと説明。PE曲線の傾き $\omega_T$ と区別 |

第6・12回の設問・本編は既に修正版解答と整合しており、変更は不要だった。第3回の確定配当のPV式も維持した。第4・10回の講義ソース、HTML、PDFは前段階のSHA256と完全一致し、解答集内の両章も編集前後で一致する。

## 図の描画環境

第5・9回の図を共通の `scripts/japanese-graphics.R` に接続した。RのCairoデバイスでPDFとPNGを生成し、導入済みの日本語フォントから必要な字形を持つものを選ぶ。個人の絶対パスと、依存不足時に日本語が描けないまま続行する処理を除いた。

今回のmacOS環境では必要なパッケージが揃っており、追加インストールやグローバル設定変更は行っていない。不足時にはリポジトリ内のRライブラリへ導入する準備スクリプトを用意した。受講者向けの準備・検査・再生成・図コード単独実行の手順は[描画環境の説明](/Users/kenjimyzk/work/gradmacro2026/scripts/README-graphics.md)を参照。

R 4.6.1、Cairo、systemfonts 1.3.2で確認した。単体検査ではHiragino Sans、配布PDFの図ではNotoSansJPが選択され、双方の出力で日本語を確認した。図のフォントとTeX本文のフォントを区別して埋込みを検査した。第5・9回のパラメータ・計算部分は修正前と一致する。

## 検証結果

- **理論・数値：verified。** 価格設定48ケース、元の非線形効用からの厚生曲率216ケース、確率的SDFの4期間例、ペッグの特性多項式18ケースを独立検算した。第7回の反例と第9回の政策比較も再実行した。[理論確認](/Users/kenjimyzk/work/gradmacro2026/reviews/2026-09-09/remaining/INDEPENDENT_THEORY_CHECK.md)、[検算コード](/Users/kenjimyzk/work/gradmacro2026/reviews/2026-09-09/remaining/check_theory.py)、[数値結果](/Users/kenjimyzk/work/gradmacro2026/reviews/2026-09-09/remaining/numeric-checks.json)。
- **生成：verified。** 6文書のHTMLとPDFがすべて終了コード0で生成された。TeXパッケージの自動インストールは無効化。組版を調整した3文書のみ追加で再生成した。[生成ログの一覧](/Users/kenjimyzk/work/gradmacro2026/reviews/2026-09-09/remaining/render-status.json)。
- **HTML静的検査・PDF文字抽出：verified。** ローカル画像・スクリプト・リンク、内部参照、ID重複、数式区切りを検査した。PDFの置換文字・未解決参照は0。[検査コード](/Users/kenjimyzk/work/gradmacro2026/reviews/2026-09-09/remaining/verify_outputs.py)。
- **PDF・図の視覚確認：verified。** 変更箇所と前後を中心に40ページ、およびHTMLに埋め込む第5・9回のPNGを点検した。第1回の記号表見出し、第5回の演習冒頭、解答集の第12回問10についてページ分断を調整し、最終PDFを再確認した。数式・日本語ラベル・凡例に切れや欠字は見られない。全ページの視覚監査ではない。[確認ページと最終結果](/Users/kenjimyzk/work/gradmacro2026/reviews/2026-09-09/remaining/visual-qa.json)。
- **HTMLのブラウザ表示：blocked。** ローカルHTMLへの移動がブラウザのセキュリティ方針で拒否された。別経路での回避は行っていない。静的検査と埋込画像の確認は完了したが、ブラウザでのレイアウトとKaTeXの実行時表示は未確認。

他OSでの描画、新規環境への依存インストール、公開サイトへの配信は実施していない。初回生成時のQA記録は `graphics/` と `solution-qa/` に保存し、改ページ修正後の記録と区別した。現在のソースと出力のSHA256は[最終manifest](/Users/kenjimyzk/work/gradmacro2026/reviews/2026-09-09/remaining/manifest.json)に保存した。

## 更新済みの配布ファイル

| 文書 | PDF | HTML |
|---|---|---|
| 第1回・共通記号表 | [PDF](/Users/kenjimyzk/work/gradmacro2026/lecture01.pdf) | [HTML](/Users/kenjimyzk/work/gradmacro2026/lecture01.html) |
| 第3回 | [PDF](/Users/kenjimyzk/work/gradmacro2026/lecture03.pdf) | [HTML](/Users/kenjimyzk/work/gradmacro2026/lecture03.html) |
| 第5回 | [PDF](/Users/kenjimyzk/work/gradmacro2026/lecture05.pdf) | [HTML](/Users/kenjimyzk/work/gradmacro2026/lecture05.html) |
| 第7回 | [PDF](/Users/kenjimyzk/work/gradmacro2026/lecture07.pdf) | [HTML](/Users/kenjimyzk/work/gradmacro2026/lecture07.html) |
| 第9回 | [PDF](/Users/kenjimyzk/work/gradmacro2026/lecture09.pdf) | [HTML](/Users/kenjimyzk/work/gradmacro2026/lecture09.html) |
| 解答集 | [PDF](/Users/kenjimyzk/work/gradmacro2026/solution.pdf) | [HTML](/Users/kenjimyzk/work/gradmacro2026/solution.html) |
