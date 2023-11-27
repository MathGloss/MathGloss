---
 layout: page
 title: local degree of map between spheres
 permalink: /chicago/local_degree_of_map_between_spheres
---
Let $f:S^n\to S^n$ be a [continuous](https://mathgloss.github.io/MathGloss/chicago/classification_of_group_homomorphisms_Z_to_G) function such that for some $y\in S^n$, the [preimage](https://mathgloss.github.io/MathGloss/chicago/continuous) $f^{-1}(y)$ is finite. Denote the elements of $f^{-1}(y)$ by $\{x_i\}_{i=1}^m$. Let $\{U_i\}_{i=1}^m$ be disjoint [neighborhoods](https://mathgloss.github.io/MathGloss/chicago/preimage) of the $x_i$. Then $f$ maps each $U_i$ into a [neighborhood](https://mathgloss.github.io/MathGloss/chicago/neighborhood) $V$ of $y$. Then $$f(U_i \setminus \{x_i\}) \subset B\setminus \{y\}$$ for all $y$ and the following diagram of [homology groups](https://mathgloss.github.io/MathGloss/chicago/neighborhood) and [relative homology groups](https://mathgloss.github.io/MathGloss/chicago/homology_group) [commuptes](https://mathgloss.github.io/MathGloss/chicago/relative_homology_groups):

![Screen Shot 2021-12-02 at 10.44.27 AM.png](https://mathgloss.github.io/MathGloss/chicago/commutative_diagram)

where all of the maps are "obvious:" $k_i$ and $p_i$ are induced by inclusion. The two [isomorphisms](https://mathgloss.github.io/MathGloss/chicago/group_homomorphism) on the top of the diagram come from the [Excision Theorem](https://mathgloss.github.io/MathGloss/chicago/Excision_Theorem) and the two on the bottom come from the [long exact sequence of a pair](https://mathgloss.github.io/MathGloss/chicago/long_exact_sequence_of_a_pair).

The top two [groups](https://mathgloss.github.io/MathGloss/chicago/group) are [then](https://mathgloss.github.io/MathGloss/chicago/reduced_homology_of_the_sphere) [isomorphic](https://mathgloss.github.io/MathGloss/chicago/###################isomorphic) to $H_n(S^n) \approx\mathbb Z$, so the top [homomorphism](https://mathgloss.github.io/MathGloss/chicago/###################homomorphism) [is then](https://mathgloss.github.io/MathGloss/chicago/classification_of_group_homomorphisms_Z_to_G) multiplication by an integer $d$. This integer is the **local degree** of $f$ at $x_i$, written $\text{deg}(f)_{\vert x_i}$.

