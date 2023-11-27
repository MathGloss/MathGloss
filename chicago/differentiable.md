---
 layout: page
 title: differentiable
 permalink: /chicago/differentiable
---

Let $U \subset \mathbb R^n$ be [open](https://mathgloss.github.io/MathGloss/chicago/open). A function $f: U\to \mathbb R^m$ is **differentiable** at $a \in U$ if there exists a [linear transformation](https://mathgloss.github.io/MathGloss/chicago/linear_transformation) $A:\mathbb R^n \to \mathbb R^m$ such that $$\lim_{h\to 0} \frac{f(a+h)-f(a)-A(h)}{\vert \vert h\vert \vert } = 0.$$ The transformation $A$ is denoted $Df(a)$ and is called the **total derivative** of $f$ at $a$.

Equivalently, let $V$ and $V$' be [vector spaces](https://mathgloss.github.io/MathGloss/chicago/vector_space) with norms $\vert \cdot\vert $ and $\vert \cdot\vert '$, respectively. A function $f:U\to V'$ from $U$ an [open](https://mathgloss.github.io/MathGloss/chicago/open) subset of $V$ is **differentiable** at $x\in U$ if there exists a [linear transformation](https://mathgloss.github.io/MathGloss/chicago/linear_transformation) $d_x f :V\to V'$ called the **differential** of $f$ at $x$ and a small [neighborhood](https://mathgloss.github.io/MathGloss/chicago/neighborhood) $U_x\subseteq U$ of $x$ such that for all $v\in U$, we have that $$f(x+v) = f(x) + d_x(f) + o(v)$$ where $o: U_x\to V'$ is a map such that $$\lim_{\vert v\vert \to 0} \frac{\vert o(v)\vert '}{\vert v\vert } = 0.$$

Wikidata ID: [Q636889](https://www.wikidata.org/wiki/Q636889)