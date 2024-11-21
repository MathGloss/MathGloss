---
layout: page
title: parallel pair
permalink: /context/parallel_pair
---
 An **equalizer** is a limit of a diagram indexed by the **parallel pair**, the category $\bullet \rightrightarrows \bullet$ with two objects and two parallel non-identity morphisms. A diagram of this shape is simply a parallel pair of morphisms $f,g : A \rightrightarrows B$ in the target category $\mathsf{C}$. A cone over this diagram with summit $C$ consists of a pair of morphisms $a : C \to A$ and $b : C \to B$ so that $fa = b$ and $ga = b$; these two equations correspond to the naturality conditions \eqref{eq:cone-naturality} imposed by each of the two non-identity morphisms in the indexing category. Together, they assert that $fa = ga$; the morphism $b$ is necessarily equal to this common composite. Thus, a cone over a parallel pair $f,g : A \rightrightarrows B$ is represented by a single morphism $a : C \to A$ so that $fa = ga$.

The equalizer $h : E \to A$ is the universal arrow with this property. The limit diagram
$ \xymatrix{  E \ar[r]^h & A \ar@<.5ex>[r]^f \ar@<-.5ex>[r]_g & B}$ is  called an **equalizer diagram**. The universal property asserts that given any $a : C \to A$ so that $fa = ga$, there exists a unique factorization $k : C \to E$ of $a$ through $h$.
$ \xymatrix{ C \ar[dr]^a \ar@{-->}[d]^{\exists !}_k \\ E \ar[r]_h & A \ar@<.5ex>[r]^f \ar@<-.5ex>[r]_g & B}$


SUGGESTION: equalizer

From [Category Theory in Context](https://mathgloss.github.io/MathGloss/context.html)