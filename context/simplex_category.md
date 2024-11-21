---
layout: page
title: simplex category
permalink: /context/simplex_category.md
---
-  Presheaves on the category $\DDelta$, of finite non-empty ordinals and order-preserving maps, are called **simplicial sets**. $\DDelta$ is also called the **simplex category**. The ordinal $n+1 = \{0,1,\ldots, n\}$ may be thought of as a direct version of  the topological $n$-simplex and, with this interpretation in mind, is typically denoted by ``$[n]$'' by algebraic topologists.



The following result, which appears immediately after functors are first defined in \cite{EM-natural}, is arguably the first lemma in category theory.

 Functors preserve isomorphisms.


Consider a functor $F : \mathsf{C} \to \mathsf{D}$ and an isomorphism $f : x \to y$ in $\mathsf{C}$ with inverse $g : y \to x$. Applying the two functoriality axioms:
$ F(g) F(f) = F(gf) = F(1_x) = 1_{Fx}\rlap{{,}.}$ Thus, $Fg : Fy \to Fx$ is a left inverse to $Ff : Fx \to Fy$. Exchanging the roles of $f$ and $g$ (or arguing by duality) shows that $Fg$ is also a right inverse.


  Let $G$ be a group, regarded as a one-object category $\mathsf{B} G$. A functor $X : \mathsf{B} G \to \mathsf{C}$ specifies an object $X \in \mathsf{C}$ (the unique object in its image) together with an endomorphism $g_* : X \to X$ for each $g \in G$. This assignment must satisfy two conditions:

SUGGESTION: group object