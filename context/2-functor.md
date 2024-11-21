---
layout: page
title: 2-functor
permalink: /context/2-functor.md
---
Definition \ref{defn:adjunction-unit} reveals that an adjunction can be defined internally to the 2-category $\textup{\textsf{CAT}}$ introduced in Definition \ref{defn:2-cat}: an adjunction consists of a pair of objects, a pair of 1-morphisms, and a pair of 2-morphisms satisfying certain composition relations. Now a **2-functor** is a morphism between 2-categories: a map on objects, 1-morphisms, and 2-morphisms preserving composition and identities at all levels. There is a 2-dimensional analog of Lemma \ref{lem:functors-pres-commutativity}---that functors preserve commutative diagrams---which says that 2-functors preserve ``2-dimensional diagrams'' including, in particular, adjunctions. Ignoring size issues, Proposition \ref{prop:whiskering-adjunction} is an immediate corollary of the fact that
$ (-)^\mathsf{J} : \textup{\textsf{CAT}} \to \textup{\textsf{CAT}} \quad \mathrm{and} \quad \mathsf{E}^{(-)} : \textup{\textsf{Cat}}^\mathrm{op} \to \textup{\textsf{CAT}}$ define 2-functors for any small category $\mathsf{J}$ and locally small category $\mathsf{E}$.

SUGGESTION: 2-functor