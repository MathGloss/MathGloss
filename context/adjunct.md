---
layout: page
title: adjunct
permalink: /context/adjunct
---
An **adjunction** consists of a pair of functors $F \colon \mathsf{C} \to \mathsf{D}$ and $G \colon \mathsf{D} \to \mathsf{C}$ together with an isomorphism $$\mathsf{D}(Fc,d) \cong \mathsf{C}(c,Gd)$$ for each $c \in \mathsf{C}$ and $d \in \mathsf{D}$ that is natural in both variables. Here $F$ is **left adjoint** to $G$ and $G$ is **right adjoint** to $F$. The morphisms $$ \xymatrix{ Fc \ar[r]^{f^\sharp} & d} \qquad \leftrightsquigarrow\qquad \xymatrix{ c \ar[r]^{f^\flat} & Gd}$$ corresponding under the bijection \eqref{eq:hom-set-adj} are **adjunct** or are **transposes** of each other.
