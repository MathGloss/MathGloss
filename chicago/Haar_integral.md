---
 layout: page
 title: Haar integral
 permalink: /chicago/haar_integral
---
We define the **Haar integral** over a [topological space](https://defsmath.github.io/DefsMath/topological_space) $X$ s follows: 

Any [Borel](https://defsmath.github.io/DefsMath/Borel_σ-algebra) [measure](https://defsmath.github.io/DefsMath/measure_space) $\mu$ on $X$ gives a [linear](https://defsmath.github.io/DefsMath/linear_transformation) [functional](https://defsmath.github.io/DefsMath/functional) $$\int:C_c(X) \to \mathbb C, f\mapsto \int_X(f) := \int_X f(x)\text d\mu(x)$$ where $C_c(X)$ is the collection of [continuous](https://defsmath.github.io/DefsMath/continuous) complex-valued functions on $X$ with [compact support](https://defsmath.github.io/DefsMath/compact_support) and the [integral](https://defsmath.github.io/DefsMath/Lebesgue_integral) is defined according to that measure.

The Haar integral is this $\mathbb C$-linear function $\int:C_c(X) \to \mathbb C$  such that
1. for all $f\in C_c(X)$, if $f(x) \geq 0$ for all $x\in X$ then $\int_X f \geq 0$. Moreover, $\int_X f= 0$ implies that $f=0$.  (when $f(x)$ is real)
2. For any [compact](https://defsmath.github.io/DefsMath/compact) $K\subset X$, there exists some $c_K\geq 0$ such that for all [continuous](https://defsmath.github.io/DefsMath/continuous) functions with [support](https://defsmath.github.io/DefsMath/support) in $K$, $\left|\int_X f\right| \leq c_K\cdot \max\limits_{x\in K} |f(x)|$.

If we want the integral to be [invariant](https://defsmath.github.io/DefsMath/G-invariant_function) with respect to the [action of a group](https://defsmath.github.io/DefsMath/group_action), we choose the [measure](https://defsmath.github.io/DefsMath/##############measure) to be the [Haar measure](https://defsmath.github.io/DefsMath/Haar_measure).

Also keep in mind that this is in fact a special case of the [Lebesgue integral](https://defsmath.github.io/DefsMath/Lebesgue_integral)! All of those [properties of the integral](https://defsmath.github.io/DefsMath/properties_of_the_integral) still apply here with no extra work!