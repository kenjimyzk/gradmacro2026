beta <- 0.99
gamma <- 1
varphi <- 1
alpha <- 0.33
GY <- 0.2
psi <- 6
eta <- 80
phi <- 1.5
MC <- 1

rho_m <- 0.5
rho_a <- 0.8
rho_g <- 0.8

tilde_gamma <- gamma / (1 - GY)
tilde_varphi <- (varphi + alpha) / (1 - alpha)
zeta_a <- (tilde_varphi + 1) / (tilde_varphi + tilde_gamma)
zeta_g <- tilde_gamma / (tilde_varphi + tilde_gamma)
kappa_x <- MC * (tilde_gamma + tilde_varphi) * psi / eta

kappa_i <- function(rho) kappa_x / (1 - beta * rho)
omega_i <- function(rho) {
  kappa_rho <- kappa_i(rho)
  tilde_gamma * (1 - rho) /
    (kappa_rho * (phi - rho) + tilde_gamma * (1 - rho))
}

kappa_m <- kappa_i(rho_m)
kappa_a <- kappa_i(rho_a)
kappa_g <- kappa_i(rho_g)

Omega <- 1 / (kappa_m * (phi - rho_m) + tilde_gamma * (1 - rho_m))
Omega_m <- tilde_gamma * (1 - rho_m) * Omega
Omega_a <- omega_i(rho_a)
Omega_g <- omega_i(rho_g)

impact <- list(
  monetary = c(
    x = Omega,
    pi = kappa_m * Omega,
    r = -Omega_m
  ),
  technology = c(
    x = -zeta_a * Omega_a,
    pi = -kappa_a * zeta_a * Omega_a,
    r = -(phi - rho_a) * kappa_a * zeta_a * Omega_a
  ),
  government = c(
    x = (1 - zeta_g) * Omega_g,
    pi = kappa_g * (1 - zeta_g) * Omega_g,
    r = (phi - rho_g) * kappa_g * (1 - zeta_g) * Omega_g
  )
)

rhos <- c(monetary = rho_m, technology = rho_a, government = rho_g)
h <- 0:20
shock_names <- c(
  monetary = "Monetary easing shock",
  technology = "Technology shock",
  government = "Government spending shock"
)
var_names <- c(x = "Output gap", pi = "Inflation", r = "Ex ante real rate")
var_cols <- c(x = "#2F6FBE", pi = "#D45D48", r = "#379B55")

op <- par(mfrow = c(3, 3), mar = c(3.0, 3.4, 2.5, 0.8), oma = c(2.0, 0.5, 1.0, 0.2), las = 1)

for (shock in names(impact)) {
  for (v in names(var_names)) {
    response <- impact[[shock]][v] * rhos[shock]^h
    y_lim <- range(c(0, response))
    pad <- 0.08 * diff(y_lim)
    if (pad == 0) pad <- 0.1
    plot(
      h, response,
      type = "n",
      xlab = "",
      ylab = "",
      main = paste(shock_names[shock], var_names[v], sep = "\n"),
      ylim = y_lim + c(-pad, pad),
      cex.main = 0.95
    )
    grid()
    abline(h = 0, lty = 2, col = "gray55")
    lines(h, response, lwd = 2.3, col = var_cols[v])
  }
}

mtext("Horizon (model periods)", side = 1, outer = TRUE, line = 0.5)
par(op)
