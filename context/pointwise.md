---
layout: page
title: pointwise
permalink: /context/pointwise
---
Left Kan extensions are dual to right Kan extensions, not under reversal of the direction of functors (the morphisms in $\textup{\textsf{CAT}}$), but under reversal of the direction of natural transformations (the 2-morphisms in the 2-category $\textup{\textsf{CAT}}$). A left Kan extension may be converted to a right Kan extension by ``replacing every category by its opposite'': a functor $K : \mathsf{C} \to \mathsf{D}$ is equally a functor $K : \mathsf{C}^\mathrm{op} \to \mathsf{D}^\mathrm{op}$ but the process of replacing each category by its opposite reverses the direction of  natural transformations, because their components are morphisms in the opposites of the target categories.\footnote{Succinctly, ``op'' is a 2-functor $(-)^\mathrm{op} : \textup{\textsf{CAT}}^\mathrm{co} \to \textup{\textsf{CAT}}$, where ``co'' is used to denote the dual of a 2-category obtained by reversing the direction of the 2-morphisms but not the 1-morphisms.} A left Kan extension is **pointwise**, if the corresponding right Kan extension is pointwise:

SUGGESTION: pointwise Kan extension

From [Category Theory in Context](https://mathgloss.github.io/MathGloss/context.html)