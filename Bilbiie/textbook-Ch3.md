## Heterogeneous Agent Macroeconomics

## A Tractable New Keynesian Framework

Florin O. Bilbiie

University of Cambridge & CEPR

Forthcoming, MIT Press

First version 2019, this version November 2025

1

#### Chapter 3

Preliminary and Incomplete. Comments Requested

© Florin O. Bilbiie 2019

<sup>1</sup>Bsed on notes used to teach advanced mini-courses over the last years at the International Monetary Fund, European Central Bank Research Department, Norges Bank, Paris School of Economics (Summer School and APE program), Brown University, HEC Lausanne, Bonn Graduate School of Economics, Goethe University, and Cambridge. I thank Sean Lavender, who provided excellent RA work and help with transcribing the lectures and drafting. TBC

# Chapter 3: A Benchmark Two-Agent (TANK) Model: Both Keynesian and General-Equilibrium

In this chapter, we will consider a Two-Agent New Keynesian model (TANK) based on the analytical framework developed by Bilbiie (2008) and extended in Bilbiie (2020). Importantly, this model will display two key features which were absent in the RANK model discussed in the previous chapter. Firstly, the TANK model will be more Keynesian, exhibiting higher fiscal multipliers and agents who are more responsive to changes in income. Secondly, the model will display more general equilibrium amplification of shocks and will allocate direct intertemporal substitution a smaller role in generating the response to monetary policy. A discussion of the broader TANK literature concludes.

#### Two-Agent New Keynesian Model

The TANK model features two types of household with total unit mass. A fraction λ of the households are hand-to-mouth (denoted by H). These households are excluded from asset markets and consume all of their income from transfers and supplying labour.

$$C_t^H = W_t N_t^H + \mathcal{T}_t^H = Y_t^H$$

The remaining 1 − λ households are savers (denoted by S). These households have full access to complete financial markets. As in the RANK model, savers supply labour and access a full set of state-contingent securities. They also hold shares in (and receive profits from) the monopolistically competitive firms. To isolate the role of income inequality and profits, assume that the assets are priced and held but not traded. Asset market clearing (the 1 − λ savers must own all of the shares) means that the budget constraint of the saver is given by:

$$C_t^S = W_t N_t^S + \frac{1}{1 - \lambda} D_t + \mathcal{T}_t^S = Y_t^S.$$

The government implements a simple redistribution scheme in which profits are taxed at rate τ <sup>D</sup> and rebated lump-sum to H households. Type H households therefore receive a transfer of:

$$\mathcal{T}_t^H = \frac{\tau^D}{\lambda} D_t.$$

In addition, the government implements the optimal New Keynesian sales subsidy (funded by taxing firms lump-sum) such that firms implement marginal cost pricing. In steady state, this achieves D = 0 and ensures that both types of households have equal steady state consumption C <sup>H</sup> = C <sup>S</sup> = C. Loglinearising the firm's profit function around the D = 0 steady state shows that profits vary inversely with the real wage:

$$d_t = -w_t$$

where d<sup>t</sup> ≡ ln <sup>D</sup><sup>t</sup> Y . As real wages are procyclical in the model, profits will be procyclical (a common feature of most New Keynesian models).

While the model introduces heterogeneity in earnings and income, assume that both types of households have identical separable preferences over consumption and leisure. The intertemporal elasticity of substitution and the Frisch elasticity are given by:

$$\sigma^{-1} \equiv -\frac{U_{CC}^{j}}{U_{C}^{j}} C^{j}$$
$$\varphi \equiv \frac{U_{NN}^{j}}{U_{N}^{j}} N^{j}.$$

Loglinearising the intratemporal first order conditions therefore yields the following expression for the labour supply of each household type:

$$\varphi n_t^j = w_t - \sigma^{-1} c_t^j.$$

As the elasticities are identical, this relationship also holds in the aggregate:

$$\varphi n_t = w_t - \sigma^{-1} c_t.$$

Combining this with goods market clearing  $y_t = c_t = n_t$  gives the real wage as a function of aggregate consumption:

$$w_t = (\varphi + \sigma^{-1})c_t.$$

The equilibrium conditions and their loglinearised counterparts are summarised in the table below.

| Description                | Equilibrium Condition                                        | Loglinearised                                         |
|----------------------------|--------------------------------------------------------------|-------------------------------------------------------|
| S Euler Equation           | $U_C(C_t^S) = \beta R_t E_t [U_C(C_{t+1}^S)]$                | $c_t^s = E_t c_{t+1}^S - \sigma r_t$                  |
| S Intratemporal Optimality | $\frac{W_t}{P_t}U_C(C_t^S) = -U_N(N_t^S)$                    | $\varphi n_t^S = w_t - \sigma^{-1} c_t^S$             |
| H Intratemporal Optimality | $\frac{W_t}{P_t}U_C(C_t^H) = -U_N(N_t^H)$                    | $\varphi n_t^H = w_t - \sigma^{-1} c_t^H$             |
| H Budget Constraint        | $C_t^H = \frac{W_t}{P_t} N_t^H + \frac{\tau^D}{\lambda} D_t$ | $c_t^H = w_t + n_t^H + \frac{\tau^D}{\lambda} d_t$    |
| Profit Function            | $D_t = (1 + \tau^S)Y_t - \frac{W_t}{P_t}N_t - T_t^F$         | $d_t = -w_t$                                          |
| Goods Market Clearing      | $Y_t = C_t \equiv \lambda C_t^H + (1 - \lambda)C_t^S$        | $y_t = c_t \equiv \lambda c_t^H + (1 - \lambda)c_t^S$ |
| Labour Market Clearing     | $N_t = \lambda N_t^H + (1 - \lambda) N_t^S$                  | $n_t = \lambda n_t^H + (1 - \lambda) n_t^S$           |
| Production                 | $Y_t = N_t$                                                  | $y_t = n_t$                                           |
|                            |                                                              |                                                       |

