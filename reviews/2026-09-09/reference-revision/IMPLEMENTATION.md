# 参考文献監査への修正対応

2026年9月9日。[監査レポート](../../../REFERENCE_REVIEW_2026-09-09.md)の確定指摘と補足提案を、講義ノート第1〜12回とシラバスに反映した。講義の数式・計算コード・演習・解答の内容は維持した。

## 対応一覧

| 対象 | 実施した修正 |
|---|---|
| 第1回 | Blanchard『Macroeconomics』第7版・2017年を単著へ訂正。確認済み出版社リンクを補完 |
| 第2回 | Hodrick–Prescott (1997) を本文と基本文献に追加。端点・人工的動学への注意とHamilton (2018) を補足。Galí第2章・著者スライド、参考書の所在を明記 |
| 第3回 | Stokey–Lucas–Prescottの決定論的・確率的動的計画法を、それぞれ第4章・第9章、該当頁へ案内 |
| 第4回 | King–Rebeloの編集者・第14章・頁・DOIを補完。Galí第2章の柔軟価格モデルとの対応を明記 |
| 第5回 | Baxter–King、Aiyagariほか、Leeper、Trabandt–UhligにDOIまたは著者公開PDFを追加。資本蓄積を含む文献と講義の静学的税収分析の関係を説明 |
| 第6回 | Dixit–Stiglitz、Blanchard–Kiyotaki、Spence、Rotemberg–Woodfordへの原典リンクを補完。Rotemberg–Woodfordの論文本体297–346頁を維持 |
| 第7・9回 | Calvo–Rotemberg比較のLombardo–Vestin (2008) を本文と文献に追加。効率的・ゼロインフレ定常状態での局所的対応という限定を維持 |
| 第8回 | Galí第3章を明記。Schmitt-Grohé–Uribeの二次近似法は一般DSGE解法への発展として案内 |
| 第9回 | divine coincidenceの原典Blanchard–Galí (2007) を追加。実質賃金硬直性と第10回の名目賃金費用を区別。Galí第4・5章を指定 |
| 第10回 | EHLはCalvo型契約の政策トレードオフ、Rotembergは価格調整費用の原典、と役割を明記。講義は後者を賃金設定へ拡張する旨を説明。Born–Pfeifer (2020) と2025年訂正を併記。Galí第6章を指定 |
| 第11・12回 | Bilbiie (2008) に2019年訂正論文と併読案内を追加。再分配の仮定・二次厚生近似に関する訂正範囲を説明。Campbell–Mankiwの頁をDOI側の論文本体185–216へ統一 |
| 第12回 | Bilbiie (2020) §§2–3・命題1–2へ読書範囲を限定。原著の外生的金利経路と講義の簡約形期待閉鎖の関係を説明。各HANK比較文献の用途、BKへの相互参照、発展用Klein (2000) QZ解法を追加 |
| シラバス | Galíと日本語教科書の対応章、HP・名目硬直性・NKクロス・訂正論文の読書案内を同期。QMDとMarkdown本文を一致させ、HTML/PDFを生成 |
| PDF組版 | 第1・5回は参考文献を改ページして開始、第2・10回は発展文献を改ページして開始。文献見出しや論文名が不自然に分断される箇所を修正。新規生成したシラバスPDFの文字サイズ・余白・行間を調整 |

詳細：[第1〜4回](l01-l04-changes.md)、[第5〜10回](l05-l10-changes.md)、[第11・12回](l11-l12-changes.md)。原著リンク・書誌の一次確認結果も各記録に収録した。

## 検証

