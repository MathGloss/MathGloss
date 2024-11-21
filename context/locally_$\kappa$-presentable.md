---
layout: page
title: locally $\kappa$-presentable
permalink: /context/locally_$\kappa$-presentable.md
---
 Let $\kappa$ be a regular cardinal.\footnote{A  **regular cardinal** is an infinite cardinal $\kappa$ with the property that every union of fewer than $\kappa$ sets each of cardinality less than $\kappa$ has cardinality less than $\kappa$.} A locally small category $\mathsf{C}$ is **locally $\kappa$-presentable** if it is cocomplete and if it has a set of objects $S$ so that:

-  Every object in $\mathsf{C}$ can be written as a colimit of a diagram valued in the subcategory spanned by the objects in $S$.
-  For each object $s \in S$, the functor $\mathsf{C}(s,-) : \mathsf{C} \to \textup{\textsf{Set}}$ preserves $\kappa$-filtered colimits.

A functor between locally $\kappa$-presentable categories is **accessible** if it preserves $\kappa$-filtered colimits.


SUGGESTION: locally $\kappa$-presentable category