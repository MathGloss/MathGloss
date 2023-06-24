---
aliases: total derivative
---
Let $U \subset \mathbb R^n$ be [[open]]. A function $f: U\to \mathbb R^m$ is **differentiable** at $a \in U$ if there exists a [[linear transformation]] $A:\mathbb R^n \to \mathbb R^m$ such that $$\lim_{h\to 0} \frac{f(a+h)-f(a)-A(h)}{||h||} = 0.$$ The transformation $A$ is denoted $Df(a)$ and is called the **total derivative** of $f$ at $a$.

Equivalently, let $V$ and $V$' be [[vector space|vector spaces]] with norms $|\cdot|$ and $|\cdot|'$, respectively. A function $f:U\to V'$ from $U$ an [[open]] subset of $V$ is **differentiable** at $x\in U$ if there exists a [[linear transformation]] $d_x f :V\to V'$ called the **differential** of $f$ at $x$ and a small [[neighborhood]] $U_x\subseteq U$ of $x$ such that for all $v\in U$, we have that $$f(x+v) = f(x) + d_x(f) + o(v)$$ where $o: U_x\to V'$ is a map such that $$\lim_{|v|\to 0} \frac{|o(v)|'}{|v|} = 0.$$

https://www.wikidata.org/wiki/Q636889