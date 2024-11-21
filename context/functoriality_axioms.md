---
layout: page
title: functoriality axioms
permalink: /context/functoriality_axioms.md
---
 A **contravariant functor** $F$ from $\mathsf{C}$ to $\mathsf{D}$ is a functor $F : \mathsf{C}^\mathrm{op} \to \mathsf{D}$.\footnote{In this text, a contravariant functor $F$ from $\mathsf{C}$ to $\mathsf{D}$ will always be written as $F : \mathsf{C}^\mathrm{op} \to \mathsf{D}$. Some mathematicians omit the ``op'' and let the context or surrounding verbiage convey the variance. We think this is bad practice, as the co- or contravariance is an essential part of the data of a functor, which is not necessarily determined by its assignation on objects. More to the point, we find that this notational convention helps mitigate the consequences of temporary distraction. Seeing $F : \mathsf{C}^\mathrm{op} \to \mathsf{D}$ written on a chalkboard immediately conveys that $F$ is a contravariant functor from $\mathsf{C}$ to $\mathsf{D}$, even to the most spaced-out observer. A similar principle will motivate other notational conventions  introduced in Definition \ref{defn:pullback} and Notation \ref{ntn:adjoints}.}
 Explicitly, this consists of the following data:

-   An object $Fc \in \mathsf{D}$, for each object $c \in \mathsf{C}$.
-  A morphism $Ff : Fc' \to Fc \in \mathsf{D}$, for each morphism $f : c \to c' \in \mathsf{C}$, so that the domain and codomain of $Ff$ are, respectively, equal to $F$ applied to the codomain or domain of $f$.

The assignments are required to satisfy the following two **functoriality axioms**:

-  For any composable pair $f,g$ in $\mathsf{C}$, $Ff \cdot Fg = F(g \cdot f)$.
-  For each object $c$ in $\mathsf{C}$, $F(1_c) = 1_{Fc}$.



SUGGESTION: functoriality axioms