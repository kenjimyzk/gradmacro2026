# Only missing/incompatible packages are installed, into this repository.
source("scripts/japanese-graphics.R")
local_library <- course_graphics_library()
if (dir.exists(local_library)) .libPaths(c(local_library, .libPaths()))
requirements <- c(knitr = "1.0", rmarkdown = "1.0", systemfonts = "1.3.0")
missing <- names(requirements)[!vapply(names(requirements), function(pkg) {
  requireNamespace(pkg, quietly = TRUE) &&
    utils::packageVersion(pkg) >= requirements[[pkg]]
}, logical(1))]
if (length(missing)) {
  dir.create(local_library, recursive = TRUE, showWarnings = FALSE)
  utils::install.packages(missing, lib = local_library, repos = "https://cloud.r-project.org")
} else {
  message("必要な R パッケージは導入済みです。インストールは行いません。")
}
message("環境確認: Rscript scripts/check-graphics.R")
