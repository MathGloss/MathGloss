---
 layout: page
 title: averaging of vector-valued function
 permalink: /averaging_of_vector-valued_function
---
Let $G$ be a [compact](https://defsmath.github.io/DefsMath/compact) [topological group](https://defsmath.github.io/DefsMath/topological_group) and let $\int_G$ be an [invariant](https://defsmath.github.io/DefsMath/G-invariant_function) [vector-valued integral](https://defsmath.github.io/DefsMath/vector-valued_integral). Let $\rho$ be a [continuous group representation](https://defsmath.github.io/DefsMath/continuous_group_representation) into the [vector space](https://defsmath.github.io/DefsMath/vector_space) $V$. For a fixed $v\in V$, consider the function $f_v:G\to V$ such that $g\mapsto \rho(g)v$. 

Define a [linear transformation](https://defsmath.github.io/DefsMath/linear_transformation) $\text{Av}_\rho:V\to V$ by the formula $$\text{Av}_\rho(v) = \frac{1}{\text{vol}(G)}\int_G
\rho(g)v\text dg.$$ 

Heuristically, we can say that this is the [barycenter](https://defsmath.github.io/DefsMath/barycenter) of the $G$-[orbit](https://defsmath.github.io/DefsMath/orbit) of $v$. 