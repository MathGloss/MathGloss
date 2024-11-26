---
layout: page
title: unital ring
permalink: /context/unital_ring
---
 A **topological monoid** is an object $M \in \textup{\textsf{Top}}$ together with morphisms $\mu : M \times M \to M$ and $\eta : 1 \to M$ so that the following diagrams commute:
$ \xymatrix{ M \times M \times M \ar[d]_{\mu \times 1_M} \ar[r]^-{1_M \times \mu} & M \times M \ar[d]^\mu & M \ar[r]^-{\eta \times 1_M} \ar[dr]_{1_M} & M \times M \ar[d]^\mu & M \ar[l]_-{1_M \times \eta} \ar[dl]^{1_M} \\ M \times M \ar[r]_-\mu & M &&  M}$

A **unital ring**\footnote{A not-necessarily unital ring may be defined by ignoring the morphism $\eta$ and the pair of commutative triangles.} is an object $R \in \textup{\textsf{Ab}}$ together with morphisms $\mu : R \otimes_\mathbb{Z}  R \to R$ and $\eta : \mathbb{Z} \to R$ so that the following diagrams commute:
$ \xymatrix{ R \otimes_\mathbb{Z} R \otimes_\mathbb{Z} R \ar[d]_{\mu \otimes_\mathbb{Z} 1_R} \ar[r]^-{1_R \otimes_\mathbb{Z} \mu} & R \otimes_\mathbb{Z} R \ar[d]^\mu & R \ar[r]^-{\eta \otimes_\mathbb{Z} 1_R} \ar[dr]_{1_R} & R \otimes_\mathbb{Z} R \ar[d]^\mu & R \ar[l]_-{1_R \otimes_\mathbb{Z} \eta} \ar[dl]^{1_R} \\ R \otimes_\mathbb{Z} R \ar[r]_-\mu & R &&  R}$

A $\mathbbe{k}$-**algebra** is an object $R \in \textup{\textsf{Vect}}_\mathbbe{k}$  together with morphisms $\mu : R \otimes_\mathbbe{k}  R \to R$ and $\eta : \mathbbe{k} \to R$ so that the following diagrams commute:
$ \xymatrix{ R \otimes_\mathbbe{k} R \otimes_\mathbbe{k} R \ar[d]_{\mu \otimes_\mathbbe{k} 1_R} \ar[r]^-{1_R \otimes_\mathbbe{k} \mu} & R \otimes_\mathbbe{k} R \ar[d]^\mu & R \ar[r]^-{\eta \otimes_\mathbbe{k} 1_R} \ar[dr]_{1_R} & R \otimes_\mathbbe{k} R \ar[d]^\mu & R \ar[l]_-{1_R \otimes_\mathbbe{k} \eta} \ar[dl]^{1_R} \\ R \otimes_\mathbbe{k} R \ar[r]_-\mu & R &&  R}$


SUGGESTION: unital ring

From [Category Theory in Context](https://mathgloss.github.io/MathGloss/context.html)