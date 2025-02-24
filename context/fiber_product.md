---
layout: page
title: fiber product
permalink: /context/fiber_product
---
 A **pullback** is a limit of a diagram indexed by the poset category $\bullet \to \bullet \leftarrow \bullet$ comprised of two non-identity morphisms with common codomain. Writing $f$ and $g$ for the morphisms defining the image of a diagram of this shape in a category $\mathsf{C}$, a cone with summit $D$ consists of a triple of morphisms, one for each object in the indexing category, so that both triangles in the diagram
 \xymatrix{ D \ar[d]_b \ar[r]^c \ar[dr]^a & C \ar[d]^g \\ B \ar[r]_f  & A}  commute; the two triangles  represent the two naturality conditions \eqref{eq:cone-naturality} imposed by the non-identity morphisms in the indexing category. The leg $a$ asserts that $gc$ and $fb$ have a common composite. Thus, the data of a cone over $B \xrightarrow{f} A \xleftarrow{g} C$ may be described more simply as a pair of morphisms $B \xleftarrow{b} D \xrightarrow{c} C$ defining a commutative square.

The pullback, the universal cone over $f$ and $g$, is a commutative square $fh=gk$ with the following universal property: given any commutative square \eqref{eq:pullback-cone}, there is a unique factorization of its legs through the summit of the pullback cone:
 \vcenter{\xymatrix{D \ar@/^/[drr]^c \ar@/_/[ddr]_b \ar@{-->}[dr]^{\exists !} \\ & P \ar[d]_h \ar[r]^k \ar@{}[dr]|(.2){\displaystyle\lrcorner} & C \ar[d]^g \\ & B \ar[r]_f & A}} The symbol ``$\lrcorner$'' indicates that the square $gk = fh$ is a pullback, i.e., a limit diagram, and not simply a commutative square. The pullback $P$ is also called the **fiber product** and is frequently denoted by $B \times_A C$. The precise relationship between pullbacks and products is explored in \S\ref{sec:set-limit} and \S\ref{sec:rep-limits}.


SUGGESTION: pullback

From [Category Theory in Context](https://mathgloss.github.io/MathGloss/context.html)