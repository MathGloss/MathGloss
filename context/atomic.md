---
layout: page
title: atomic
permalink: /context/atomic
---
The adjunction supplies a natural bijection between functors $F(G) \to \mathsf{C}$ and morphisms $G \to U(\mathsf{C})$ of directed graphs. A functor $F(G) \to \mathsf{C}$, or equally a directed graph morphism $G \to U(\mathsf{C})$,  defines a diagram in $\mathsf{C}$ with no commutativity requirements, since directed graphs do not encode composites. The data of such a diagram is uniquely determined by the images of the vertices and edges in the directed graph $G$. These edges form **atomic** arrows in the category $F(G)$, admitting no non-trivial factorizations. For instance, as described in Example \ref{exs:abstract-categories}\eqref{itm:ordinal}, the category $\bbomega$ is free on the directed graph whose vertices are indexed by natural numbers and with edges $n \to n+1$. On account of the adjunction, an $\bbomega$-indexed diagram is defined by specifying only the images of the atomic arrows, from an ordinal to its successor.


SUGGESTION: atomic arrow

From [Category Theory in Context](https://mathgloss.github.io/MathGloss/context.html)