Table 1: TANK equilibrium conditions.

#### Deriving AggregateD Demand in TANK

We can now use the loglinearised equilibrium conditions to derive the key equations of the TANK model which express individual consumption as functions of aggregate income. Begin with the budget constrained for households for type H:

$$c_t^H = w_t + n_t^H + \frac{\tau^D}{\lambda} d_t.$$

Replace labour supply and profits using:

$$\varphi n_t^H = w_t - \sigma^{-1} c_t^H$$
$$d_t = -w_t.$$

This gives:

$$(1 + (\varphi \sigma)^{-1})c_t^H = (1 - \frac{\tau^D}{\lambda} + \varphi^{-1})w_t.$$

Using aggregate labour supply and the goods market clearing condition (y<sup>t</sup> = c<sup>t</sup> = nt), we obtain:

$$c_t^H = y_t^H = \chi y_t$$
where  $\chi \equiv 1 + \varphi (1 - \frac{\tau^D}{\lambda})$ .

The parameter χ represents the elasticity of the hand-to-mouth household's consumption to changes in aggregate income and is crucial in the TANK model (and indeed in the Tractable HANK models to follow). Importantly, χ is the main departure from the assumption used by Campbell and Mankiw (1989, 1990, 1991). Throughout all their three papers on this subject, Campbell and Mankiw assume that rule-of-thumb households (H in our notation) consume a constant fraction of aggregate income, equivalent to setting χ = 1.<sup>2</sup> In the TANK model instead,

<sup>2</sup>A final footnote 26 in their third and final paper on this, the 1991 EER, points out that

household H consumes all of their own income. As χ may be greater than or less than one, this means that the consumption of the type H households may move more than or less than one-for-one with aggregate income.<sup>3</sup>

To illustrate the mechanism through which H consumption moves disproportionately with aggregate income, we must first consider the consumption of the savers. Substitute the consumption of H into c<sup>t</sup> = λc<sup>H</sup> <sup>t</sup> + (1 − λ)c S t to obtain:

$$c_t^S = \frac{1 - \lambda \chi}{1 - \lambda} y_t.$$

From this, we can see that the elasticity of S consumption to aggregate income will be less than one when the elasticity of H consumption (χ) is greater than one. It is also apparent that χ can be interpreted as the cyclicality of income inequality. Defining γ y <sup>t</sup> as the difference between the income of S and H (income inequality), we can obtain:

$$\gamma_t^y = y_t^S - y_t^H = \frac{1 - \chi}{1 - \lambda} y_t.$$
 (1)

When χ > 1, income inequality is countercyclical as H income rises more than one-for-one with aggregate income while S income rises less than one-for-one. Conversely, when χ < 1, income inequality is procyclical.

Consider the effect of an increase in aggregate income. When income rises, aggregate demand rises. To fulfill this additional consumption demand, firms must increase their demand for labour. This leads to a rise in the real wage and fuels a further increase in consumption demand from H as labour income is increased. Importantly, the rise in real wages also causes profits to fall. This generates a fall in the income of type S households. This allows the economy to reach equilibrium, as the income effect causes S households to supply the labour needed to meet the increased aggregate demand. This general equilibrium effect

<sup>&</sup>quot;utility costs would be much larger if agents consumed their own income".

<sup>3</sup>Bilbiie and Straub (2012) study precisely the empirical implications of that different assumption for the estimation of aggregate Euler equations, and contrast their results to Campbell and Mankiw's work.

means that the consumption of the H household can increase by more than the increase in aggregate income.

This example illustrates the importance of profits in generating the general equilibrium effects in the TANK model. In the RANK model studied in chapter 2, there is only one type of household. This means that the distribution of factor incomes is irrelevant as the same household incurs the labour income gains and the fall in profits. In TANK, the incidence of the fall in profits across the agents is crucial. Notice that χ is made up of two components:

$$\chi = 1 + \underbrace{\varphi}_{LabourMarket} \times \underbrace{\left(1 - \frac{\tau^D}{\lambda}\right)}_{FiscalRedistribution}$$

When the labour supply curve is upward-sloping (ϕ > 0), it is the fiscal redistribution scheme which determines whether χ is greater than or smaller than 1. This is because τ <sup>D</sup> determines the extent to which H households internalise the fall in profit income generated by their increased demand. When τ <sup>D</sup> = 0, the fall in profits falls entirely upon the S households. Therefore, S households work more and the H households demand more due to the rise in labour income. However, as τ <sup>D</sup> is increased, H households receive a negative transfer when profits fall. This mitigates their increase in demand as they internalise the fall in profit income. In equilibrium, consumption demand rises by less as S households suffer a smaller fall in profit income. When fiscal policy is sufficiently redistributive such that τ <sup>D</sup> > λ, we can see that χ < 1. In this case, H households receive a disproportionate share of profits. This means that the consumption demand of H will rise less than the original rise in aggregate income as the H household recognises that increased demand would cause them to incur a fall profit income. When τ <sup>D</sup> < λ the fall in profit income for H is not enough to offset the rise in labour income and H consumption demand rises more than one-for-one with aggregate income.

The Campbell-Mankiw benchmark of χ = 1 results when τ <sup>D</sup> = λ. In this case, uniform redistribution of profit income means that the income effect disappears. Similar to the RANK case, both types of households are equally exposed to the fall in profit income. Therefore, H consumption demand cannot rise more than the increase in aggregate income. The Campbell-Mankiw benchmark also results when ϕ = 0. Here, labour supply is infinitely elastic meaning that firms can hire workers to meet the increase in demand without the need for real wages to rise. This means that profits do not fall when demand increases. Hence, S households do not incur a fall in profit income and are not induced to work more to meet consumption demand form H households. This means that the consumption of type H cannot rise more than aggregate income.

