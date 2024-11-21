---
layout: page
title: monoidal category
permalink: /context/monoidal_category.md
---
 The diagrams in Definition \ref{defn:monad} are reminiscent of the diagrams in Definition \ref{defn:monoid-cases}. This is no coincidence. Monads, like (topological) monoids, unital rings, and $\mathbbe{k}$-algebras, are all instances of \emph{monoids in a monoidal category}. A **monoidal category** $\mathsf{V}$ is a category equipped with a binary functor $\mathsf{V} \times \mathsf{V} \to \mathsf{V}$ and a unit object, together with some additional coherence natural isomorphisms satisfying conditions that are described in \S\ref{sec:monoidal}.  A monad on $\mathsf{C}$ is precisely a monoid in the monoidal category $\mathsf{C}^\mathsf{C}$ of endofunctors on $\mathsf{C}$, where the binary functor $\mathsf{C}^\mathsf{C} \times \mathsf{C}^\mathsf{C} \to \mathsf{C}^\mathsf{C}$ is composition, and the unit object is the identity endofunctor $1_\mathsf{C} \in \mathsf{C}^\mathsf{C}$. The category of endofunctors is a \emph{strict} monoidal category, in which the coherence natural isomorphisms can be taken to be identities. Nonetheless, the notion of monoid in a monoidal category is rather more complicated than the notion of monad on a category, which is the point of the following joke from Iry's ``A Brief, Incomplete, and Mostly Wrong History of Programming Languages'' \cite{Iry:2009ab}:

1990---A committee formed by Simon Peyton-Jones, Paul Hudak, Philip Wadler, \ldots creates Haskell, a pure, non-strict, functional language. Haskell gets some resistance due to the complexity of using monads to control side effects. Wadler tries to appease critics by explaining that ``a monad is a monoid in the category of endofunctors, what's the problem?''



SUGGESTION: monoidal category