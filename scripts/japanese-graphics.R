# Run from the repository root. No persistent R options or global libraries change.
course_graphics_library <- function() {
  r_minor <- strsplit(R.version$minor, ".", fixed = TRUE)[[1]][1]
  file.path("scripts", ".R-library", paste(R.version$major, r_minor, sep = "."),
            R.version$platform)
}

course_japanese_graphics <- function() {
  local_library <- course_graphics_library()
  if (dir.exists(local_library)) .libPaths(c(local_library, .libPaths()))
  help <- "リポジトリのルートで Rscript scripts/setup-graphics.R を実行してください。詳細: scripts/README-graphics.md"
  if (!requireNamespace("systemfonts", quietly = TRUE) ||
      utils::packageVersion("systemfonts") < "1.3.0") {
    stop("systemfonts >= 1.3.0 が必要です。", help, call. = FALSE)
  }
  if (!isTRUE(capabilities("cairo")) || !isTRUE(capabilities("png"))) {
    stop("Cairo と PNG に対応した R が必要です。詳細: scripts/README-graphics.md",
         call. = FALSE)
  }

  requested <- Sys.getenv("GRADMACRO_JP_FONT", unset = "")
  candidates <- if (nzchar(requested)) requested else c(
    "Noto Sans CJK JP", "Noto Sans JP", "Hiragino Sans", "Yu Gothic",
    "Yu Gothic UI", "Meiryo", "IPAexGothic", "IPAGothic"
  )
  installed <- unique(systemfonts::system_fonts()$family)
  candidates <- candidates[candidates %in% installed]
  # The characters used in the two lecture figures, including bold titles.
  labels <- "労働所得税率正規化した収最大裁量タイムレス価格インフレ産出ギャップ期のラッファーカーブ"
  for (family in candidates) {
    indices <- c(
      systemfonts::glyph_info(labels, family = family)$index,
      systemfonts::glyph_info(labels, family = family, weight = "bold")$index
    )
    if (all(indices != 0L)) {
      return(list(family = family,
                  font = systemfonts::font_info(family = family)[, c("family", "path", "index")],
                  systemfonts = as.character(utils::packageVersion("systemfonts"))))
    }
  }
  stop(
    "図の日本語を表示できるフォントが見つかりません。",
    if (nzchar(requested)) paste0("指定: ", requested, "。") else "",
    "Noto Sans JP 等を OS に導入するか、導入済みの日本語フォントの family 名を ",
    "GRADMACRO_JP_FONT に指定してください。詳細: scripts/README-graphics.md",
    call. = FALSE
  )
}

configure_course_graphics <- function() {
  info <- course_japanese_graphics()
  if (!requireNamespace("knitr", quietly = TRUE)) {
    stop("Quarto の R 文書を描画するには knitr が必要です。scripts/README-graphics.md を参照してください。",
         call. = FALSE)
  }
  if (knitr::is_latex_output()) {
    knitr::opts_chunk$set(dev = "cairo_pdf", dev.args = list(family = info$family))
  } else {
    knitr::opts_chunk$set(dev = "png", dev.args = list(type = "cairo", family = info$family))
  }
  info
}
