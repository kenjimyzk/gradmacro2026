# Clean direct-R execution of unchanged lecture chunks, in a dedicated directory.
# Invoke from this directory: Rscript --vanilla run-clean.R
repo <- normalizePath("../../../..")
source("scripts/japanese-graphics.R")
lib <- course_graphics_library()
if (dir.exists(lib)) .libPaths(c(lib, .libPaths()))
graphics_info <- course_japanese_graphics()
print(graphics_info)
for (lecture in c("lecture05", "lecture08")) {
  extracted <- paste0(lecture, "-chunks.R")
  knitr::purl(file.path(repo, paste0(lecture, ".qmd")),
              output = extracted, documentation = 0L, quiet = TRUE)
  parse(extracted)
  cairo_pdf(paste0(lecture, "-clean.pdf"),
            width = if (lecture == "lecture05") 6.5 else 8,
            height = if (lecture == "lecture05") 4 else 6.3,
            family = graphics_info$family)
  env <- new.env(parent = globalenv())
  sys.source(extracted, envir = env)
  dev.off()
  if (lecture == "lecture05") {
    result <- data.frame(tau = env$tau, normalized_revenue = env$tax_revenue)
    write.csv(result, "lecture05-curve.csv", row.names = FALSE)
    stopifnot(all.equal(read.csv("lecture05-curve.csv"), result,
                        check.attributes = FALSE) == TRUE)
    cat("L05 peak:", env$tau_star, "normalized revenue:", env$tax_revenue_star, "\n")
  } else {
    result <- do.call(rbind, lapply(names(env$impact), function(nm) {
      data.frame(shock = nm, t(env$impact[[nm]]), row.names = NULL)
    }))
    write.csv(result, "lecture08-impact.csv", row.names = FALSE)
    print(result)
    # Independent linear solve of the original 3-equation system.
    checks <- lapply(names(env$impact), function(nm) {
      rho <- env$rhos[nm]
      nat <- switch(nm, monetary = 0,
        technology = -env$tilde_gamma * (1-rho) * env$zeta_a,
        government = env$tilde_gamma * (1-rho) * (1-env$zeta_g))
      mat <- rbind(c(env$tilde_gamma*(1-rho), 0, 1),
                   c(-env$kappa_x, 1-env$beta*rho, 0),
                   c(0, -(env$phi-rho), 1))
      rhs <- c(nat, 0, if (nm == "monetary") -1 else 0)
      direct <- solve(mat, rhs)
      data.frame(shock = nm,
                 max_closed_form_error = max(abs(direct-env$impact[[nm]])),
                 max_equation_residual = max(abs(mat %*% env$impact[[nm]]-rhs)))
    })
    checks <- do.call(rbind, checks)
    print(checks)
    write.csv(checks, "lecture08-independent-linear-check.csv", row.names = FALSE)
    stopifnot(max(checks$max_closed_form_error) < 1e-12,
              max(checks$max_equation_residual) < 1e-12)
  }
}
cat("Clean sequential direct R checks passed.\n")
print(sessionInfo())
