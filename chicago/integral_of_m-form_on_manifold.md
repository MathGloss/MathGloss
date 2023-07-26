---
 layout: page
 title: integral of m-form on manifold
 permalink: /chicago/integral_of_m-form_on_manifold
---
Let $M\subset\mathbb R^n$ be a [compact](https://mathgloss.github.io/MathGloss/compact), [oriented](https://mathgloss.github.io/MathGloss/oriented_manifold) [embedded m-dimensional manifold with boundary](https://mathgloss.github.io/MathGloss/embedded_m-dimensional_manifold_with_boundary). Let $U$ be an [open](https://mathgloss.github.io/MathGloss/open) set containing $M$ and $\omega$ an [m-form](https://mathgloss.github.io/MathGloss/differential_k-form) on $U$. 

For each $p \in M$, choose a smooth [local parametrization](https://mathgloss.github.io/MathGloss/local_parametrization) $\phi_p: U_p \to M$ [compatible](https://mathgloss.github.io/MathGloss/compatibility_with_orientation) with the [orientation](https://mathgloss.github.io/MathGloss/orientation) on $M$. Then the image $\phi_p(U_p)$ is an [open](https://mathgloss.github.io/MathGloss/open) subset of $M$, so there exists an [open](https://mathgloss.github.io/MathGloss/open) set $V_p \subset \mathbb R^n$ such that $\phi_p(U_p) = V_p \cap M$ because of the [subspace topology](https://mathgloss.github.io/MathGloss/subspace_topology). Since $M$ is [compact](https://mathgloss.github.io/MathGloss/compact), finitely many of these $V_p$ cover $M$. Call them $V_i$ for $1\leq i \leq k$. Then $$V = \bigcup\limits_{i=1}^k V_i$$ is an [open](https://mathgloss.github.io/MathGloss/open) set containing $M$. 

[Let](https://mathgloss.github.io/MathGloss/existence_of_partitions_of_unity) $\{\psi_j\}$ be a [partition of unity](https://mathgloss.github.io/MathGloss/partition_of_unity) subordinate to the $V_i$. Then $\omega = \sum_{j} \psi_j \omega$, so define $$\int_M \omega = \sum_{j} \psi_j\omega.$$ todo 

