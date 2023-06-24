---
 layout: page
 title: absolute convergence
 permalink: /chicago/absolute_convergence
---
Let $A$ be a [Banach algebra](https://defsmath.github.io/DefsMath/Banach_algebra) with [norm](https://defsmath.github.io/DefsMath/norm) $|\cdot |$. Given a sequence $\{a_i\}_{i\in \mathbb N}$ of elements of $A$, we say that the series $$\sum_{i=1}^\infty a_i$$ is **absolutely convergent** if $$\sum_{i=1}^\infty |a_i| <\infty,$$ i.e. if the series $\{|a_i|\}_{i\in\mathbb N}$ is [convergent](https://defsmath.github.io/DefsMath/series_convergence) as real numbers.

This means that the partial sums $$\sum_{i=1}^n a_i$$ form a [Cauchy sequence](https://defsmath.github.io/DefsMath/Cauchy_sequence) in $A$, which is [complete](https://defsmath.github.io/DefsMath/complete_metric_space), and therefore must have a limit in $A$. We denote this limit by the infinite sum. 