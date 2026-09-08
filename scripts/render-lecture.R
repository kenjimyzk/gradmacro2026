# Forward Quarto render arguments and expose the repository library to its R process.
# Usage: Rscript --vanilla scripts/render-lecture.R lecture05.qmd --to pdf
source("scripts/japanese-graphics.R")
local_library <- course_graphics_library()
if (dir.exists(local_library)) .libPaths(c(local_library, .libPaths()))
Sys.setenv(R_LIBS = paste(.libPaths(), collapse = .Platform$path.sep))
args <- commandArgs(trailingOnly = TRUE)
if (!length(args)) stop("対象の .qmd と Quarto のオプションを指定してください。", call. = FALSE)
quarto <- Sys.which("quarto")
if (!nzchar(quarto)) stop("Quarto を導入し PATH を確認してください。", call. = FALSE)
status <- system2(quarto, c("render", vapply(args, shQuote, character(1))))
quit(status = status)
