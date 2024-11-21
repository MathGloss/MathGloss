---
layout: page
title: monadic over
permalink: /context/monadic_over
---
Recall that a category $\mathsf{A}$ is **monadic over** $\mathsf{C}$ if there is an adjunction
$ \xymatrix{ \mathsf{C} \ar@<1ex>[r]^F \ar@{}[r]|\perp &\mathsf{A} \ar@<1ex>[l]^U}$  that is equivalent to the adjunction between $\mathsf{C}$ and the category of algebras for the monad $UF$. By Theorem \ref{thm:monadicity}, this is the case if and only if the functor $U : \mathsf{A} \to \mathsf{C}$ creates coequalizers of $U$-split pairs, a somewhat strange technical condition that can be relatively practical to check. Our aim in this section is to present a few results from categorical universal algebra, which describe some of the common features of categories that are equivalent to categories of algebras. In particular, these properties hold for $\textup{\textsf{Set}}_*$, $\textup{\textsf{Monoid}}$, $\textup{\textsf{Group}}$, $\textup{\textsf{Ab}}$, $\textup{\textsf{Ring}}$,  $\textup{\textsf{CRing}}$, $\textup{\textsf{Mod}}_R$,  $\textup{\textsf{Aff}}_\mathbbe{k}$, $\textup{\textsf{Set}}^{\mathsf{B} G}$, $\textup{\textsf{Lattice}}$, and $\textup{\textsf{cHaus}}$, all of which are monadic over $\textup{\textsf{Set}}$,\footnote{For ease of exposition, these applications are focused on categories that are monadic over sets, but the categorical results apply to monads acting on any category, and more sophisticated applications frequently take advantage of this.
} and sometimes fail for $\textup{\textsf{Poset}}$, $\textup{\textsf{Top}}$, and $\textup{\textsf{Field}}$,  which are not.\footnote{The functor $U : \textup{\textsf{Field}} \to \textup{\textsf{Set}}$ cannot be monadic: Example \ref{ex:field-no-adjoint} observes that it fails to admit any adjoints. Proofs that the forgetful functors $U : \textup{\textsf{Poset}} \to \textup{\textsf{Set}}$ and $U : \textup{\textsf{Top}} \to \textup{\textsf{Set}}$ are not monadic will appear shortly.}

SUGGESTION: monadic category

From [Category Theory in Context](https://mathgloss.github.io/MathGloss/context.html)