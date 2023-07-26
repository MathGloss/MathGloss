---
 layout: page
 title: elementary symmetric polynomials
 permalink: /chicago/elementary_symmetric_polynomials
---
Let $R$ be a [ring](https://mathgloss.github.io/MathGloss/chicago/ring) and let $R[x_1,\dots,x_n]$ be the [polynomial ring](https://mathgloss.github.io/MathGloss/chicago/polynomial_ring) in $n$ variables. Then the **elementary symmetric polynomials** are 
$$\begin{align*}e_1(x_1,\dots,x_n) &= \sum_{1\leq j\leq n} x_j \\ e_2(x_1,\dots,x_n) &= \sum_{1\leq j < k \leq n} x_jx_k \\e_3(x_1,\dots, x_n) &=\sum_{1\leq j < k < \ell\leq n} x_jx_kx_\ell\\&\quad\vdots\\e_n(x_1,\dots,x_n) &= x_1x_2\cdots x_n.\end{align*}$$ In general, $$e_k(x_1,\dots,x_n) = \sum_{1\leq j_1<j_2<\cdots < j_k \leq n} x_{j_1}\cdots x_{j_k}$$ for $1\leq k\leq n$. They are [symmetric polynomials](https://mathgloss.github.io/MathGloss/chicago/symmetric_polynomial).