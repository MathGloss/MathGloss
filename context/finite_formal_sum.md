---
layout: page
title: finite formal sum
permalink: /context/finite_formal_sum
---
A more interesting challenge is to reverse the direction of this translation and build a vector space from a set $S$. Cardinality restrictions might prevent the direct use of $S$ as the set of vectors for a $\mathbbe{k}$-vector space, and even without this obstruction there is no natural way to define vector addition in $S$.
Instead, a more natural way to build a vector space  is to let the elements of $S$ serve as a basis: vectors are then finite formal sums\footnote{A precise way to define what is meant by this informal phrase is to say that a **finite formal sum** is a finitely supported function $\phi : S \to \mathbbe{k}$, corresponding to the expression $\sum_{s \in S} \phi(s) s$. In particular, two finite sums are considered to be identical when they differ only up to reordering of terms, up to consolidating repeated instances of the same term by adding their coefficients, or up to inclusion or deletion of terms whose coefficients are zero.}  $k_1s_1 + \cdots + k_n s_n$ with $k_i \in \mathbbe{k}$,  $s_i \in S$, and $n \geq 0$. This defines a vector space $\mathbbe{k}[S]$ whose dimension is equal to the cardinality of $S$, called the **free vector space on the set** $S$. Moreover, as our use of the adjective ``natural'' would suggest,  this construction is functorial, defining a functor $\mathbbe{k}[-] : \textup{\textsf{Set}} \to \textup{\textsf{Vect}}_\mathbbe{k}$: a function $f : S \to T$ induces a linear map $\mathbbe{k}[f] : \mathbbe{k}[S] \to \mathbbe{k}[T]$ defined on the basis elements in the evident way.

SUGGESTION: finite formal sum

From [Category Theory in Context](https://mathgloss.github.io/MathGloss/context.html)