---
 layout: page
 title: integral of m-form on manifold
 permalink: /integral_of_m-form_on_manifold
---
Let $M\subset\mathbb R^n$ be a [compact](https://defsmath.github.io/DefsMath/compact), [oriented](https://defsmath.github.io/DefsMath/oriented_manifold) [embedded m-dimensional manifold with boundary](https://defsmath.github.io/DefsMath/embedded_m-dimensional_manifold_with_boundary). Let $U$ be an [open](https://defsmath.github.io/DefsMath/open) set containing $M$ and $\omega$ an [m-form](https://defsmath.github.io/DefsMath/differential_k-form) on $U$. 

For each $p \in M$, choose a smooth [local parametrization](https://defsmath.github.io/DefsMath/local_parametrization) $\phi_p: U_p \to M$ [compatible](https://defsmath.github.io/DefsMath/compatibility_with_orientation) with the [orientation](https://defsmath.github.io/DefsMath/orientation) on $M$. Then the image $\phi_p(U_p)$ is an [open](https://defsmath.github.io/DefsMath/open) subset of $M$, so there exists an [open](https://defsmath.github.io/DefsMath/open) set $V_p \subset \mathbb R^n$ such that $\phi_p(U_p) = V_p \cap M$ because of the [subspace topology](https://defsmath.github.io/DefsMath/subspace_topology). Since $M$ is [compact](https://defsmath.github.io/DefsMath/compact), finitely many of these $V_p$ cover $M$. Call them $V_i$ for $1\leq i \leq k$. Then $$V = \bigcup\limits_{i=1}^k V_i$$ is an [open](https://defsmath.github.io/DefsMath/open) set containing $M$. 

[Let](https://defsmath.github.io/DefsMath/existence_of_partitions_of_unity) $\{\psi_j\}$ be a [partition of unity](https://defsmath.github.io/DefsMath/partition_of_unity) subordinate to the $V_i$. Then $\omega = \sum_{j} \psi_j \omega$, so define $$\int_M \omega = \sum_{j} \psi_j\omega.$$ todo 

