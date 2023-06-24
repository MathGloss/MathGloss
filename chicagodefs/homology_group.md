---
 layout: page
 title: homology group
 permalink: /homology_group
---

Consider a [chain complex](https://defsmath.github.io/DefsMath/chain_complex) with [abelian](https://defsmath.github.io/DefsMath/abelian) [groups](https://defsmath.github.io/DefsMath/group) $C_i$ and [homomorphisms](https://defsmath.github.io/DefsMath/group_homomorphism) $\partial_i$. Because $\partial_{k+1}\circ\partial_k = 0$ for all $k$, the [image](https://defsmath.github.io/DefsMath/image) of $\partial_{k=1}$ is a subset of the [kernel of kernel](https://defsmath.github.io/DefsMath/kernel_of_###################kernel) of $\partial_k$: $$\text{Im}(\partial_{k+1})\subset \text{Ker}(\partial_k).$$ The $n$th **homology group** of the chain complex is the [quotient by subquotient group](https://defsmath.github.io/DefsMath/quotient_by_sub######quotient_group) $$H_n = \text{Ker}(\partial_n)/\text{Im}(\partial_{n+1}).$$ 

Elements of $\text{Ker}(\partial_n)$ are called **cycles** and elements of $\text{Im}(\partial_{n+1})$ are called **boundaries**.

Wikidata ID: [Q1144780](https://www.wikidata.org/wiki/Q1144780)