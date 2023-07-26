---
 layout: page
 title: homology group
 permalink: /chicago/homology_group
---

Consider a [chain complex](https://mathgloss.github.io/MathGloss/chicago/chain_complex) with [abelian](https://mathgloss.github.io/MathGloss/chicago/abelian) [groups](https://mathgloss.github.io/MathGloss/chicago/group) $C_i$ and [homomorphisms](https://mathgloss.github.io/MathGloss/chicago/group_homomorphism) $\partial_i$. Because $\partial_{k+1}\circ\partial_k = 0$ for all $k$, the [image](https://mathgloss.github.io/MathGloss/chicago/image) of $\partial_{k=1}$ is a subset of the [kernel of kernel](https://mathgloss.github.io/MathGloss/chicago/kernel_of_###################kernel) of $\partial_k$: $$\text{Im}(\partial_{k+1})\subset \text{Ker}(\partial_k).$$ The $n$th **homology group** of the chain complex is the [quotient by subquotient group](https://mathgloss.github.io/MathGloss/chicago/quotient_by_sub######quotient_group) $$H_n = \text{Ker}(\partial_n)/\text{Im}(\partial_{n+1}).$$ 

Elements of $\text{Ker}(\partial_n)$ are called **cycles** and elements of $\text{Im}(\partial_{n+1})$ are called **boundaries**.

Wikidata ID: [Q1144780](https://www.wikidata.org/wiki/Q1144780)