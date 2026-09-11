#| label: setup-japanese-graphics
#| include: false
source("scripts/japanese-graphics.R")
jp_graphics <- configure_course_graphics()

print(jp_graphics)
png("lecture09-clean.png",width=1600,height=960,res=200,type="cairo",family=jp_graphics$family)
#| label: fig-lecture09-discretion-timeless-irf
#| fig-cap: "コストプッシュショックに対する裁量政策とタイムレス・パースペクティブの動学的反応の比較"
#| fig-width: 8
#| fig-height: 4.8
#| echo: !expr knitr::is_html_output()
#| code-fold: true
#| code-summary: "Rコードを表示"

font_family <- jp_graphics$family

beta <- 0.99
kappa_x <- 0.08
omega_p <- 20
rho_u <- 0.7
T <- 40

u <- rho_u^(0:T)

# 裁量政策
den <- (1 - beta * rho_u) + kappa_x^2 * omega_p
pi_D <- 1 / den * u
x_D <- -kappa_x * omega_p / den * u

# タイムレス・パースペクティブの有限期間近似
B <- 1 + beta + kappa_x^2 * omega_p
A <- matrix(0, nrow = T + 1, ncol = T + 1)
b <- -kappa_x * omega_p * u
x_lag <- 0

for (t in 1:(T + 1)) {
  A[t, t] <- B
  if (t < T + 1) A[t, t + 1] <- -beta
  if (t > 1) {
    A[t, t - 1] <- -1
  } else {
    b[t] <- b[t] + x_lag
  }
}

x_C <- as.vector(solve(A, b))
pi_C <- -1 / (kappa_x * omega_p) * c(x_C[1] - x_lag, diff(x_C))

h <- 0:T
col_discretion <- "#2F6FBE"
col_timeless <- "#D45D48"

op <- par(
  mfrow = c(1, 2),
  mar = c(4.1, 4.1, 3.0, 1.0),
  las = 1,
  family = font_family
)

plot(
  h, x_D,
  type = "n",
  ylim = range(c(0, x_D, x_C)),
  xlab = "経過期間（期）",
  ylab = "厚生上の産出ギャップ",
  main = "産出ギャップの反応"
)
grid()
abline(h = 0, lty = 2, col = "gray55")
lines(h, x_D, lwd = 2.4, col = col_discretion)
lines(h, x_C, lwd = 2.4, col = col_timeless)
legend(
  "bottomright",
  legend = c("裁量政策", "タイムレス"),
  col = c(col_discretion, col_timeless),
  lty = 1,
  lwd = 2.4,
  bty = "n"
)

plot(
  h, pi_D,
  type = "n",
  ylim = range(c(0, pi_D, pi_C)),
  xlab = "経過期間（期）",
  ylab = "価格インフレ率",
  main = "価格インフレ率の反応"
)
grid()
abline(h = 0, lty = 2, col = "gray55")
lines(h, pi_D, lwd = 2.4, col = col_discretion)
lines(h, pi_C, lwd = 2.4, col = col_timeless)
legend(
  "topright",
  legend = c("裁量政策", "タイムレス"),
  col = c(col_discretion, col_timeless),
  lty = 1,
  lwd = 2.4,
  bty = "n"
)

par(op)

dev.off()
write.csv(data.frame(h,u,x_D,pi_D,x_C,pi_C),"lecture09-irf.csv",row.names=FALSE)
stopifnot(max(abs(A %*% x_C-b)) < 1e-10)
cat("\nMAX_LINEAR_RESIDUAL ",max(abs(A %*% x_C-b)),"\n")
print(sessionInfo())
