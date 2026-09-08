# 指摘1・2の本文・演習・解答への反映（2026-09-09）

**後続作業：** 指摘3〜6・表記・描画環境も反映した。最新の解答集を含む更新と確認範囲は[後続の反映記録](/Users/kenjimyzk/work/gradmacro2026/reviews/2026-09-09/remaining/IMPLEMENTATION.md)を参照。この文書と同階層の証拠は指摘1・2を反映した段階の記録である。

2026-09-08の確定文書に基づき、第4回、第10回、対応する演習解答を同時に更新した。講義本編は仮定と経済的な意味を中心にし、完全な導出は発展補論に置いた。今回の反映対象は再レビューの指摘1・2であり、指摘3以降の修正は含めない。

## 更新内容

| 対象 | 反映内容 |
|---|---|
| [第4回ソース](/Users/kenjimyzk/work/gradmacro2026/lecture04.qmd) | 純金融資産の有限信用限度、対称初期保有、非拘束性、SDFと横断性条件の役割を本文に反映。問1・4を更新。末尾の発展補論にモーメント条件、価格構成、固定された均衡SDFによるNo-Ponzi性、有限期間の予算恒等式と凹性による十分性証明を追加 |
| [第10回ソース](/Users/kenjimyzk/work/gradmacro2026/lecture10.qmd) | 将来政策関数と期待値の違い、期待の状態微分を含む完全FOC・ターゲット条件・包絡条件を反映。問5は終端から解く二期間演習、問6は両期の実装金利、問7は柔軟賃金モデルの直接導出に変更。正則な極限は任意の追加問 |
| [解答ソース](/Users/kenjimyzk/work/gradmacro2026/solution.qmd) | 第4回問1・4、第10回問5–7を同期。二期間問題は終端係数と価値関数、期待微分、初期時点の条件、正曲率まで示した。第4・10回以外の解答は変更前と一致 |

第4回の「関数形と閉形式解」以降の既存実物分析と、第10回の「モデルの部品」から本編のまとめ直前までが変更前と完全一致することを確認した。新しい信用限度は明示的なモデル仮定だが、選択した対称均衡では非拘束であり、既存の実物配分と反応係数は維持される。

## 検証

- **数値（verified）**：固定信用限度の反例排除・12定常均衡・24代替計画、無限期間の無ショック定常Markov計算を再実行。新しい二期間演習は、一変数解析解と独立したKKT連立系を比較し、非ゼロの初期状態と技術変化を持つ3ケース、既存の基準ケース、両期の全民間制約とIS/Fisher実装を確認した。最大検証残差は約 `2.71e-15`。
- **ソース（verified）**：数式区切り、ラベル重複、内部参照、変更範囲、`git diff --check` を確認。元の監査入力17ファイルのうち変更したのは上記3ソースだけ。
- **生成（verified）**：第4回・第10回・解答のHTMLとPDFをQuartoで生成。TeXパッケージの自動インストールは無効化。PDF抽出テキストに置換文字・未解決参照はなく、HTMLの相互参照も解決した。
- **視覚点検（verified）**：第4回14ページ、第10回21ページ、解答16ページの計51ページを、変更箇所とその前後を中心に点検した。演習がページ境界で分断される2箇所を組版調整し、最終PDFで解消を確認した。確認ページと結果は下記QA記録に記載する。全配布資料・全ページの視覚監査という意味ではない。

## 配布用出力と証拠

| 文書 | PDF | HTML |
|---|---|---|
| 第4回 | [lecture04.pdf](/Users/kenjimyzk/work/gradmacro2026/lecture04.pdf) | [lecture04.html](/Users/kenjimyzk/work/gradmacro2026/lecture04.html) |
| 第10回 | [lecture10.pdf](/Users/kenjimyzk/work/gradmacro2026/lecture10.pdf) | [lecture10.html](/Users/kenjimyzk/work/gradmacro2026/lecture10.html) |
| 解答集 | [solution.pdf](/Users/kenjimyzk/work/gradmacro2026/solution.pdf) | [solution.html](/Users/kenjimyzk/work/gradmacro2026/solution.html) |

- [新しい演習の独立検証コード](/Users/kenjimyzk/work/gradmacro2026/reviews/2026-09-09/check_updated_exercises.py)
- [数値検証の実行結果](/Users/kenjimyzk/work/gradmacro2026/reviews/2026-09-09/numeric-verification.json)
- [ソース検査](/Users/kenjimyzk/work/gradmacro2026/reviews/2026-09-09/source-verification.json)、[生成結果](/Users/kenjimyzk/work/gradmacro2026/reviews/2026-09-09/render-status.json)
- [第4回PDFのQA](/Users/kenjimyzk/work/gradmacro2026/reviews/2026-09-09/lecture04-qa-results.json)、[第10回PDFのQA](/Users/kenjimyzk/work/gradmacro2026/reviews/2026-09-09/lecture10-qa-result.json)、[解答PDFのQA](/Users/kenjimyzk/work/gradmacro2026/reviews/2026-09-09/solution-qa-result.json)

二期間の検証は一般の確率的・無限期間Markov均衡の存在や一意性の証明ではない。今回変更しなかった他講義の再生成、全文献の再検証、公開サイトへの配信は行っていない。
