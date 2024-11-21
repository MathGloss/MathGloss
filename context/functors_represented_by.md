---
layout: page
title: functors represented by
permalink: /context/functors_represented_by.md
---

If $\mathsf{C}$ is locally small, then for any object $c\in \mathsf{C}$ we may define a pair of covariant and contravariant **functors represented by** $c$:
$ \xymatrix@C=8pt@R=8pt{ \mathsf{C} \ar[rr]^-{\mathsf{C}(c,-)} && \textup{\textsf{Set}} & & \mathsf{C}^\mathrm{op} \ar[rr]^-{\mathsf{C}(-,c)} & & \textup{\textsf{Set}} \\ x \ar[dd]_f & \mapsto & \mathsf{C}(c,x) \ar[dd]^{f_*} & & x \ar[dd]_f & \mapsto & \mathsf{C}(x,c) \\ & \mapsto & & & & \mapsto & \\ y & \mapsto & \mathsf{C}(c,y) & & y & \mapsto & \mathsf{C}(y,c)\ar[uu]_{f^{*}} }$
The notation suggests the action on objects: the functor $\mathsf{C}(c,-)$ carries $x \in \mathsf{C}$ to the set $\mathsf{C}(c,x)$ of arrows from $c$ to $x$ in $\mathsf{C}$. Dually, the functor $\mathsf{C}(-,c)$ carries $x \in \mathsf{C}$ to the set $\mathsf{C}(x,c)$.

The functor $\mathsf{C}(c,-)$ carries a morphism $f : x \to y$ to the post-composition function $f_* : \mathsf{C}(c,x) \to \mathsf{C}(c,y)$ introduced in Lemma \ref{lem:iso}\eqref{lem:iso-post}. Dually, the functor $\mathsf{C}(-,c)$ carries $f$ to the pre-composition function $f^* : \mathsf{C}(y,c) \to \mathsf{C}(x,c)$ introduced in \ref{lem:iso}\eqref{lem:iso-pre}. Note that post-composition defines a \emph{covariant} action on hom-sets, while pre-composition defines a \emph{contravariant} action. There are no choices involved here; post-composition is always a covariant operation, while pre-composition is always a contravariant one. This is just the natural order of things.


SUGGESTION: functor represented by an object