---
 layout: page
 title: holomorph of a group
 permalink: /holomorph_of_a_group
---
The **holomorph** of a [group](https://defsmath.github.io/DefsMath/group) $G$ is in some sense a [group](https://defsmath.github.io/DefsMath/group) that contains a copy of both $G$ itself and the [automorphism group](https://defsmath.github.io/DefsMath/automorphism_group) of $G$. 

Formally, $\text{Hol}(G) = G\rtimes \text{Aut}(G)$ where the [homomorphism](https://defsmath.github.io/DefsMath/group_homomorphism) $\rho: \text{Aut}(G)\to \text{Aut}(G)$ associated to the [semidirect product](https://defsmath.github.io/DefsMath/semidirect_product) is the [identity function](https://defsmath.github.io/DefsMath/identity_function). Thus the product of elements of $\text{Hol}(G)$ is as follows:
$$(g,\alpha)(h,\beta) = (g\alpha(h),\alpha\beta).$$

Equivalently, we can define $\text{Hol}(G) =\{l_g\circ\sigma \mid g\in G, \sigma\in\text{Aut}(G)\}\subset S_G$ where $l_g$ denotes left multiplication by $g$.

Wikidata ID: [Q3139500](https://www.wikidata.org/wiki/Q3139500)