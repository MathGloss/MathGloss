---
 layout: page
 title: diameter of an n-simplex
 permalink: /chicago/diameter_of_an_n-simplex
---
The **diamteter** of an [n-simplex](https://defsmath.github.io/DefsMath/n-simplex) $[v_0,\dots,v_n]$ is the maximum distance (in the [ambient](https://defsmath.github.io/DefsMath/Euclidean_inner_product) [Euclidean](https://defsmath.github.io/DefsMath/########################Euclidean) [metric](https://defsmath.github.io/DefsMath/metric_space) [inner product induces metric](https://defsmath.github.io/DefsMath/inner_product_induces_metric)) between any of its vertices.

This is equivalent to the [diameter](https://defsmath.github.io/DefsMath/diameter_of_a_set) of the [n-simplex](https://defsmath.github.io/DefsMath/n-simplex) when considered as a set because the distance between two points $v$ and $\sum_i t_iv_i$ of $[v_0,\dots,v_n]$ satisfies $$\begin{align*}\left|v-\sum_i t_iv_i\right| &= \left|\sum_it_i(v-v_i)\right| \\&\leq \sum_i t_i |v-v_i| \\&\leq \sum_i t_i\max
|v-v_i|\\& = \max|v-v_i|.\end{align*}$$