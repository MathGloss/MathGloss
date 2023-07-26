---
 layout: page
 title: Lebesgue integral of a simple function
 permalink: /chicago/lebesgue_integral_of_a_simple_function
---
Let $(X,\Sigma, \mu)$ be a [measure space](https://mathgloss.github.io/MathGloss/measure_space). Let $f = \sum\limits_{k=1}^n a_k \chi_{A_k}$ be a [simple function](https://mathgloss.github.io/MathGloss/simple_function) such that $\mu(A_k) < \infty$ for $a_k \neq 0$.  The **Lebesgue integral of the [simple function](https://mathgloss.github.io/MathGloss/simple_function)** $f$ is defined as $$\int\left(\sum_{k=1}^n a_k\chi_{A_k}\right)d\mu = \sum_{k=1}^n a_k \int\chi_{A_k}d\mu = \sum_{k=1}^n a_k\mu(A_k),$$ consistent with the [Lebesgue integral of characteristic functions](https://mathgloss.github.io/MathGloss/Lebesgue_integral_of_characteristic_function).

If $B$ is a [measurable](https://mathgloss.github.io/MathGloss/measurable) subset of $X$ and $g = \sum\limits_{k=1}^n b_k\chi_{B_k}$ is a [measurable](https://mathgloss.github.io/MathGloss/measurable_function) [simple function](https://mathgloss.github.io/MathGloss/simple_function) on $B$, define $$\int_B gd\mu = \int\chi_Bgd\mu = \sum_{k=1}^nb_k\mu(B_k\cap B).$$

