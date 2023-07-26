---
 layout: page
 title: local degree of map between spheres
 permalink: /chicago/local_degree_of_map_between_spheres
---
Let $f:S^n\to S^n$ be a [continuous](https://mathgloss.github.io/MathGloss/classification_of_group_homomorphisms_Z_to_G) function such that for some $y\in S^n$, the [preimage](https://mathgloss.github.io/MathGloss/continuous) $f^{-1}(y)$ is finite. Denote the elements of $f^{-1}(y)$ by $\{x_i\}_{i=1}^m$. Let $\{U_i\}_{i=1}^m$ be disjoint [neighborhoods](https://mathgloss.github.io/MathGloss/preimage) of the $x_i$. Then $f$ maps each $U_i$ into a [neighborhood](https://mathgloss.github.io/MathGloss/neighborhood) $V$ of $y$. Then $$f(U_i \setminus \{x_i\}) \subset B\setminus \{y\}$$ for all $y$ and the following diagram of [homology groups](https://mathgloss.github.io/MathGloss/neighborhood) and [relative homology groups](https://mathgloss.github.io/MathGloss/homology_group) [commuptes](https://mathgloss.github.io/MathGloss/relative_homology_groups):

![Screen Shot 2021-12-02 at 10.44.27 AM.png](https://mathgloss.github.io/MathGloss/commutative_diagram)

where all of the maps are "obvious:" $k_i$ and $p_i$ are induced by inclusion. The two [isomorphisms](https://mathgloss.github.io/MathGloss/group_homomorphism) on the top of the diagram come from the [Excision Theorem](https://mathgloss.github.io/MathGloss/Excision_Theorem) and the two on the bottom come from the [long exact sequence of a pair](https://mathgloss.github.io/MathGloss/long_exact_sequence_of_a_pair).

The top two [groups](https://mathgloss.github.io/MathGloss/group) are [then](https://mathgloss.github.io/MathGloss/reduced_homology_of_the_sphere) [isomorphic](https://mathgloss.github.io/MathGloss/###################isomorphic) to $H_n(S^n) \approx\mathbb Z$, so the top [homomorphism](https://mathgloss.github.io/MathGloss/###################homomorphism) [is then](https://mathgloss.github.io/MathGloss/classification_of_group_homomorphisms_Z_to_G) multiplication by an integer $d$. This integer is the **local degree** of $f$ at $x_i$, written $\text{deg}(f)_{|x_i}$.