# The Aggregate(d) Euler Equation: The Primitive "Master Equation" of TANK

To obtain the aggregated Euler equation for the TANK model, start with the Euler equation of the savers:

$$c_t^s = E_t c_{t+1}^S - \sigma r_t.$$

Substituting our expression for the consumption of S as a function of aggregate consumption delivers the Aggregate Euler Equation for the TANK model <sup>4</sup> :

$$c_t = E_t c_{t+1} - \sigma \frac{1 - \lambda}{1 - \lambda \chi} r_t.$$

This Euler equation is the same as for the RANK model but with a different coefficient on the real interest rate. This coefficient has a clear intuitive interpretation. Firstly, the numerator is equal to 1 − λ which corresponds to the share of households who are directly responsive to changes in interest rates. As the TANK model introduces a mass λ of agents who do not have access to financial markets, the direct effect of interest rate changes through intertemporal substitution must be reduced. The denominator represents the indirect effect of the change in interest rates working through the general equilibrium mechanism. As discussed above,

<sup>4</sup>Here, we assume that λχ < 1 such that interest rate cuts lead to an increase in consumption. We will consider the alternative case later in the chapter.

when aggregate income rises by one unit as a result of the interest rate change, the income of the λ hand-to-mouth households rises by χ units. As a result, the coefficient on the real interest rate is multiplied by a factor of <sup>1</sup> <sup>1</sup>−λχ, resembling the traditional Keynesian multiplier with an 'MPC' of λχ.

The TANK aggregate Euler equation plays the conceptual role of an aggregator: it collapses household heterogeneity into a small number of sufficient statistics and delivers a closed-form equilibrium condition that governs aggregate dynamics. This is analogous — in role, not in formal structure — to the master equation of mean-field games, which similarly links individual optimization to the evolution of the distribution. Unlike the PDE-based master equation in MFGs, however, the TANK aggregator is finite-dimensional and algebraic; the analogy is therefore suggestive rather than literal.

Here is how to rewrite the aggregate Euler (delivering the exact same amplification mechanism) that illustrates even more literally its role as a primitive "master equation", encapsulating how distributional dynamics feed back into aggregate dynamics. Denoting consumption inequality between the savers and the hand-to-mouth by γ<sup>t</sup> = c S <sup>t</sup> − c H t , and using that we are approximating around a symmetric steady state (C <sup>H</sup> = C <sup>S</sup> = C) we can rewrite the same aggregate Euler equation as:

$$c_t = E_t c_{t+1} - \sigma r_t - \underbrace{\lambda \left( \gamma_t - E_t \gamma_{t+1} \right)}_{\text{cycl ineq TANK}}$$
 (2)

The distributional wedge λ˜ (γ<sup>t</sup> − Etγt+1) captures, again, the cyclical-inequality channel; it encapsulates all the heterogeneity that is relevant for aggregate dynamics in this model (regardless of what model determines inequality itself in equilibrium: 1 is but one example of such model).<sup>5</sup> In this sense, 2 is a proto "master equation". There is amplification of aggregate-demand shocks when consumption (income) inequality is countercyclical: in response to an interest rate cut for example, the general-equilibrium effect on aggregate consumption will be larger than

<sup>5</sup> In this simple model, consumption inequality is the same as income inequality since there is no saving: we relax this in subsequent chapters.

in RANK iff inequality is countercyclical, whatever makes it so; in that case, more resources get allocated to the constrained (high-MPC) in an expansion, and that magnifies the expansion itself. If this sounds like a Keynesian cross, it is because it is.

### (New) Keynesian Cross Representation

The genealogy of the (New) Keynesian-cross representation in this chapter traces back to a handwritten note from Jordi Gal´ı during my PhD defense in September 2004. Gal´ı, serving as an external examiner, suggested that this was a useful way to frame the amplification mechanism emerging from my model. The suggestion proved remarkably fruitful. I incorporated an early version into the 2005 revision of the paper Bilbiie (2005), but it did not survive the publication process: an anonymous referee requested that it be removed, along with any reference to the word "Keynesian" — which, remarkably, had been in the original title (how the times have changed). A trace remained in the published 2008 version in the section title "Profits Redistribution Restores Keynesian (!) Logic," but the cross itself disappeared.

A decade later, when the heterogeneous-agent literature began to accelerate and converge toward what would become HANK, the Keynesian-cross representation offered exactly the right lens to reconnect analytical TANK insights with developments in consumption theory. Preston (2005), in the meantime, had provided the correct consumption-function representation of the RANK model, and his contribution made it possible to formalize the NK Cross in a way that was both rigorous and transparent. What began as a scribbled note during a thesis defense thus became a central organizing device for understanding amplification in heterogeneous-agent NK models.

As with the RANK model, we can also derive a Keynesian cross representation of the TANK model. This will allow us to examine the conditions under which shocks are amplified or dampened relative to RANK, and to study the relative importance of direct and general equilibrium effects in determining the response to monetary policy shocks.

To obtain the PE curve and Keynesian-cross representation for the TANK model, start with the consumption function for the savers.<sup>6</sup> This is the same as that of the representative household in the RANK model:

$$c_t^S = (1 - \beta)y_t^S - \sigma\beta r_t + \beta E_t c_{t+1}^S.$$

Using c<sup>t</sup> = λc<sup>H</sup> <sup>t</sup> +(1−λ)c S t and our equations for c S t and c H t as functions of aggregate consumption, we obtain:

$$c_t = [1 - \beta(1 - \lambda \chi)]\hat{y}_t - (1 - \lambda)\beta\sigma r_t + \beta(1 - \lambda \chi)E_t c_{t+1}.$$

This equation yields important insights into the differences between the RANK and the TANK models. Consider the case where the central bank engineers a real interest rate cut with persistence parameter p. The total effect of the change on consumption is equal to:

$$\Omega = \frac{\sigma}{1 - p} \frac{1 - \lambda}{1 - \lambda \chi}.$$

This effect is increasing in the share of hand-to-mouth agents λ when χ > 1. Hence, TANK generates amplification relative to RANK if and only if income inequality is countercyclical. Conversely, TANK dampens the effect of interest rate changes relative to RANK if and only if income inequality is procyclical χ < 1.

The indirect share of the total effect (the 'aggregate MPC') can be obtained

<sup>6</sup>The full derivation is for completion in the Appendix, and in the NK cross paper Bilbiie (2020) and its Appendix.

by considering the coefficient on aggregate income:

$$\omega = \frac{1 - \beta(1 - \lambda \chi)}{1 - \beta p(1 - \lambda \chi)}.$$

This corresponds to the slope of the PE curve and measures the proportion of the consumption change which is driven by changes in income. Notice tht since β is very close to 1, in the case of purely transitory shocks p = 0 this object is literally identical to the "aggregate MPC" λχ we recovered in the denominator of the multiplier expression, Samuelson-style. We will re-encounter this object repeatedly, for it governs the "multiplier" effect, or the indirect, GE effect, for any exogenous shock.

The direct effect of the interest rate change is given by the derivative with respect to the real interest rate (holding all else fixed):

$$\Omega_D = \frac{\sigma\beta(1-\lambda)}{1-\beta p(1-\lambda\chi)}.$$

This gives the 'shift' of the PE curve and gives the proportion of the consumption change driven by intertemporal substitution.

Crucially, we can see the the indirect share of the total consumption change is increasing in the share of hand-to-mouth agents λ regardless of the value of χ. When more hand-to-mouth agents are added to the model, the indirect effect share unambiguously rises and the direct share unambiguously falls. Therefore, although TANK may not necessarily amplify the response to monetary policy, the model will always be more 'general equilibrium' than its RANK counterpart. This is due to the presence of households who are more responsive to changes in their income. Hence, the TANK model successfully addresses one of the core shortcomings of the RANK model, its counterfactual reliance on intertemporal substitution as the key transmission mechanism for monetary policy.

In order for TANK to generate amplification relative to RANK, this strengthening of the indirect effect must override the weakening of the direct intertemporal substitution effect of monetary policy. This occurs only when χ > 1. When χ > 1 the income of hand-to -mouth agents rises more than aggregate income as increased consumption demand induces savers to increase their labour supply due to a fall in profit income. This general equilibrium mechanism is sufficiently strong to overcome the reduced responsiveness to the real interest rate.

#### Inverted Keynesian Logic

In the above sections, we have restricted our attention to the case where λ < χ<sup>−</sup><sup>1</sup> . As shown y the Euler equation,this restriction ensures that the usual aggregate demand logic holds - a rise in the real interest rate leads to a fall in aggregate consumption.

$$c_t = E_t c_{t+1} - \sigma \frac{1 - \lambda}{1 - \lambda \chi} r_t.$$

However, as shown by Bilbiie (2008), the aggregate demand logic becomes inverted when λ > χ<sup>−</sup><sup>1</sup> . In this case, a rise in the real interest leads to an increase in aggregate consumption. This also means that determinacy requires that the central bank implements an inverted Taylor rule in which they respond to increases in expected inflation by increasing the nominal interest rate less than one for one. This leads to a fall in the real interest rate in order to eliminate sunspots.

Bilbiie and Straub (2012; 2013) first estimated aggregate Euler equations from the TANK model in the US, using GMM and Bayesian techniques, respectively (the former was lateer revisited by Ascari et al. (2021)); they provide evidence that suggests that the IS slope became inverted in the United States during the 1970s. As a result, the inverted Taylor principle suggests that the passive monetary policy implemented by the Federal Reserve during the Great Inflation may have been a ore reasonable course of action than is conventionally thought. The advent of the financial liberalisation and innovation of the 1980s, may have served to bring about a restoration of the conventional aggregate demand logic. By reducing the proportion of households without access to financial markets (a fall in λ), these changes would restore the downward-sloping Euler-IS relationship. Consequently, the active monetary policy of the Volcker disinflation was also consistent with equilibrium determinacy.

#### Fiscal Multipliers According to TANK

As well as introducing a stronger general equilibrium mechanism, a key initial motivation of the TANK literature (referred to below) was to generate larger fiscal multipliers than in the RANK model. To study fiscal multiplies in the TANK model, we must extend the model to incorporate government spending. Suppose that the government spends G<sup>t</sup> (which is wasted) and balances its budget through lump-sum taxes T<sup>t</sup> . The tax system features exogenous redistribution, with H households paying a share α of total taxes and S households paying the remaining 1 − α.

$$\lambda T_t^H = \alpha T_t$$
$$(1 - \lambda)T_t^S = (1 - \alpha)T_t$$

Loglinearising around a steady state with G = 0 (so that lower case variable denote shares of steady state output) shows that we can decompose the taxes into two parts:

$$t_t^H = \frac{\alpha}{\lambda} t_t = \frac{\alpha}{\lambda} g_t = \underbrace{g_t}_{Balanced\ Budget} - \underbrace{\left(1 - \frac{\alpha}{\lambda}\right) t_t}_{Exogenous\ Redistribution}.$$

The taxes paid by H households are equal to the sum of a uniform tax equal to the spending increase and exogenous redistribution through transfers. When α < λ, H households pay a disproportionately low share of total taxes. This is effectively a redistributive transfer from S to H. When α > λ, this is a regressive transfer from H to S.

To derive the fiscal multiplier in the TANK model, first note that the goods market clearing condition and the budget constraints must change to reflect the addition of government spending and taxation.

$$y_t = c_t + g_t$$

$$c_t^H = w_t + n_t^H + \frac{\tau^D}{\lambda} d_t - t_t^H$$

