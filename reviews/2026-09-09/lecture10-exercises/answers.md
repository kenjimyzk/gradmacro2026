## 発展問題

### 問5 `[Research extension] [Derivation]`：初期実質賃金と完全安定化

**1. 自然実質賃金と状態の推移**

柔軟価格の条件 $\mu_t^p=a_t-w_t=0$ から $w_t^f=a_t$ です。したがって、賃金インフレ恒等式より
$$
\begin{aligned}
\widetilde w_t-\widetilde w_{t-1}
&=(w_t-w_{t-1})-(a_t-a_{t-1})\\
&=\pi_t^w-\pi_t^p-(a_t-a_{t-1}).
\end{aligned}
$$
過去の実質賃金と当期の技術変化が、必要な名目賃金・物価の調整を制約します。

**2. 全期の完全安定化**

すべての期・履歴で両インフレ率をゼロとする計画では、将来インフレの期待もゼロです。$\kappa_p,\kappa_w>0$ なので、両フィリップス曲線は
$$
\mu_t^p=\mu_t^w=0
$$
を要求します。マークアップの和から $x_t=0$、価格マークアップの定義から $w_t=a_t$ です。一方、恒等式より $\Delta w_t=0$ なので、$w_t=w_{-1}$ が続きます。両立の必要条件は
$$
a_t=w_{-1}\qquad\text{すべての }t\geq0
$$
です。初期の $a_0$ と $w_{-1}$ が一致し、その後も技術が変わらないことが必要です。この場合は自然配分が一定なので、IS曲線を満たす実質・名目利子率の乖離をともにゼロとすることで、ゼロインフレの配分を支持できます。この支持だけで均衡の一意性を主張しているわけではありません。

設問のショックでは、$a_0=0.01$ に対して $w_{-1}=0$ なので必要条件を満たさず、計画は実現できません。技術ショックがなく $a_t=0$ でも、$w_{-1}\ne0$ なら同じ問題が生じます。これは特定の金利ルールの失敗ではなく、実質賃金を変えるためには両インフレ率に差が必要なことから生じます。

**3. 当期だけの安定化との違い**

当期だけ両インフレ率がゼロでも、将来の期待インフレが非ゼロなら
$$
\kappa_p\mu_t^p=\beta\mathbb E_t\pi_{t+1}^p,
\qquad
\kappa_w\mu_t^w=\beta\mathbb E_t\pi_{t+1}^w
$$
であり、当期のマークアップはゼロとは限りません。2の結論には、全期にわたる計画が必要です。

```{=latex}
\Needspace{8\baselineskip}
```

### 問6 `[Research extension] [Derivation] [Computation]`：二つのインフレ率と柔軟性の極限

**1. 条件付きのインフレ率**

期待項がゼロなら $\mu_t^p=-\pi_t^p/\kappa_p$、$\mu_t^w=-\pi_t^w/\kappa_w$ です。両者の和を使うと
$$
\frac{\pi_t^p}{\kappa_p}+\frac{\pi_t^w}{\kappa_w}
=(\gamma+\varphi)x_t.
$$
$\pi_t^w=\pi_t^p+\Delta w_t$ を代入して
$$
\begin{aligned}
\pi_t^p&=\frac{\kappa_p\kappa_w}{\kappa_p+\kappa_w}
(\gamma+\varphi)x_t-\frac{\kappa_p}{\kappa_p+\kappa_w}\Delta w_t,\\
\pi_t^w&=\frac{\kappa_p\kappa_w}{\kappa_p+\kappa_w}
(\gamma+\varphi)x_t+\frac{\kappa_w}{\kappa_p+\kappa_w}\Delta w_t
\end{aligned}
$$
を得ます。

**2. 数値例**

$\bar\kappa=1/30$、$(\gamma+\varphi)x_t=0.02$ なので、
$$
\begin{aligned}
\pi_t^p&=\frac{0.02}{30}-\frac23(0.002)
=-\frac1{1500}\simeq-0.0006667,\\
\pi_t^w&=\frac{0.02}{30}+\frac13(0.002)
=\frac1{750}\simeq0.0013333.
\end{aligned}
$$
100倍した一次近似の表示では、それぞれ約 $-0.0667$、$0.1333$ パーセントポイントです。両者の差は $0.002$ です。実質賃金を上げるための相対価格調整が、正の需給ギャップによる共通の上昇圧力を上回るため、価格インフレ率は負になります。

**3. 柔軟化の極限**

