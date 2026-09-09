# 第4回：3節の簡略化と11節の削除

ユーザーの指示に基づき、3節は家計・企業・市場均衡の説明に集中させ、厳密な条件と最適性の証明は本講義で扱わないと本文に明記した。11節は講義から削除した。

## 変更内容

- [lecture04.qmd 第3節](/Users/kenjimyzk/work/gradmacro2026/lecture04.qmd:86)：可測性・可積分性、状態価格の展開、多期間の終端式、最適性の証明への参照を削除。有限信用限度、非拘束・内点の対称均衡、必要な横断性条件、無バブル価格の仮定を短く残した。
- 家計の予算制約の左右を説明し、集計した `C = D + WN` に企業利潤を代入して `Y = C` を得る手順を明示。SDFと配当割引は第3回の結果を簡潔に再利用した。
- [第4回の問1・問4](/Users/kenjimyzk/work/gradmacro2026/lecture04.qmd:473)：信用限度と横断性の区別、非拘束性の技術的確認を削除。対応する [solution.qmd](/Users/kenjimyzk/work/gradmacro2026/solution.qmd:301) も同期した。
- 第11節「発展補論：信用限度と家計の最適性」と、その参照を削除。過去のレビュー記録は当時の記録として保持した。

## 更新した配布物

| 文書 | 原稿 | HTML | PDF | ページ数 |
|---|---|---|---|---|
| 第4回 | [QMD](/Users/kenjimyzk/work/gradmacro2026/lecture04.qmd) | [HTML](/Users/kenjimyzk/work/gradmacro2026/lecture04.html) | [PDF](/Users/kenjimyzk/work/gradmacro2026/lecture04.pdf) | 19 → 14 |
| 解答集 | [QMD](/Users/kenjimyzk/work/gradmacro2026/solution.qmd) | [HTML](/Users/kenjimyzk/work/gradmacro2026/solution.html) | [PDF](/Users/kenjimyzk/work/gradmacro2026/solution.pdf) | 42 → 41 |

## 検証

- **verified — 内容と保持範囲**：別担当による原稿・設問・解答の照合を実施。有限信用限度と無バブル価格を維持し、必要な条件を仮定することと証明を省略することが明確になっている。第4回の4〜9節、他の講義と共通include、解答集の第4回以外は変更前と一致する。`baseline.json`、`source-preservation.json`、`source-changes.patch` に記録。
- **verified — 再生成**：既存のQuarto・LuaLaTeX環境で2文書のHTML/PDFを生成し、終了コード0。解答の長いインライン数式を目視後に短く整え、解答集だけ再生成した。コマンドと実行結果は `render-status.json`、最終ログは `lecture04-render.log` と `solution-render.log`。
- **verified — HTML静的検査**：ローカル画像・スクリプト・リンク、内部参照、ID重複、未解決参照に問題なし。記録は `html-static-verification.json`。
- **verified — PDFテキスト**：全ページを抽出し、置換文字と未解決参照は0。記録は `pdf-text-verification.json`。
- **verified — PDF目視**：第4回の2・4・5・6・7・14頁、解答集の13・14・15頁の計9頁を確認。3節、目次末尾、演習と解答、第4・5回の境界に数式の切れ・重なり・文字化け・見出しの孤立はない。確認画像と `visual-qa.json` を保存。
- **verified — 差分**：`git -c core.fsmonitor=false diff --check` を通過。

数式区切りの検査では、再利用した検査コードがラベル付きの `$$ {#eq-...}` を数えていなかったため修正した。原稿の数式区切り自体には欠落はなく、ラベルを含めた検査を通過している。

**not run**：ブラウザ内のHTMLレイアウト・KaTeX実行、全ページの目視、大規模な数値再検算、他環境での実行、公開サイトへの配信。今回の目的は教材の簡略化と配布物の同期であり、新たな最適性証明を実施したという意味ではない。

HTMLと付随アセットは既存の `.gitignore` によりGit管理外だが、ワークスペースの出力は更新済み。
