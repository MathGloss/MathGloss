---
 layout: page
 title: isolated singularity
 permalink: /isolated_singularity
---

Let $f:U\setminus\{a\}\to \mathbb C$ be [holomorphic](https://defsmath.github.io/DefsMath/holomorphic) on the [open](https://defsmath.github.io/DefsMath/open) set $C\setminus \{a\}$ except at $a$. Then $a$ is an **isolated singularity** of $f$ and can be one of the following:
1. $a$ is a **removable singularity** if there exists a [holomorphic](https://defsmath.github.io/DefsMath/holomorphic) function $g:U\to \mathbb C$ such that $f(z) = g(z)$ for all $z\in U\setminus a$. Such a function $g$ is a [continuous](https://defsmath.github.io/DefsMath/continuous) and [holomorphic](https://defsmath.github.io/DefsMath/holomorphic) extension of $f$ over $a$ as in [Riemann's theorem on removable singularities](https://defsmath.github.io/DefsMath/Riemann's_theorem_on_removable_singularities).
2. $a$ can be a **pole** if there exists a [holomorphic](https://defsmath.github.io/DefsMath/holomorphic) function $g:U\to\mathbb C$ with $g(a)\neq 0$ and $n\in\mathbb N$ such that $f(z) = \frac{g(z)}{(z-a)^n}$ for all $z\in U\setminus \{a\}$. The number $n$ is the **order** of the pole.
3. $a$ can be an **essential singularity** of $f$ if it is neither a removable singularity nor a pole. This occurs if and only if the [Laurent series](https://defsmath.github.io/DefsMath/Laurent_series) for $f$ has infinitely many nonzero terms in negative degree. That is, if the [principal part](https://defsmath.github.io/DefsMath/principal_part) is infinite. 