---
layout: page
title: comma category
permalink: /context/comma_category
---

Given functors $F : \mathsf{D} \to \mathsf{C}$ and $G : \mathsf{E} \to \mathsf{C}$, show that there is a category, called the **comma category** $F \mathrm{co}mma G$, which has

-  as objects, triples $(d \in \mathsf{D}, e \in \mathsf{E}, f : Fd \to Ge \in \mathsf{C})$, and
-  as morphisms $(d,e,f) \to (d',e',f')$, a pair of morphisms $(h : d \to d', k : e \to e')$ so that the square
$  \xymatrix{ Fd \ar[d]_{Fh} \ar[r]^f & Ge \ar[d]^{Gk} \\ Fd' \ar[r]_{f'} & Ge'}$ commutes in $\mathsf{C}$, i.e., so that $f' \cdot Fh = Gk \cdot f$.

Define a pair of projection functors $\mathrm{dom} : F \mathrm{co}mma G \to \mathsf{D}$ and $\mathrm{cod} : F \mathrm{co}mma G \to \mathsf{E}$.


SUGGESTION: comma category

From [Category Theory in Context](https://mathgloss.github.io/MathGloss/context.html)