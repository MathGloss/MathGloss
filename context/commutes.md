---
layout: page
title: commutes
permalink: /context/commutes
---
Given categories $\mathsf{C}$ and $\mathsf{D}$ and functors $F,G \colon \mathsf{C} \rightrightarrows \mathsf{D}$, a **natural transformation** $\alpha \colon F \Rightarrow G$ consists of:
1. an arrow $\alpha_c \colon Fc \to Gc$ in $\mathsf{D}$ for each object $c\in \mathsf{C}$, the collection of which define the **components** of the natural transformation,
so that, for any morphism $f \colon c \to c'$ in $\mathsf{C}$, the following square of morphisms in $\mathsf{D}$
$$ \vcenter{\xymatrix{ Fc \ar[d]_{Ff} \ar[r]^{\alpha_c} & Gc \ar[d]^{Gf} \\ Fc' \ar[r]_{\alpha_{c'}} & Gc'}}$$
**commutes**, i.e., has a common composite $Fc \to Gc'$ in $\mathsf{D}$.

A **natural isomorphism** is a natural transformation $\alpha \colon F \Rightarrow G$ in which every component $\alpha_c$ is an isomorphism. In this case, the natural isomorphism may be depicted as $\alpha \colon F \cong G$.
