# 2026-09-09 再レビューに基づく修正・検証記録

`CORE_COURSE_REVIEW_2026-09-09.md` の新規指摘3件と任意の明確化2件を反映した。既存の未コミット修正を保持し、今回の差分は `source-before/` と `source-changes.patch` に保存した。元のレビュー文書はレビュー時点の記録として保持している。

## 反映した内容と配布物

| 対象 | 修正 | 更新済み配布物 |
|---|---|---|
| [第3回原稿](/Users/kenjimyzk/work/gradmacro2026/lecture03.qmd:418) | Bellman問題が先行節のNo-Ponzi条件を継承すること、価値関数を実行可能経路上で定義すること、一階条件が内点解に対応することを明記 | [HTML](/Users/kenjimyzk/work/gradmacro2026/lecture03.html) / [PDF](/Users/kenjimyzk/work/gradmacro2026/lecture03.pdf) |
| [第5回原稿](/Users/kenjimyzk/work/gradmacro2026/lecture05.qmd:641) | 本文と図注の「A=1」を削除し、縦軸が正規化した税収 $TX/\mathcal A$ であることを明記 | [HTML](/Users/kenjimyzk/work/gradmacro2026/lecture05.html) / [PDF](/Users/kenjimyzk/work/gradmacro2026/lecture05.pdf) |
| [第10回原稿](/Users/kenjimyzk/work/gradmacro2026/lecture10.qmd:1431) | CRRA分数式を $\gamma\ne1$ に限定し、$\gamma=1$ では $C=1$ より $\log C_t=c_t$、消費の二次項はゼロとなることを補足 | [HTML](/Users/kenjimyzk/work/gradmacro2026/lecture10.html) / [PDF](/Users/kenjimyzk/work/gradmacro2026/lecture10.pdf) |
| [第11回原稿](/Users/kenjimyzk/work/gradmacro2026/lecture11.qmd:393) | 同じ賃金のもとでは、消費が高いタイプほど消費の限界効用と最適点の労働の限界不効用が低くなり、労働供給を減らすという説明に修正 | [HTML](/Users/kenjimyzk/work/gradmacro2026/lecture11.html) / [PDF](/Users/kenjimyzk/work/gradmacro2026/lecture11.pdf) |
| [第12回原稿](/Users/kenjimyzk/work/gradmacro2026/lecture12.qmd:937) | 発展の資源制約と資本蓄積式を $Y_t=C_t+I_t+G_t$、$K_{t+1}=(1-\delta)K_t+I_t$ に統一し、水準と減耗率を明記 | [HTML](/Users/kenjimyzk/work/gradmacro2026/lecture12.html) / [PDF](/Users/kenjimyzk/work/gradmacro2026/lecture12.pdf) |

第5回の計算、第11・12回の主要式と演習解答、第10回の厚生近似の最終式は変更していない。`solution.qmd` と `lecture11_outline.md` の関連箇所を照合し、今回の訂正を反映する追加変更は不要と判断した。別担当による5講義の差分の独立確認でも、追加の不整合は見つからなかった。

## 実施した検証

- **verified — 原稿・関連文書**：今回の5件が原稿の変数定義、仮定、関連解答と整合することを確認。`source-changes.patch` は今回作業開始時点からの差分であり、以前の変更と分離して確認できる。
- **verified — 再生成**：Quarto 1.10.18、既存のR描画設定とLuaLaTeXにより5講義を `--to all` で再生成し、すべて終了コード0。第5回は設定・図のRチャンク実行を含む。最終レンダーログに `WARNING`、`ERROR`、`Overfull`、`Underfull` は検出されなかった。実行コマンド・時間は `render-status.json`、全文ログは各 `lectureNN-render.log`。
- **verified — HTML静的検査**：5講義のローカル画像・スクリプト・リンク、内部参照、ID重複、未解決参照を検査し問題0。記録は `html-static-verification.json`。
- **verified — PDFテキスト**：5講義の全ページからテキストを抽出し、置換文字と未解決参照は0。ページ数は第3回25、第5回21、第10回44、第11回32、第12回48。記録は `pdf-text-verification.json`。
- **verified — PDF目視**：修正ページと関連する改ページ前後の計10ページを画像で確認。第3回13・14頁、第5回17・18頁、第10回32・33頁、第11回12・13頁、第12回34・35頁。数式の大文字・添字、追記した条件と説明、ラッファー図の日本語と図注を確認し、切れ・重なり・文字化けは見つからなかった。対応画像は同フォルダの `lectureNN-page-P.png`。
- **verified — 差分**：`git -c core.fsmonitor=false diff --check` を通過。

第5回の初回レンダーはサンドボックス内でQuartoの既定ユーザーキャッシュを開けず停止した。必要な権限で同じレンダーを再実行し成功した。初回記録は `lecture05-initial-render.log` と `lecture05-initial-render.json` に残している。グローバル設定やパッケージの変更・導入は行っていない。

## 検証の範囲

- **not run — ブラウザ表示**：ブラウザ内のKaTeX実行とHTMLレイアウトは今回確認していない。HTML静的検査とPDF目視はこれらを代替しない。
- **not run — 全教材の再監査**：変更していない講義の再生成、前回の大規模数値検算の再実行、全ページの目視は今回の範囲外。
- **not run — 外部環境・配信**：データ再取得、他OS、新規パッケージ導入環境、公開サイトへの配信は今回の範囲外。

HTMLと付随アセットは既存の `.gitignore` によりGit管理外だが、ワークスペース内の出力は更新済み。
