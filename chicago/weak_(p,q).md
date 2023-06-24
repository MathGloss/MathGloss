---
 layout: page
 title: weak (p,q)
 permalink: /chicago/weak_(p,q)
---
Let $(X,\Sigma,\mu)$ and $(Y,T,\nu)$  be [measure spaces](https://defsmath.github.io/DefsMath/measure_space) and let $T: L_1(X,\mu) \to L_1(Y,\nu)$ be an operator that maps [measurable functions](https://defsmath.github.io/DefsMath/measurable_function) on $X$ to measurable functions on $Y$. Let $1\leq p\leq \infty$ and $1\leq q < \infty$. The operator $T$ is of type **weak $(p,q)$** if there exists a constant $c > 0$ such that $$\mu(\{x \in X\mid |Tf(x)|>t\})\leq\left(\frac{c||f||_p}{t}\right)^q.$$ 
If $q = \infty$, then $T$ is **weak $(p,\infty)$** if there exists a constant $c > 0$ such that $||Tf||_\infty \leq c||f||_p$.

