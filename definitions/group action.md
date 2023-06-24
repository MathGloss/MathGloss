---
aliases: acting, G-set
---
A **group action** of a [[group]] $G$ on a set $X$ is a map $G\times A\to A$ such that 
1. $g_1\cdot(g_2\cdot x)= (g_1g_2)\cdot x$ for all $g_1,g_2\in G$ and for all $x\in X$;
2. $e\cdot x = x$ for all $x\in X$.

Equivalently, we can describe a group action in terms of the [[homomorphism]] $\rho:G\to S_X$ (to the [[symmetric group]] on $X$) given by $\rho(g) = \sigma_g$ where $\sigma_g \in S_X$ is such that $x\mapsto g\cdot x$ under $\sigma_g$. 

When thinking of the [[group]] $G$ as a [[groupoid]] with a single object, then a left action of $G$ is the same as a covariant [[functor]] $G\to \mathcal S$ from $G$ to the [[category of sets]] while a right action is like a contravariant [[functor]]. 

https://www.wikidata.org/wiki/Q288465