Replacing the the labour supply of H in the budget and recalling that  $d_t = -w_t$  gives:

$$(1 + (\varphi \sigma)^{-1})c_t^H = (1 - \frac{\tau^D}{\lambda} + \varphi^{-1})w_t - t_t^H.$$

Use aggregate labour supply and  $y_t = c_t + g_t = n_t$  to re-write the wage as:

$$w_t = (\varphi + \sigma^{-1})c_t + \varphi g_t.$$

Substituting into the budget constraint of H allows us to express the consumption of H as a function of aggregate output, government spending and taxation:

$$c_t^H = \chi c_t + \chi \zeta g_t - \zeta t_t^H$$

$$where \ \zeta = \frac{1}{1 + (\varphi \sigma)^{-1}}.$$

The parameter  $\zeta$  gives the elasticity of H household consumption to a transfer. Using the definition of disposable income and the decomposition of taxes, we can express H consumption in terms of aggregate disposable income and government spending:

$$c_t^H = \chi \hat{y}_t + \zeta \left( \chi - \frac{\alpha}{\lambda} \right) g_t.$$

We can now follow the same steps as the previous section to derive the PE curve

and the aggregate Euler-IS. The PE curve is given by:

$$c_t = [1 - \beta(1 - \lambda \chi)]\hat{y}_t - (1 - \lambda)\beta\sigma r_t + \beta(1 - \lambda \chi)E_t c_{t+1} + \underbrace{\beta\lambda\zeta\left(\chi - \frac{\alpha}{\lambda}\right)(g_t - E_t g_{t+1})}_{Fiscal\ Policy}.$$

Using the fact that aggregate consumption is equal to aggregate disposable income  $(c_t = \hat{y}_t)$ , we can also obtain the aggregate Euler-IS:

$$c_t = E_t c_{t+1} - \frac{1 - \lambda}{1 - \lambda \chi} \sigma r_t + \frac{\lambda \zeta}{1 - \lambda \chi} \left( \chi - \frac{\alpha}{\lambda} \right) (g_t - E_t g_{t+1}).$$

The fiscal multiplier with a fixed real interest rate can now be obtained by differentiating with respect to  $g_t$ . The fiscal multiplier on output is equal to:<sup>7</sup>

$$\mathcal{M} = 1 + \frac{\lambda \zeta}{1 - \lambda \chi} \left( \chi - \frac{\alpha}{\lambda} \right).$$

In the RANK case, the output multiplier is equal to 1, meaning that consumption is uncharged when government spending is increased. However, in TANK, we can see that the multiplier on consumption is positive provided that  $\chi > \frac{\alpha}{\lambda}$ . This is a far more characteristically Keynesian result.

To analyse the source of the multiplier in the TANK model, note that we can decompose  $\mathcal{M}$  into two parts:

$$\mathcal{M} = 1 + \frac{\lambda \zeta}{1 - \lambda \chi} \left[ \underbrace{\left(\chi - 1\right)}_{NK\ Cross} + \underbrace{\left(1 - \frac{\alpha}{\lambda}\right)}_{Exogenous\ Redistribution} \right].$$

The first potion of the multiplier gives the multiplier for government spending

<sup>&</sup>lt;sup>7</sup>Note that, unlike monetary policy, the persistence of the government spending increase is irrelevant here.

financed through uniform taxation (i.e. α = λ):

$$\Omega_{Uniform} = 1 + \frac{\lambda \zeta}{1 - \lambda \chi} (\chi - 1).$$

With uniform taxation, TANK generates a larger fiscal multiplier than RANK if and only if χ > 1. hence, this term disappears in the Campbell-Mankiw benchmark case. This operates through the same general equilibrium mechanism as discussed in the section on monetary policy shocks.

The second portion gives the multiplier for a pure redistributive transfer from S to H:

$$\Omega_{Transfer} = \frac{\lambda \zeta}{1 - \lambda \chi} \left( 1 - \frac{\alpha}{\lambda} \right).$$

This term is positive if and only if α < λ, that is when the fiscal policy is financed with progressive taxation. Importantly, this term will still be present in the Campbell-Mankiw benchmark. In fact, even in the dampening case with procyclical income inequality, ΩT ransfer is still increasing in λ provided that taxation is progressive (α < λ). Therefore, even when TANK generates dampening of monetary shocks relative to RANK, a redistributive transfer from S to H can still increase aggregate consumption.

Using Keynesian Cross terminology, we can see that χ increases the slope of the PE curve. When government spending rises, χ also increases the shift of the PE curve provided that χ > 1.The degree of progressivity in the tax system also affects the shift of the PE curve. A decreases in α increases the shift of the PE curve provided that the transfer is progressive (α < λ).

This analysis shows that the TANK model is also more Keynesian than RANK in generating positive multipliers of government spending on consumption.

#### Adding the Phillips Curve

In the analysis above, we assumed that prices were rigid and that the central bank fixed the real interest rate. The TANK model can easily be extended to incorporate sticky (rather than fixed) prices and a Taylor rule for monetary policy. Consider the case where inflation is given by a static Phillips curve and the central bank implements a Taylor rule.

$$\pi_t = \kappa c_t + \kappa \zeta g_t$$

$$r_t = i_t - E_t \pi_{t+1} = (\phi - 1) E_t \pi_{t+1} - \varepsilon_t$$

Replacing these in the aggregate Euler-IS gives:

$$c_{t} = \left[1 - \frac{1 - \lambda}{1 - \lambda \chi} \sigma(\phi - 1)\kappa\right] E_{t} c_{t+1} + \frac{1 - \lambda}{1 - \lambda \chi} \sigma \varepsilon_{t} - \underbrace{\frac{1 - \lambda}{1 - \lambda \chi} \sigma(\phi - 1)\kappa \zeta E_{t} g_{t+1}}_{RANK} + \underbrace{\frac{\lambda \zeta}{1 - \lambda \chi} \left(\chi - \frac{\alpha}{\lambda}\right) (g_{t} - E_{t} g_{t+1})}_{TANK}.$$