| 確認 | 結果と証跡 |
|---|---|
| 監査との対応 | **verified**：元レポートと3本の詳細監査を現行12回・シラバスへ独立照合。確定指摘・任意補足の未対応、新たな書誌矛盾は検出されなかった |
| 再生成 | **verified**：第1〜12回とシラバスの13文書、HTML/PDF計26出力を既存のR/Quarto経路で再生成。最終原稿・出力のSHA-256がレンダー記録と一致。[記録](render-results.json) |
| 実行コード | **verified**：第5・8・9回のRチャンクはHTML/PDFのレンダー時に実行され、終了コード0。変更のないPython生成スクリプトは再実行していない |
| 参考文献の表示 | **verified**：講義97項目＋シラバス7項目＝104項目をQMD/HTML間で正規化照合。不一致0。PDFの抽出対象となる文献タイトルも欠落0 |
| リンク | **verified**：参考文献の全記載URLがHTML hrefとPDFリンク注釈に存在。ローカルリンク・参照anchor・画像等の欠落0。外部リンク先全件の再取得や実クリックを意味しない |
| 数式・コード・演習 | **verified**：全12回の表示数式955本、インライン数式、計算用コードブロック、演習開始以降の全文が修正前と一致。追加したraw LaTeXは改ページだけ |
| データ等の保全 | **verified**：データ・図・生成スクリプト・解答・共通表など保護対象48ファイルのハッシュ一致。シラバスQMD/Markdown本文も一致 |
| 静的出力検査 | **verified**：未解決参照、重複HTML ID、PDF置換文字、PDFの未解決参照記号を検出しなかった。[統合検証](verification.json)、[検証スクリプト](check_revision.py) |
| PDF目視 | **verified（対象範囲）**：参考文献欄の全ページ、追記箇所、前後の改ページを確認。初回に検出した文献欄の改ページを修正して再確認。新規シラバスは最終版5ページを全て目視。[第1〜4回](l01-l04-visual.md)、[第5〜10回](l05-l10-visual.md)、[第11・12回](l11-l12-visual.md)、[シラバス](syllabus-visual.md) |
| 差分 | `git diff --check` 成功。編集前原稿は [source-before/](source-before/) に保存 |

HTMLの検証は保存ファイルの静的検査であり、全ページのブラウザ・KaTeX表示監査ではない。参考文献の照合に合わせた修正であり、全論文の全文精読や講義理論全体の新しい再検証は行っていない。公開サイトやLMSへのアップロード、Gitコミットは実施していない。

## 更新済み配布物

原稿・HTML・PDFは従来と同じプロジェクト直下に保存した。

| 教材 | 原稿 | HTML | PDF |
|---|---|---|---|
| 第1回 | [QMD](../../../lecture01.qmd) | [HTML](../../../lecture01.html) | [PDF](../../../lecture01.pdf) |
| 第2回 | [QMD](../../../lecture02.qmd) | [HTML](../../../lecture02.html) | [PDF](../../../lecture02.pdf) |
| 第3回 | [QMD](../../../lecture03.qmd) | [HTML](../../../lecture03.html) | [PDF](../../../lecture03.pdf) |
| 第4回 | [QMD](../../../lecture04.qmd) | [HTML](../../../lecture04.html) | [PDF](../../../lecture04.pdf) |
| 第5回 | [QMD](../../../lecture05.qmd) | [HTML](../../../lecture05.html) | [PDF](../../../lecture05.pdf) |
| 第6回 | [QMD](../../../lecture06.qmd) | [HTML](../../../lecture06.html) | [PDF](../../../lecture06.pdf) |
| 第7回 | [QMD](../../../lecture07.qmd) | [HTML](../../../lecture07.html) | [PDF](../../../lecture07.pdf) |
| 第8回 | [QMD](../../../lecture08.qmd) | [HTML](../../../lecture08.html) | [PDF](../../../lecture08.pdf) |
| 第9回 | [QMD](../../../lecture09.qmd) | [HTML](../../../lecture09.html) | [PDF](../../../lecture09.pdf) |
| 第10回 | [QMD](../../../lecture10.qmd) | [HTML](../../../lecture10.html) | [PDF](../../../lecture10.pdf) |
| 第11回 | [QMD](../../../lecture11.qmd) | [HTML](../../../lecture11.html) | [PDF](../../../lecture11.pdf) |
| 第12回 | [QMD](../../../lecture12.qmd) | [HTML](../../../lecture12.html) | [PDF](../../../lecture12.pdf) |
| シラバス | [QMD](../../../マクロ経済学B_シラバス案.qmd)・[Markdown](../../../マクロ経済学B_シラバス案.md) | [HTML](../../../マクロ経済学B_シラバス案.html) | [PDF](../../../マクロ経済学B_シラバス案.pdf) |
