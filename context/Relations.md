---
layout: page
title: Relations
permalink: /context/Relations
---
Any abelian group $A$ has a presentation that can be defined in terms of the free and forgetful functors \eqref{eq:ab-free-forgetful}.  If $G$ is any set of elements of an abelian group $A$, there is a canonical homomorphism $\mathbb{Z}[G] \to A$ that sends a finite $\mathbb{Z}$-linear combination of these elements to the element of $A$ that is their sum. The set $G$ is a set of **generators** for $A$ precisely when this map is surjective. **Relations** involving these generators, meaning the terms that are to be set equal to zero, are elements of the group $\mathbb{Z}[G]$, so again there is a canonical ``evaluation'' homomorphism $\mathbb{Z}[R] \to \mathbb{Z}[G]$ from the free group on a set $R$ of relations to the free group on the generators. The sets  $G \subset A$ of generators and $R \subset \mathbb{Z}[G]$ of relations give a **presentation** of $A$ if the quotient map $\mathbb{Z}[G] \twoheadrightarrow A$ is a coequalizer of the evaluation map and the zero homomorphism
 \vcenter{ \xymatrix@=30pt{\mathbb{Z}[R] \ar@<-.5ex>[r]_-{\mathrm{evaluation}} \ar@<.5ex>[r]^0 & \mathbb{Z}[G] \ar@{->>}[r] & A,}} in which case one often writes $A = \big\langle G \bigm| R \big\rangle$.

SUGGESTION: presentation

From [Category Theory in Context](https://mathgloss.github.io/MathGloss/context.html)