As in the RANK model, firms now respond to increased demand by increasing their price as well as their labour demand. If the government spending shock is persistent, this leads to a rise in expected inflation.As the central bank follows a Taylor rule, the real interest rate will rise (assuming that monetary policy sets φ > 1 such that monetary policy is active).This rise in the real interest rate reduces consumption demand , causing the fiscal multiplier to fall. In the RANK case, this delivers a fiscal multiplier of less than one. In the TANK model, this reduces the multiplier (though M may still be greater than one if χ is sufficiently large and/or α is sufficiently small).

For a government spending shock of persistence p, aggregate consumption

can be expressed as:

$$c_{t} = \frac{(1-\lambda)\sigma}{(1-\lambda\chi)(1-p) + p(1-\lambda)\sigma\kappa(\phi-1)} \varepsilon_{t} + \zeta \frac{\lambda\left(\chi - \frac{\alpha}{\lambda}\right)(1-p) - p(1-\lambda)\sigma\kappa(\phi-1)}{(1-\lambda\chi)(1-p) + p(1-\lambda)\sigma\kappa(\phi-1)} g_{t}.$$

As discussed above, a positive fiscal multiplier requires  $\left(\chi - \frac{\alpha}{\lambda}\right)$  to be sufficiently high to override the contractionary monetary policy response to higher expected inflation.

#### Forward Guidance: Still a puzzle

Although the TANK model improves upon the RANK model by generating higher fiscal multipliers and a stronger general equilibrium mechanism, the Euler-IS equation still has a unit coefficient on expected future aggregate consumption.

$$c_t = E_t c_{t+1} - \sigma \frac{1 - \lambda}{1 - \lambda \chi} r_t.$$

This means that the forward guidance puzzle is still present in the TANK model - an announced future interest rate cut has a larger effect on present aggregate consumption the further in the future is the cut.

## Notes on the Literature: Some TANK Archeology

A key motivating factor in the development of two-agent New Keynesian models was the failure of the Real Business Cycle and RANK models to generate sufficiently large fiscal multipliers. Blanchard and Perotti (2002) used US post-war data to show that positive government spending shocks increased private consumption, while positive tax shocks lead to a fall in private consumption. They noted

that existing models were unable to produce predictions in line with the data; this was arguably the spark that got the TANK literature started, since Roberto Perotti was both the current author's PhD thesis advisor, and Jordi Gali's coauthor on a paper on fiscal rules in the EU. Conversations with and encouragement from him led directly to investigations in this direction. In particular, it turns out that Mankiw (2000) (building upon Campbell and Mankiw (1989)), precisely to move towards a more realistic model of fiscal policy but without stepping into the OLG world, had developed in a short paper a two-agent "spender-saver" Ramsey growth model in which a proportion of households consume their current income while savers owned the capital stock. This was a "TA" (two-agent)—but not NK yet!—model.<sup>8</sup>

