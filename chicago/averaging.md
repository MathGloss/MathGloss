---
 layout: page
 title: averaging
 permalink: /chicago/averaging
---
Let $G$ be a [compact](https://defsmath.github.io/DefsMath/compact) [topological group](https://defsmath.github.io/DefsMath/topological_group) [acting](https://defsmath.github.io/DefsMath/group_action) [continuously](https://defsmath.github.io/DefsMath/continuous) on a [topological space](https://defsmath.github.io/DefsMath/topological_space) $X$. Let $f$ be a [continuous](https://defsmath.github.io/DefsMath/continuous) function $X\to \mathbb C$. An **averaging** of $f$ is a [continuous](https://defsmath.github.io/DefsMath/continuous) function $\text{Av}(f)$ on $X$ given by $$\text{Av}(f)(x) = \frac{1}{\text{vol}(G)} \int_G f(g\cdot x)\text dx$$ where $\text{vol}(G)$ is the [volume](https://defsmath.github.io/DefsMath/volume_of_compact_topological_space) of $G$ and the integral is the [Haar integral](https://defsmath.github.io/DefsMath/Haar_integral) on $G$. 

Note that for a finite [group](https://defsmath.github.io/DefsMath/group) $G$, which is [necessarily](https://defsmath.github.io/DefsMath/finite_sets_are_compact) [compact](https://defsmath.github.io/DefsMath/compact), we have simply $\text{Av}(f)(x) = \frac{1}{|G|} \sum_{g\in G}f(gx)$. 