# 第5・9回の R 図を再生成する

リポジトリのルートを作業ディレクトリとして実行します。Quarto、R、PDF 用の LuaLaTeX が必要です。図は R に組み込まれた Cairo デバイスを使い、HTML には PNG、PDF にはフォントを埋め込んだ PDF を生成します。`showtext`、`sysfonts`、個人のフォントファイルへの絶対パスは使いません。

## 準備

```sh
Rscript --vanilla scripts/setup-graphics.R
Rscript --vanilla scripts/check-graphics.R
```

最初のコマンドは、不足する `knitr`、`rmarkdown`、`systemfonts >= 1.3.0` だけを `scripts/.R-library/<R版>/<platform>/` に導入します。既存のライブラリや R の起動設定は変更しません。既に要件を満たしている場合は何も導入しません。ソース版パッケージのビルド環境がない場合は、使用する OS と R に対応した CRAN バイナリを利用してください。

次のコマンドは一時フォルダに確認用 PDF・PNG と `environment.txt` を生成し、その場所を表示します。両方を開き、日本語、負号、ラベルの切れを確認してください。処理が終了したことだけでは画面表示の確認にはなりません。保存先を残したい場合は第1引数に指定します。

```sh
Rscript --vanilla scripts/check-graphics.R /tmp/gradmacro-graphics-check
```

## フォントと Cairo

導入済みの Noto Sans CJK JP、Noto Sans JP、Hiragino Sans、Yu Gothic、Yu Gothic UI、Meiryo、IPAexGothic、IPAGothic の順で検索し、図に使う日本語の字形が通常・太字の両方にあるフォントを選びます。特定の OS に依存するフォントファイルのパスは保存しません。候補が見つからない場合や Cairo に対応しない R では、文字化けした図を生成せずに停止します。

日本語フォントがない環境では、[Google Fonts の Noto Sans JP](https://fonts.google.com/noto/specimen/Noto+Sans+JP) 等を OS の通常の方法で導入し、R を再起動してください。フォント本体はこのリポジトリに同梱していません。別の導入済みフォントを選ぶ場合は、その **family 名**をレンダーする R プロセスの環境変数に指定します。

```sh
GRADMACRO_JP_FONT="Noto Sans JP" Rscript --vanilla scripts/render-lecture.R lecture05.qmd --to pdf
```

R コンソールからは `Sys.setenv(GRADMACRO_JP_FONT = "Noto Sans JP")` と指定できます。利用可能な family 名は `unique(systemfonts::system_fonts()$family)` で確認します。指定名が未導入の場合にも停止します。

`capabilities("cairo")` と `capabilities("png")` がともに `TRUE` である R を使ってください。Cairo の可用性は R のビルドとシステムに依存します。macOS では環境によって XQuartz が必要です。詳細は [R の Cairo デバイス公式マニュアル](https://stat.ethz.ch/R-manual/R-devel/library/grDevices/html/cairo.html)を参照してください。字形の検査には [systemfonts の glyph_info](https://systemfonts.r-lib.org/reference/glyph_info.html) を使います。

## 再生成

```sh
Rscript --vanilla scripts/render-lecture.R lecture05.qmd --to html
Rscript --vanilla scripts/render-lecture.R lecture05.qmd --to pdf
Rscript --vanilla scripts/render-lecture.R lecture09.qmd --to html
Rscript --vanilla scripts/render-lecture.R lecture09.qmd --to pdf
```

`render-lecture.R` は、このリポジトリの R ライブラリを子プロセスへ渡して `quarto render` を実行します。これにより `knitr`・`rmarkdown` をプロジェクト内に導入した場合も使えます。必要なパッケージが通常の R ライブラリに揃っている環境では、従来どおり `quarto render lecture05.qmd --to pdf` 等でも実行できます。

HTML で展開する図のコードは、文書先頭の共通設定で作る `jp_graphics` を使います。図だけを別の R セッションで実行する場合は、ルートディレクトリで次を先に実行し、続けて図のコードを実行してください。

```r
source("scripts/japanese-graphics.R")
jp_graphics <- course_japanese_graphics()
grDevices::cairo_pdf("figure-check.pdf", width = 8, height = 4.8,
                    family = jp_graphics$family)
```

図のコードの実行後に `grDevices::dev.off()` を実行すると `figure-check.pdf` を開けます。第5回の元の図寸法を使う場合は `width = 6.5, height = 4` に変更します。

生成後は本文の図でも日本語・数式・凡例を確認してください。PDF のフォントとテキストを調べる補助コマンドとして、Poppler の `pdffonts` と `pdftotext` も利用できます。フォント名・字形の検査は R 側の確認であり、Cairo の最終出力の目視を代替するものではありません。

2026-09-09 のローカル確認環境は macOS arm64、R 4.6.1、knitr 1.51、rmarkdown 2.31、systemfonts 1.3.2、Hiragino Sans、Cairo 対応 R です。他の OS での実行は未検証です。依存は最低要件を指定しており、この手順は全 OS・全バージョンで画像の画素単位の一致を保証するものではありません。
