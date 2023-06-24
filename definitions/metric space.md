---
aliases: metric, triangle inequality
---
A **metric space** is a set $X$ together with a function $\rho: X\times X \to \mathbb R$ such that for all $x,y,z \in X$, the following properties are satisfied:
1. $\rho(x,y) = 0$ if and only if $x=y$.
2. $\rho(x,y) = \rho(y,x)$.
3. $\rho(x,z) \leq \rho(x,y) + \rho(y,z)$. 

Property 3 is called the **triangle inequality**and the function $\rho$ is called a **metric**. The metric generates a [[topological space|topology]] on $X$ where the [[open]] sets $G$ are those for which there exists $\varepsilon > 0$  for all $x \in G$ such that $\{y\in X\mid \rho(x,y) < \varepsilon\}\subset G$.

https://www.wikidata.org/wiki/Q180953