---
 layout: page
 title: CW complex
 permalink: /chicago/cw_complex
---
A **CW complex** is a [topological space](https://defsmath.github.io/DefsMath/topological_space) $X$ constructed in the following way: 
1. Consider a discrete set $X^0$ and call its points "0-cells."
2. Form the **$n$-skeleton** $X^n$ from $X^{n-1}$ by attaching $n$-cells $e_\alpha^n$ via maps $\varphi_\alpha:S^{n-1} \to X^{n-1}$. Thus $X^n$ is the [quotient vector space](https://defsmath.github.io/DefsMath/quotient_vector_space) of the disjoint union $X^{n-1}\coprod_\alpha D_\alpha^n$ of $X^{n-1}$ with a collection of disks $D_\alpha^n$ under the [identification](https://defsmath.github.io/DefsMath/equivalence_relation) $x\sim \varphi_\alpha(x)$ for $x\in \partial D_\alpha^n$. As a set, $X^n = X^{n-1}\coprod_\alpha e_\alpha^n$ where each $e_\alpha^n$ is an [open](https://defsmath.github.io/DefsMath/open) $n$-disk.
3. Either stop this process at a finite value of $n$, setting $X=X^n$ or continue indefinitely and endow $X = \bigcup_n X^n$ with the [weak topology](https://defsmath.github.io/DefsMath/weak_topology).


Wikidata ID: [Q189061](https://www.wikidata.org/wiki/Q189061)