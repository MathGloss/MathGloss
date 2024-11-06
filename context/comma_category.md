---
layout: page
title: comma category
permalink: /context/comma_category
---
Given functors $F \colon \mathsf{D} \to \mathsf{C}$ and $G \colon \mathsf{E} \to \mathsf{C}$, show that there is a category, called the **comma category** $F \!\downarrow\! G$, which has
1. as objects, triples $(d \in \mathsf{D}, e \in \mathsf{E}, f \colon Fd \to Ge \in \mathsf{C})$, and
2. as morphisms $(d,e,f) \to (d',e',f')$, a pair of morphisms $(h \colon d \to d', k \colon e \to e')$ so that the square
$$  \xymatrix{ Fd \ar[d]_{Fh} \ar[r]^f & Ge \ar[d]^{Gk} \\ Fd' \ar[r]_{f'} & Ge'}$$ commutes in $\mathsf{C}$, i.e., so that $f' \cdot Fh = Gk \cdot f$.
Define a pair of projection functors $\mathrm{dom} \colon F \!\downarrow\! G \to \mathsf{D}$ and $\mathrm{cod} \colon F \!\downarrow\! G \to \mathsf{E}$.
