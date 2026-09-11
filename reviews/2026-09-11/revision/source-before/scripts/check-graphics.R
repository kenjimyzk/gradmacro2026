# Usage: Rscript --vanilla scripts/check-graphics.R [output-directory]
source("scripts/japanese-graphics.R")
info <- course_japanese_graphics()
args <- commandArgs(trailingOnly = TRUE)
output <- if (length(args)) args[[1]] else tempfile("gradmacro-graphics-")
dir.create(output, recursive = TRUE, showWarnings = FALSE)
output <- normalizePath(output, mustWork = TRUE)
draw_check <- function() {
  par(mar = c(4.5, 4.5, 4.5, 1), family = info$family)
  plot(0:4, c(0, 1, .5, -.5, 0), type = "l", xlab = "期",
       ylab = "産出ギャップ")
  title(main = "日本語の描画確認：裁量・タイムレス", line = 2.5)
  mtext("労働所得税率・正規化した税収・価格インフレ率", side = 3, line = .8, cex = .9)
}
pdf_path <- file.path(output, "japanese-font-check.pdf")
png_path <- file.path(output, "japanese-font-check.png")
grDevices::cairo_pdf(pdf_path, width = 8, height = 4.5, family = info$family)
draw_check()
invisible(grDevices::dev.off())
grDevices::png(png_path, width = 1200, height = 675, res = 150,
              type = "cairo", family = info$family)
draw_check()
invisible(grDevices::dev.off())
capture.output(list(R = R.version.string, cairo = capabilities("cairo"),
                    graphics = info, packages = sessionInfo()),
               file = file.path(output, "environment.txt"))
cat("PDF:", pdf_path, "\nPNG:", png_path, "\nFont:", info$family,
    "\n両ファイルを開き、日本語・負号・ラベルの切れがないことを確認してください。\n")
