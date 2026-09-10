# 第5〜10回 参考文献修正の対応一覧

2026-09-09。ユーザーの「レポートをもとにすべて修正」という承認に基づき、担当の `lecture05.qmd`〜`lecture10.qmd` を修正した。数式・計算コード・演習・補論の内容は維持した。レンダーは統合担当へ引き継ぐ。

| 監査項目 | 修正内容 | 修正後の箇所 |
|---|---|---|
| 第5回の文献への導線 | Baxter–King に著者公開PDF、Aiyagari et al.、Leeper、Trabandt–Uhlig に DOI を追加 | `lecture05.qmd:728–731` |
| 第5回の財政・税収文献の位置づけ | Baxter–King は資本蓄積を含む財政動学、Trabandt–Uhlig は成長モデルによる定量的ラッファーカーブとして注記 | `lecture05.qmd:728,731` |
| 第5回 Galí の対象 | 第3章の基本NKモデルを第8回への準備として案内。政府支出モデルの直接の導出元とは書かない | `lecture05.qmd:724` |
| 第6回の原典への導線 | Dixit–Stiglitz に AEA 公開PDF、Blanchard–Kiyotaki に JSTOR、Spence に DOI を追加 | `lecture06.qmd:589–595` |
| 第6回 Rotemberg–Woodford | 出版社で正式 DOI `10.1086/654340` を確認して追加。現行本文頁297–346を維持し、金融政策の定量分析への発展と注記 | `lecture06.qmd:596` |
| 第6回 Galí | 第3章を指定 | `lecture06.qmd:591` |
| 第7回 Calvo–Rotemberg 対応 | 効率的定常状態の役割について Lombardo–Vestin (2008) の本文参照と発展文献を追加 | `lecture07.qmd:119,643` |
| 第7回の原典・教科書 | Galí 第3章の Calvo 型導出と、Rotemberg の価格調整費用の役割を注記 | `lecture07.qmd:631,642` |
| 第8回の教科書・一般解法 | Galí 第3章を指定。Schmitt-Grohé–Uribe は一般DSGEモデルの二次近似へ進む発展文献と注記 | `lecture08.qmd:1033,1045` |
| 第9回 divine coincidence | Blanchard–Galí (2007) の本文参照と発展文献を追加。実質賃金硬直性の原典であることを明示 | `lecture09.qmd:86,780` |
| 第9回 Calvo–Rotemberg 厚生 | Lombardo–Vestin (2008) の本文参照と発展文献を追加。既存の効率的定常状態・局所近似の限定を維持 | `lecture09.qmd:224,781` |
| 第9回 Galí | 第4・5章を指定 | `lecture09.qmd:769` |
| 第10回 EHL と Rotemberg | EHL は Calvo 型価格・賃金契約の政策トレードオフ、Rotemberg は価格費用の原典と注記。本文でも価格費用の考え方を賃金設定へ拡張することを説明 | `lecture10.qmd:316,1077–1078` |
| 第10回 Galí | 第6章の Calvo 型価格・賃金モデルを指定 | `lecture10.qmd:1079` |
| 第10回の賃金設定比較・訂正 | Born–Pfeifer (2020) と2025年 Corrigendum を発展文献に追加。数値結果利用時の併読、コードの指数逆転と表4〜6の訂正、定性的結果の維持を注記 | `lecture10.qmd:316,1088–1089` |

## 一次情報の追加確認

前回監査で確認済みの文献情報を用いた。第6回のリンク補完については、この修正時に次の一次情報を追加確認した。

- Dixit–Stiglitz (1977)：[AEA 公開原著PDF](https://www.aeaweb.org/aer/top20/67.3.297-308.pdf)の題名・著者、12ページの原著を取得。
- Blanchard–Kiyotaki (1987)：[JSTOR の当該巻目次](https://www.jstor.org/stable/i331470)が題名・著者・647–666頁と [stable/1814537](https://www.jstor.org/stable/1814537) を掲載。
- Rotemberg–Woodford (1997)：[出版社の論文ページ](https://www.journals.uchicago.edu/doi/10.1086/654340)が題名・著者・1997年・第12巻・297–346頁・DOIを確認できる。
- Born–Pfeifer (2025)：[Cambridge の訂正本文](https://www.cambridge.org/core/journals/macroeconomic-dynamics/article/new-keynesian-wage-phillips-curve-calvo-vs-rotemberg-corrigendum/5070C1EC70E46FA2D56E91B2D72143A4)を前回監査で取得し、*Macroeconomic Dynamics*, 29, **e85**、2025年、DOI `10.1017/S1365100525000161` を確認済み。本文は合成インフレ指数のコード上の重み逆転、表4〜6の訂正、定性的結果の維持を明記している。

Lombardo–Vestin、Blanchard–Galí、Born–Pfeifer と訂正は、[前回の一次資料照合記録](../reference-audit/l05-l10.md)に基づく。Born–Pfeifer はオンライン先行公開年2018ではなく、巻号付き刊行年2020で統一した。

## 検証

- **verified**：6ファイルの差分を通読し、本文の引用案内・文献・読書範囲だけの変更と確認。
- **verified**：修正前バックアップとの比較で、YAML、全 fenced blocks、表示数式、コードブロック外のインライン数式、演習開始以降の全文、見出し列の全36チェックが一致。[保全結果](l05-l10-preservation.json)。
- **verified**：担当6ファイルに対する `git -c core.fsmonitor=false diff --check` が成功。
- **not run**：HTML/PDFレンダー、画面・PDF目視、計算の再実行。この分担では実施せず、統合担当の検証へ引き継ぐ。

参考文献は第7回に1項目、第9回に2項目、第10回に2項目を追加。他の担当ファイルや生成物は変更していない。
