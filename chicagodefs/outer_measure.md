---
 layout: page
 title: outer measure
 permalink: /outer_measure
---
Let $\mathcal P(X)$ be the [power set](https://defsmath.github.io/DefsMath/power_set) of $X$. An **outer measure** on $X$ is a function $\mu: \mathcal P(X) \to [0,\infty]$ such that
- $\mu(\emptyset) = 0$ 
- if $A, B \subset X$ with $A\subset B$, then $\mu(A) \leq\mu(B)$
- for arbitrary subsets $B_i \subset X$ for $i \in \mathbb N$, we have $\mu\left(\bigcup\limits_{i\in\mathbb N} B_i \right)\leq \sum\limits_{i\in\mathbb N}\mu(B_i)$.
Wikidata ID: [Q258374](https://www.wikidata.org/wiki/Q258374)