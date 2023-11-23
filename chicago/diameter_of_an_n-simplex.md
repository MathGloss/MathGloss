---
 layout: page
 title: diameter of an n-simplex
 permalink: /chicago/diameter_of_an_n-simplex
---
The **diamteter** of an [n-simplex](https://mathgloss.github.io/MathGloss/chicago/n-simplex) $[v_0,\dots,v_n]$ is the maximum distance (in the [ambient](https://mathgloss.github.io/MathGloss/chicago/Euclidean_inner_product) [Euclidean](https://mathgloss.github.io/MathGloss/chicago/########################Euclidean) [metric](https://mathgloss.github.io/MathGloss/chicago/metric_space) [inner product induces metric](https://mathgloss.github.io/MathGloss/chicago/inner_product_induces_metric)) between any of its vertices.

This is equivalent to the [diameter](https://mathgloss.github.io/MathGloss/chicago/diameter_of_a_set) of the [n-simplex](https://mathgloss.github.io/MathGloss/chicago/n-simplex) when considered as a set because the distance between two points $v$ and $\sum_i t_iv_i$ of $[v_0,\dots,v_n]$ satisfies $$\begin{align*}\left{\vert}v-\sum_i t_iv_i\right{\vert} &= \left{\vert}\sum_it_i(v-v_i)\right{\vert} \\&\leq \sum_i t_i {\vert}v-v_i{\vert} \\&\leq \sum_i t_i\max
{\vert}v-v_i{\vert}\\& = \max{\vert}v-v_i{\vert}.\end{align*}$$