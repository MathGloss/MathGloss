---
 layout: page
 title: Haar integral
 permalink: /chicago/haar_integral
---
We define the **Haar integral** over a [topological space](https://mathgloss.github.io/MathGloss/chicago/topological_space) $X$ s follows: 

Any [Borel](https://mathgloss.github.io/MathGloss/chicago/Borel_σ-algebra) [measure](https://mathgloss.github.io/MathGloss/chicago/measure_space) $\mu$ on $X$ gives a [linear](https://mathgloss.github.io/MathGloss/chicago/linear_transformation) [functional](https://mathgloss.github.io/MathGloss/chicago/functional) $$\int:C_c(X) \to \mathbb C, f\mapsto \int_X(f) := \int_X f(x)\text d\mu(x)$$ where $C_c(X)$ is the collection of [continuous](https://mathgloss.github.io/MathGloss/chicago/continuous) complex-valued functions on $X$ with [compact support](https://mathgloss.github.io/MathGloss/chicago/compact_support) and the [integral](https://mathgloss.github.io/MathGloss/chicago/Lebesgue_integral) is defined according to that measure.

The Haar integral is this $\mathbb C$-linear function $\int:C_c(X) \to \mathbb C$  such that
1. for all $f\in C_c(X)$, if $f(x) \geq 0$ for all $x\in X$ then $\int_X f \geq 0$. Moreover, $\int_X f= 0$ implies that $f=0$.  (when $f(x)$ is real)
2. For any [compact](https://mathgloss.github.io/MathGloss/chicago/compact) $K\subset X$, there exists some $c_K\geq 0$ such that for all [continuous](https://mathgloss.github.io/MathGloss/chicago/continuous) functions with [support](https://mathgloss.github.io/MathGloss/chicago/support) in $K$, $\left\vert \int_X f\right\vert  \leq c_K\cdot \max\limits_{x\in K} \vert f(x)\vert $.

If we want the integral to be [invariant](https://mathgloss.github.io/MathGloss/chicago/G-invariant_function) with respect to the [action of a group](https://mathgloss.github.io/MathGloss/chicago/group_action), we choose the [measure](https://mathgloss.github.io/MathGloss/chicago/##############measure) to be the [Haar measure](https://mathgloss.github.io/MathGloss/chicago/Haar_measure).

Also keep in mind that this is in fact a special case of the [Lebesgue integral](https://mathgloss.github.io/MathGloss/chicago/Lebesgue_integral)! All of those [properties of the integral](https://mathgloss.github.io/MathGloss/chicago/properties_of_the_integral) still apply here with no extra work!