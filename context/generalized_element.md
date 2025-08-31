---
layout: page
title: generalized element
permalink: /context/generalized_element
---
Elements of a set $A$ stand in bijection with morphisms $a : 1 \to A$ in the category of sets. By composition, morphisms $f : A \to B$ in the category of sets act on elements: the composite $fa$ encodes the element $f(a)$.\footnote{The standard function notation motivates the usual ``composition order.''} In any category $\mathsf{C}$, a **generalized element** of an object $A$ is a morphism $a : X \to A$ with codomain $A$. Morphisms $f : A \to B$ in $\mathsf{C}$ act on $X$-shaped elements by composition: the composite $fa$ encodes an $X$-shaped generalized element of $B$. In this terminology, the contravariant represented functor $\mathrm{Hom}(-,A) : \mathsf{C}^\mathrm{op} \to \textup{\textsf{Set}}$ sends an object $X$ to the set of $X$-shaped generalized elements of $A$. Since the Yoneda embedding $\mathsf{C} \hookrightarrow \textup{\textsf{Set}}^{\mathsf{C}^\mathrm{op}}$ is fully faithful, no information about $A$ is lost by considering instead the functor $\mathrm{Hom}(-,A)$ of generalized elements of $A$.

SUGGESTION: generalized element

From [Category Theory in Context](https://mathgloss.github.io/MathGloss/context.html)