Both Gal´ı et al. (2007) and Bilbiie (2008) (chapter 1 of the author's 2004 PhD thesis) followed this agenda, if with subtly but importantly different approaches, leading to what we now call TANK models. Gal´ı et al. (2007) essentially extended the business-cycle version of the Mankiw model with sticky prices; that is, they introduced "rule of thumb" households into a model with sticky prices and, crucially, physical capital. The distinction between the two agent types was is fact described as being oeprational only through holding or not physical capital, the only asset held in the economy. This renderd the model impossible to solve analytically, so all the results were numerical, obtained by computer simulation. The quantitative results showed that the introduction of rule-of-thumb households allowed the model under certain calibrations (with a centralized labor market and enough degree of deficit-fianancing, so that the rule-of-thumb did not pay their ful lshare of taxes) to deliver positive consumption multipliers. A companion—still numerical and centered about the physical capital holding distinction—paper Gal´ı et al. (2004) noted that the Taylor principle is insufficient to guarantee equilibrium determinacy, by means of simulations. In the baseline models presented here, following Bilbiie (2008), there is no capital but there are segmented markets as in Alvarez et al. (2001). This allows the models to yield closed-form analytical results,

<sup>8</sup> It is worth noticing that Campbell and Mankiw's three papers on the topic did not build "models" (much less so, NK models) but instead estimated empirical Euler equations using the two-agent distinction.

sharpens intuition, and (perhaps therefore) has been adopted as the benchmark by most of the subsequent literature using "TANK"<sup>9</sup> models referred to in the introduction (see Di Bartolomeo and Rossi (2007) for another early contribution to that literature). The results ranged from general aggregate dynamics through the aggregate Euler equation, monetary policy amplification, the role of profits, and optimal monetary policy by means of a quadratic approximation to aggregate welfare; to the analytical derivation of fiscal multipliers Bilbiie and Straub (2004); and the estimation of the TANK aggregate Euler equation Bilbiie and Straub (2012) and of a small-scale TANK-DSGE model with a focus on monetary policy Bilbiie and Straub (2013) and fiscal multipliers Bilbiie et al. (2008), respectively. Other contributions extended this to wage stickiness, e.g. Colciago (2011); Furlanetto (2011); Natvik (2009, 2012); Ascari et al. (2017) and to an open economy Eser (2009). Later, in the aftermath of the Great Recession, TANK models (still not called such yet) became a standard environement for studying liqudity traps Eggertsson and Krugman (2012), and the effects of fiscal transfers and public debt that we shall return to later, Bilbiie et al. (2013); Monacelli and Perotti (2011); Giambattista and Pennings (2017); Mehrotra (2018).

A final strand of the TANK literature originated in my July 2015 keynote lecture, Hand-to-Mouth Macro, delivered at the ERMAS conference in Cluj. That lecture—and the working-paper versions circulating since 2016—developed what became known as the New Keynesian Cross (NK Cross), Bilbiie (2020), on which both this chapter and the previous one build. The aim of that paper was to show, in a transparent and fully analytical way, that the TANK model can reproduce several of the key amplification mechanisms emphasized in the emerging quantitative HANK literature. The NK Cross provided the right language to make this connection precise: it highlighted the decomposition between direct MPC effects and indirect general-equilibrium feedbacks, and clarified analytically the conditions under which heterogeneity leads to amplification relative to RANK—core themes of the then-young HANK literature, including Kaplan et al. (2018); Auclert (2019); Bayer et al. (2019); Gornemann et al. (2016); Hagedorn et al. (2019);

<sup>9</sup>This acronym came much later, courtesy of Kaplan et al. (2018); the "working acronym" for this second strand was "LAMP", from, precisely "Limited Asset Markets Pariticipation".

McKay et al. (2016).

Another paper in that literature by Broer et al. (2020) further clarified the role that income distribution played in HANK monetary transmission by using a simple, TANK-inspired HANK model and arguing forcefully in favor of introducing wage rigidity (their follow-up work Broer et al. (2023, 2024) extended the analysis to fiscal multipliers). Subsequent work by Debortoli and Gal´ı (2018) pursued a complementary comparison between TANK and HANK models, using essentially the same analytical TANK structure developed in my thesis and in Bilbiie (2008). They then compared a version of this analytical TANK model to a quantitative HANK model that they solved numerically. By contrast, the NK Cross paper compared the same analytical TANK benchmark to equilibrium outcomes in the leading calibrated HANK models in the literature listed above. The two approaches therefore address different but related questions: one compares TANK to its own quantitative counterpart, while the other compares TANK to the field's established quantitative benchmarks. Maliar and Naubert (2019), instead, investigated the role of the monetary policy rule in TANK for deliverig amplification or the lack thereof. Together, these contributions helped clarify some of the conceptual links between tractable heterogeneous-agent mechanisms and the richer dynamics found in fully quantitative HANK environments. The rest of the book explores additional such links that lie beyond these "first-generation" TANK models.

### Summary

The TANK model studied in this chapter addresses two of the core shortcomings of the RANK model. By introducing hand-to-mouth agents, the model takes on more traditionally Keynesian characteristics. This is evident in the fact that the TANK model can generate fiscal multipliers greater than one. In addition, the TANK model is a "more general-equilibrium" model than its RANK counterpart. While the RANK model relies on direct intertemporal substitution to generate the response to monetary policy, TANK exhibits strong 'indirect effects'. When income inequality is countercyclical (χ > 1), these indirect effects serve to amplify the effects of monetary policy shocks relative to the RANK case. However, regardless of whether the model generates amplification compared to RANK, TANK will always generate a higher indirect share of shock transmission.

TANK does, however, lack a key mechanism of the HANK literature—risk and precautionary saving. The next chapters will examine how to incorporate these features into a tractable framework which closely follows and naturally nests the TANK model. <sup>10</sup>

<sup>10</sup>This will also contribute to solving the forward guidance puzzle.

## References

- Fernando Alvarez, Robert E Lucas Jr, and Warren E Weber. Interest rates and inflation. American Economic Review, 91(2):219–225, 2001.
- Guido Ascari, Andrea Colciago, and Lorenza Rossi. Limited Asset Market Participation and Optimal Monetary Policy. Economic Inquiry, 2017. doi: 10.1111/ecin.12413.
- Guido Ascari, Leandro M. Magnusson, and Sophocles Mavroeidis. Empirical Evidence on the Euler Equation for Consumption in the US. Journal of Monetary Economics, 117:129–152, 2021. doi: 10.1016/j.jmoneco.2019.12.004.
- Adrien Auclert. Monetary policy and the redistribution channel. American Economic Review, 109(6):2333–67, 2019.
- Christian Bayer, Ralph L¨utticke, Lien Pham-Dao, and Volker Tjaden. Precautionary Savings, Illiquid Assets, and the Aggregate Consequences of Shocks to Household Income Risk. Econometrica, 87(1):255–290, 2019. doi: 10.3982/ECTA14321.
- Florin O. Bilbiie. Limited Asset Markets Participation, Monetary Policy and (Inverted) Keynesian Logic. Economics Papers 2005-W09, Economics Group, Nuffield College, University of Oxford, 2005. URL https://www.nuffield.ox.ac.uk/economics/papers/2005/w9/LAMPtheory.pdf.
- Florin O. Bilbiie. Limited Asset Markets Participation, Monetary Policy and (Inverted) Aggregate Demand Logic. Journal of Economic Theory, 140(1):162– 196, 2008. doi: 10.1016/j.jet.2007.06.010.
- Florin O. Bilbiie. The new keynesian cross. Journal of Monetary Economics, 114: 90–108, 2020. doi: 10.1016/j.jmoneco.2020.04.009.
- Florin O. Bilbiie and Roland Straub. Fiscal Policy, Labor Markets and Business Cycle Fluctuations. Working Paper 2004/6, Magyar Nemzeti Bank (Central Bank of Hungary), 2004.

- Florin O Bilbiie and Roland Straub. Changes in the output euler equation and asset markets participation. Journal of Economic Dynamics and Control, 36 (11):1659–1672, 2012.
- Florin O Bilbiie and Roland Straub. Asset market participation, monetary policy rules, and the great inflation. Review of Economics and Statistics, 95(2):377– 392, 2013.
- Florin O. Bilbiie, Andr Meier, and Gernot J. Mller. What accounts for the changes in U.S. fiscal policy transmission? Journal of Money, Credit and Banking, 40 (7):1257–1289, 2008. doi: 10.1111/j.1538-4616.2008.00164.x.
- Florin O. Bilbiie, Tommaso Monacelli, and Roberto Perotti. Public Debt and Redistribution with Borrowing Constraints. Economic Journal, 123(566):F64– F98, 2013. doi: 10.1111/ecoj.12012.
- Olivier Blanchard and Roberto Perotti. An empirical characterization of the dynamic effects of changes in government spending and taxes on output. the Quarterly Journal of economics, 117(4):1329–1368, 2002. doi: 10.1162/003355302320935043.
- Tobias Broer, Niels-Jakob H. Hansen, Per Krusell, and Erik Oberg. The New Key- ¨ nesian Transmission Mechanism: A Heterogeneous Agent Perspective. Review of Economic Studies, 87(1):77–101, 2020. doi: 10.1093/restud/rdz002.
- Tobias Broer, Per Krusell, and Erik Oberg. Fiscal Multipliers: A Heterogenous- ¨ Agent Perspective. Quantitative Economics, 14(3):799–816, 2023. doi: 10.3982/QE1835.
- Tobias Broer, Jeppe Druedahl, Karl Harmenberg, and Erik Oberg. Stimulus effects ¨ of common fiscal policies. CEPR Discussion Paper 19823, Centre for Economic Policy Research, December 2024.
- John Y Campbell and N Gregory Mankiw. Consumption, income, and interest rates: Reinterpreting the time series evidence. NBER macroeconomics annual, 4:185–216, 1989. doi: 10.1086/654144.

- John Y. Campbell and N. Gregory Mankiw. Permanent income, current income, and consumption. Journal of Business & Economic Statistics, 8(3):265–279, 1990. doi: 10.2307/1391964.
- John Y. Campbell and N. Gregory Mankiw. The response of consumption to income: A cross-country investigation. European Economic Review, 35(4):723– 756, 1991.
- Andrea Colciago. Rule-of-Thumb Consumers Meet Sticky Wages. Journal of Money, Credit and Banking, 43(2-3):325–353, 2011. doi: 10.1111/j.1538- 4616.2010.00382.x.
- Davide Debortoli and Jordi Gal´ı. Monetary policy with heterogeneous agents: Insights from tank models. 2018.
- Giovanni Di Bartolomeo and Lorenza Rossi. Effectiveness of Monetary Policy and Limited Asset Market Participation. International Journal of Economic Theory, 3(3):213–218, 2007. doi: 10.1111/j.1742-7363.2007.00052.x.
- Gauti B Eggertsson and Paul Krugman. Debt, deleveraging, and the liquidity trap: A fisher-minsky-koo approach. The Quarterly Journal of Economics, 127 (3):1469–1513, 2012. doi: 10.1093/qje/qjs023.
- Fabian Eser. Monetary Policy in a Currency Union with Heterogeneous Limited Asset Markets Participation. Economics Series Working Papers 464, University of Oxford, Department of Economics, 2009.
- Francesco Furlanetto. Fiscal Stimulus and the Role of Wage Rigidity. Journal of Economic Dynamics and Control, 35(4):512–527, 2011. doi: 10.1016/j.jedc.2010.12.008.
- Jordi Gal´ı, J. David L´opez-Salido, and Javier Vall´es. Rule-of-thumb Consumers and the Design of Interest Rate Rules. Journal of Money, Credit and Banking, 36(3):491–511, 2004. doi: 10.1353/mcb.2004.0052.
- Jordi Gal´ı, J. David L´opez-Salido, and Javier Vall´es. Understanding the effects of government spending on consumption. Journal of the European Economic Association, 5(1):227–270, 2007.

- Eric Giambattista and Steven Michael Pennings. When is the Government Transfer Multiplier Large? European Economic Review, 100:525–543, 2017. doi: 10.1016/j.euroecorev.2017.09.007.
- Nils Gornemann, Keith Kuester, and Makoto Nakajima. Doves for the Rich, Hawks for the Poor? Distributional Consequences of Monetary Policy. 2016. CEPR Discussion Paper No. DP11233.
- Marcus Hagedorn, Iourii Manovskii, and Kurt Mitman. The Fiscal Multiplier. Working Paper 25571, NBER, 2019.
- Greg Kaplan, Benjamin Moll, and Giovanni L Violante. Monetary policy according to hank. American Economic Review, 108(3):697–743, 2018. doi: 10.1257/aer.20160042.
- Lilia Maliar and Christopher Naubert. Monetary policy transmission with endogenous central bank responses in tank. Discussion Paper 14159, Centre for Economic Policy Research, London, 2019.
- N. Gregory Mankiw. The Savers-Spenders Theory of Fiscal Policy. American Economic Review, 90(2):120–125, 2000. doi: 10.1257/aer.90.2.120.
- Alisdair McKay, Emi Nakamura, and J´on Steinsson. The Power of Forward Guidance Revisited. American Economic Review, 106(10):3133–3158, 2016. doi: 10.1257/aer.20150063.
- Neil R. Mehrotra. Fiscal Policy Stabilization: Purchases or Transfers? International Journal of Central Banking, 14(1):1–57, 2018.
- Tommaso Monacelli and Roberto Perotti. Redistribution and the Multiplier. IMF Economic Review, 59(4):630–651, 2011. doi: 10.1057/imfer.2011.26.
- Gisle James Natvik. Government Spending and the Taylor Principle. Journal of Money, Credit and Banking, 41(1):57–77, 2009. doi: 10.1111/j.1538- 4616.2008.00191.x.

Gisle James Natvik. Government Spending Shocks and Rule-of-Thumb Consumers with Steady-State Inequality. Scandinavian Journal of Economics, 114(4):1414– 1436, 2012. doi: 10.1111/j.1467-9442.2012.01726.x.

Bruce Preston. Adaptive learning in infinite horizon decision problems. Mimeo, Columbia University, 2005.