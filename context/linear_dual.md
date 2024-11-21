---
layout: page
title: linear dual
permalink: /context/linear_dual
---
Any finite-dimensional $\mathbbe{k}$-vector space $V$ is isomorphic to its **linear dual**, the vector space $V^* = \mathrm{Hom}(V,\mathbbe{k})$ of linear maps $V \to \mathbbe{k}$, because these vector spaces have the same dimension. This can be proven through the construction of an explicit **dual basis**: choose a basis $e_1,\ldots, e_n$ for $V$ and then define $e_1^*,\ldots, e_n^* \in V^*$ by $ e_i^*(e_j) =   1 & i = j \\ 0 & i \neq j. $ The collection $e_1^*,\ldots, e_n^*$ defines a basis for $V^*$ and the map $e_i \mapsto e_i^*$ extends by linearity to define an isomorphism $V \mathrm{co}ng V^*$.

SUGGESTION: linear dual

From [Category Theory in Context](https://mathgloss.github.io/MathGloss/context.html)