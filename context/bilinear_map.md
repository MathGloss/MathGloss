---
layout: page
title: bilinear map
permalink: /context/bilinear_map
---

 Fix $\mathbbe{k}$-vector spaces $V$ and $W$ and consider the functor $\textup{Bilin}(V,W;-) : \textup{\textsf{Vect}}_\mathbbe{k} \to \textup{\textsf{Set}}$ that sends a vector space $U$ to the set of $\mathbbe{k}$-bilinear maps $V \times W \to U$. A **bilinear map** $f : V \times W \to U$ is a function of two variables so that for all $v\in V$, $f(v,-) : W \to U$ is a linear map and for all $w \in W$, $f(-,w) : V \to U$ is a linear map.  Equivalently, by ``currying,'' a bilinear map may be defined to be a linear map $V \to \mathrm{Hom}(W,U)$ or $W \to \mathrm{Hom}(V,U)$, where the codomains are vector spaces of linear maps.

SUGGESTION: bilinear map

From [Category Theory in Context](https://mathgloss.github.io/MathGloss/context.html)