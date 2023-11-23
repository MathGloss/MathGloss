---
 layout: page
 title: averaging
 permalink: /chicago/averaging
---
Let $G$ be a [compact](https://mathgloss.github.io/MathGloss/chicago/compact) [topological group](https://mathgloss.github.io/MathGloss/chicago/topological_group) [acting](https://mathgloss.github.io/MathGloss/chicago/group_action) [continuously](https://mathgloss.github.io/MathGloss/chicago/continuous) on a [topological space](https://mathgloss.github.io/MathGloss/chicago/topological_space) $X$. Let $f$ be a [continuous](https://mathgloss.github.io/MathGloss/chicago/continuous) function $X\to \mathbb C$. An **averaging** of $f$ is a [continuous](https://mathgloss.github.io/MathGloss/chicago/continuous) function $\text{Av}(f)$ on $X$ given by $$\text{Av}(f)(x) = \frac{1}{\text{vol}(G)} \int_G f(g\cdot x)\text dx$$ where $\text{vol}(G)$ is the [volume](https://mathgloss.github.io/MathGloss/chicago/volume_of_compact_topological_space) of $G$ and the integral is the [Haar integral](https://mathgloss.github.io/MathGloss/chicago/Haar_integral) on $G$. 

Note that for a finite [group](https://mathgloss.github.io/MathGloss/chicago/group) $G$, which is [necessarily](https://mathgloss.github.io/MathGloss/chicago/finite_sets_are_compact) [compact](https://mathgloss.github.io/MathGloss/chicago/compact), we have simply $\text{Av}(f)(x) = \frac{1}{|G|} \sum_{g\in G}f(gx)$. 