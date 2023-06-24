---
 layout: page
 title: Laurent series
 permalink: /chicago/laurent_series
---
Let $f:A\to \mathbb C$ be a function [holomorphic](https://defsmath.github.io/DefsMath/holomorphic) on the [annulus](https://defsmath.github.io/DefsMath/annulus) $A$. Then $f(z)$ can be written as the **Laurent series** $$f(z) = \sum_{n=-\infty}^\infty a_n (z-c)^n$$ for $a_n,c\in \mathbb C$ and $a_n$ given by $$a_n = \frac{1}{2\pi i} \int_\gamma \frac{f(z)}{(z-c)^{n+1}}\text dz$$ for $\gamma$ a positively-oriented piecewise [continuously differentiable](https://defsmath.github.io/DefsMath/class) [loop](https://defsmath.github.io/DefsMath/loop) in $A$.