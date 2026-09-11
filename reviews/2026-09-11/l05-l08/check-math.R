# Independent checks of nonlinear allocations, welfare curvature and tax incidence.
out <- "reviews/2026-09-11/l05-l08"
alpha <- .4; gamma <- 1; varphi <- 1; GY <- .2
N0 <- ((1-alpha)*(1-GY)^(-gamma))^(1/(varphi+alpha+gamma*(1-alpha)))
Y0 <- N0^(1-alpha); G0 <- GY*Y0; C0 <- Y0-G0
alloc <- function(g) {
  G <- G0 + g*Y0
  N <- uniroot(function(N) N^(varphi+alpha)*(N^(1-alpha)-G)^gamma-(1-alpha),
               c(G^(1/(1-alpha))+1e-5, 10), tol=1e-13)$root
  Y <- N^(1-alpha)
  c(n=log(N/N0),y=log(Y/Y0),c=log((Y-G)/C0),w=-alpha*log(N/N0))
}
h <- 1e-5
fd <- (alloc(h)-alloc(-h))/(2*h)
zeta_g <- gamma*(1-alpha)/((1-GY)*(alpha+varphi)+gamma*(1-alpha))
exact <- c(n=zeta_g/(1-alpha),y=zeta_g,c=(zeta_g-1)/(1-GY),w=-alpha*zeta_g/(1-alpha))
write.csv(data.frame(variable=names(fd), nonlinear_derivative=fd, lecture_coefficient=exact,
                     error=fd-exact), file.path(out,"l05-nonlinear-check.csv"),row.names=FALSE)
stopifnot(max(abs(fd-exact))<1e-7)

# CES: log MRTS = constant + (rho-1) log(X1/X2).
rho <- 5/6
ces <- data.frame(rho=rho, derivative_written_definition=1/(rho-1),
                  positive_substitution_elasticity=-1/(rho-1))
write.csv(ces,file.path(out,"l06-ces-sign.csv"),row.names=FALSE)

# A proportional tax on net economic profit scales the entire objective.
psi <- 6; A <- 1.2; W <- .7
profit <- function(s) s*s^(-psi)-W*(s^(-psi)/A)^(1/(1-alpha))
profit_opt <- sapply(c(0,.2,.7),function(tau) optimize(function(s) (1-tau)*profit(s),
                                                     c(.1,3), maximum=TRUE,tol=1e-12)$maximum)
write.csv(data.frame(net_profit_tax=c(0,.2,.7), optimal_relative_price=profit_opt),
          file.path(out,"l06-net-profit-tax-counterexample.csv"),row.names=FALSE)
stopifnot(diff(range(profit_opt))<1e-7)

# L08: numerical welfare Hessian from the nonlinear resource and production equations.
alpha <- .33; gamma <- 1; varphi <- 1; GY <- .2; eta <- 80
N0 <- ((1-alpha)*(1-GY)^(-gamma))^(1/(varphi+alpha+gamma*(1-alpha)))
Y0 <- N0^(1-alpha); G0 <- GY*Y0; C0 <- Y0-G0
util <- function(y, pi) {
  Y <- Y0*exp(y)
  C <- Y*(1-eta/2*(exp(pi)-1)^2)-G0
  N <- Y^(1/(1-alpha))
  log(C)-N^(1+varphi)/(1+varphi)
}
h <- 1e-4
scale <- C0^(-gamma)*Y0
curvature_y <- -(util(h,0)-2*util(0,0)+util(-h,0))/h^2/scale
curvature_pi <- -(util(0,h)-2*util(0,0)+util(0,-h))/h^2/scale
expected_y <- gamma/(1-GY)+(varphi+alpha)/(1-alpha)
write.csv(data.frame(term=c("output_gap","inflation"),
                     nonlinear_curvature=c(curvature_y,curvature_pi),
                     lecture_coefficient=c(expected_y,eta)),
          file.path(out,"l08-welfare-hessian.csv"),row.names=FALSE)
stopifnot(abs(curvature_y-expected_y)<1e-5,abs(curvature_pi-eta)<1e-4)
cat("Independent nonlinear derivatives, CES sign, net-profit-tax example and welfare curvature completed.\n")
