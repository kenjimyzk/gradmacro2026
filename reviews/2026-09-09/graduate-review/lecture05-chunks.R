source("scripts/japanese-graphics.R")
info <- course_japanese_graphics()
grDevices::cairo_pdf("/Users/kenjimyzk/work/gradmacro2026/reviews/2026-09-09/graduate-review/lecture05-r.pdf", width=8, height=4.8, family=info$family)
#| label: setup-japanese-graphics
#| include: false
source("scripts/japanese-graphics.R")
jp_graphics <- configure_course_graphics()


#| label: fig-laffer-curve
#| fig-cap: "労働所得税のラッファーカーブ。$\\alpha=0.4$、$\\gamma=\\varphi=1$。縦軸は正規化した税収 $TX/\\mathcal A$。赤い破線は最大税収率 $\\tau_N^*=0.769$ を示す。"
#| fig-width: 6.5
#| fig-height: 4
#| fig-pos: H
#| echo: !expr knitr::is_html_output()
#| code-fold: true
#| code-summary: "Rコードを表示"

alpha <- 0.4
gamma <- 1
varphi <- 1

font_family <- jp_graphics$family

denom <- varphi + alpha + gamma * (1 - alpha)
vartheta <- (1 - alpha) / denom
tau_star <- 1 / (1 + vartheta)

tau <- seq(0, 1, length.out = 501)
tax_revenue <- tau * (1 - tau)^vartheta
tax_revenue_star <- tau_star * (1 - tau_star)^vartheta

op <- par(mar = c(4.5, 4.5, 2.5, 1), las = 1, family = font_family)
plot(
  tau, tax_revenue,
  type = "n",
  xlim = c(0, 1),
  ylim = c(0, max(tax_revenue) * 1.08),
  xlab = expression("労働所得税率 " * tau[N]),
  ylab = "正規化した税収",
  main = "労働所得税のラッファーカーブ"
)
grid()
lines(tau, tax_revenue, lwd = 2, col = "#1F77B4")
abline(v = tau_star, lty = 2, lwd = 1.5, col = "#D62728")
points(tau_star, tax_revenue_star, pch = 19, col = "#D62728")
text(
  tau_star - 0.03,
  tax_revenue_star,
  labels = sprintf("最大税率 = %.3f", tau_star),
  pos = 2,
  col = "#D62728"
)
par(op)


grDevices::dev.off()
print(sessionInfo())