$\Delta w_t=0$ なら
$$
\pi_t^p=\pi_t^w=\bar\kappa(\gamma+\varphi)x_t,
\qquad
\bar\kappa=\frac{\kappa_p\kappa_w}{\kappa_p+\kappa_w}.
$$
$\kappa_i=\psi_i/\eta_i$ なので、他方の調整費用を正に固定すると、
$$
\begin{aligned}
\eta_w\to0&\Rightarrow\kappa_w\to\infty
\Rightarrow\bar\kappa\to\kappa_p,\\
\eta_p\to0&\Rightarrow\kappa_p\to\infty
\Rightarrow\bar\kappa\to\kappa_w.
\end{aligned}
$$
それぞれ価格硬直性だけ、賃金硬直性だけの傾きを回収します。$\kappa_i\to0$ は調整費用が大きくなる方向であり、柔軟化とは逆です。これは $\Delta w_t=0$ とした合成係数の極限であり、柔軟な名目変数のインフレ率が必ずゼロになるという意味ではありません。

```{=latex}
\Needspace{6\baselineskip}
```

**4. 動学解との違い**

$x_t$、$\Delta w_t$ と将来期待を条件として与えた関係であり、これらの変数をショックから求めていません。インパルス応答には、初期実質賃金、マークアップの定義、合理的期待、IS曲線、政策ルール、ショック過程を同時に満たす経路が必要です。

### 問7 `[Research extension] [Derivation]`：実質賃金調整の費用下限

**1. 恒等式だけを使った最小化**

$\pi_t^w=\pi_t^p+\delta$ を代入すると、
$$
J_t=\frac12\left[\omega_p(\pi_t^p)^2
+\omega_w(\pi_t^p+\delta)^2\right].
$$
一階条件は $\omega_p\pi_t^p+\omega_w(\pi_t^p+\delta)=0$ です。二階微分は $\omega_p+\omega_w>0$ なので、最小点は一意に
$$
\pi_t^p=-\frac{\omega_w}{\omega_p+\omega_w}\delta,
\qquad
\pi_t^w=\frac{\omega_p}{\omega_p+\omega_w}\delta
$$
と決まります。代入すれば下限は
$$
J_t^{\min}=\frac12\frac{\omega_p\omega_w}{\omega_p+\omega_w}\delta^2.
$$
$\delta>0$ なら物価下落と名目賃金上昇を組み合わせて実質賃金を上げます。$\omega_w$ が相対的に大きいほど賃金インフレ率を小さくし、物価下落に調整を多く負担させます。

**2. 数値と解釈**

設問では $\omega_p=30$、$\omega_w=60$ なので、
$$
\pi_t^p=-\frac1{150}\simeq-0.006667,
\qquad
\pi_t^w=\frac1{300}\simeq0.003333,
\qquad
J_t^{\min}=0.001.
$$
インフレ率を100倍すると約 $-0.6667$、$0.3333$ パーセントポイントです。$J_t$ は正規化された損失であり、消費の百分率そのものではありません。

この計算は、$\Delta w_t=\delta$ を満たす任意の動学的配分について、当期の名目調整損失がこれより小さくならないことを示します。両フィリップス曲線、IS曲線、初期状態や将来期待を制約に含めず、$x_t^2/2$ と将来の損失も目的から落としているため、この下限を達成する配分が元のモデルで実現可能とは限りません。したがって、動学的な最適政策や総厚生損失を求めたことにはなりません。

```{=latex}
\Needspace{6\baselineskip}
```

**3. 静学条件付き解との一致**

問6で $x_t=0$、$\Delta w_t=\delta$ とすると、
$$
\pi_t^p=-\frac{\kappa_p}{\kappa_p+\kappa_w}\delta,
\qquad
\pi_t^w=\frac{\kappa_w}{\kappa_p+\kappa_w}\delta.
$$
$\delta\ne0$ のもとで1の配分と一致する条件は
$$
\frac{\kappa_p}{\kappa_p+\kappa_w}
=\frac{\omega_w}{\omega_p+\omega_w}
\quad\Longleftrightarrow\quad
\kappa_p\omega_p=\kappa_w\omega_w.
$$
$\kappa_i\omega_i=\psi_i/(\gamma+\varphi)$ なので、$\psi_p=\psi_w$ と同値です。$\delta=0$ なら両方の解がゼロとなり、代替弾力性にかかわらず一致します。この一致も当期の静学条件に関するもので、動学的な最適性を保証しません。
