---
aliases: pole, removable singularity, essential singularity
---
Let $f:U\setminus\{a\}\to \mathbb C$ be [[holomorphic]] on the [[open]] set $C\setminus \{a\}$ except at $a$. Then $a$ is an **isolated singularity** of $f$ and can be one of the following:
1. $a$ is a **removable singularity** if there exists a [[holomorphic]] function $g:U\to \mathbb C$ such that $f(z) = g(z)$ for all $z\in U\setminus a$. Such a function $g$ is a [[continuous]] and [[holomorphic]] extension of $f$ over $a$ as in [[Riemann's theorem on removable singularities]].
2. $a$ can be a **pole** if there exists a [[holomorphic]] function $g:U\to\mathbb C$ with $g(a)\neq 0$ and $n\in\mathbb N$ such that $f(z) = \frac{g(z)}{(z-a)^n}$ for all $z\in U\setminus \{a\}$. The number $n$ is the **order** of the pole.
3. $a$ can be an **essential singularity** of $f$ if it is neither a removable singularity nor a pole. This occurs if and only if the [[Laurent series]] for $f$ has infinitely many nonzero terms in negative degree. That is, if the [[principal part]] is infinite. 