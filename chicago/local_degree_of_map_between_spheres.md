---
 layout: page
 title: local degree of map between spheres
 permalink: /chicago/local_degree_of_map_between_spheres
---
Let $f:S^n\to S^n$ be a [continuous](https://defsmath.github.io/DefsMath/classification_of_group_homomorphisms_Z_to_G) function such that for some $y\in S^n$, the [preimage](https://defsmath.github.io/DefsMath/continuous) $f^{-1}(y)$ is finite. Denote the elements of $f^{-1}(y)$ by $\{x_i\}_{i=1}^m$. Let $\{U_i\}_{i=1}^m$ be disjoint [neighborhoods](https://defsmath.github.io/DefsMath/preimage) of the $x_i$. Then $f$ maps each $U_i$ into a [neighborhood](https://defsmath.github.io/DefsMath/neighborhood) $V$ of $y$. Then $$f(U_i \setminus \{x_i\}) \subset B\setminus \{y\}$$ for all $y$ and the following diagram of [homology groups](https://defsmath.github.io/DefsMath/neighborhood) and [relative homology groups](https://defsmath.github.io/DefsMath/homology_group) [commuptes](https://defsmath.github.io/DefsMath/relative_homology_groups):

![Screen Shot 2021-12-02 at 10.44.27 AM.png](https://defsmath.github.io/DefsMath/commutative_diagram)

where all of the maps are "obvious:" $k_i$ and $p_i$ are induced by inclusion. The two [isomorphisms](https://defsmath.github.io/DefsMath/group_homomorphism) on the top of the diagram come from the [Excision Theorem](https://defsmath.github.io/DefsMath/Excision_Theorem) and the two on the bottom come from the [long exact sequence of a pair](https://defsmath.github.io/DefsMath/long_exact_sequence_of_a_pair).

The top two [groups](https://defsmath.github.io/DefsMath/group) are [then](https://defsmath.github.io/DefsMath/reduced_homology_of_the_sphere) [isomorphic](https://defsmath.github.io/DefsMath/###################isomorphic) to $H_n(S^n) \approx\mathbb Z$, so the top [homomorphism](https://defsmath.github.io/DefsMath/###################homomorphism) [is then](https://defsmath.github.io/DefsMath/classification_of_group_homomorphisms_Z_to_G) multiplication by an integer $d$. This integer is the **local degree** of $f$ at $x_i$, written $\text{deg}(f)_{|x_i}$.

