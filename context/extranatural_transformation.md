---
layout: page
title: extranatural transformation
permalink: /context/extranatural_transformation.md
---
 Given a pair of functors $F : \mathsf{A} \times \mathsf{B} \times \mathsf{B}^\mathrm{op} \to \mathsf{D}$ and $G : \mathsf{A} \times \mathsf{C} \times \mathsf{C}^\mathrm{op} \to \mathsf{D}$, a family of morphisms $ \alpha_{a,b,c} : F(a,b,b) \to G(a,c,c)$ in $\mathsf{D}$ defines the components of an **extranatural transformation** $\alpha : F \Rightarrow G$ if for any $f : a \to a'$, $g : b \to b'$, and $h : c \to c'$ the following diagrams commute in $\mathsf{D}$:
${\xymatrix{ F(a,b,b) \ar[d]|{F(f,1_b,1_b)} \ar[r]^{\alpha_{a,b,c}} & G(a,c,c) \ar[d]|{G(f,1_c,1_c)} \\ F(a',b,b) \ar[r]_{\alpha_{a',b,c}} & G(a',c,c) }}
{\xymatrix{ F(a,b,b') \ar[d]|{F(1_a, g, 1_{b'})} \ar[r]^{F(1_a, 1_b, g)} & F(a, b,b) \ar[d]^{\alpha_{a,b,c}} \\F(a,b',b') \ar[r]_{\alpha_{a,b',c}} & G(a,c,c) }} {\xymatrix{ F(a,b,b) \ar[r]^{\alpha_{a,b,c'}} \ar[d]_{\alpha_{a,b,c}} & G(a,c',c') \ar[d]|{G(1_a, 1_{c'}, h)} \\ G(a,c,c) \ar[r]_{G(1_a, h, 1_c)} & G(a, c',c)}}$
The left-hand square asserts that the components $\alpha_{-,b,c} : F(-,b,b) \Rightarrow G(-,c,c)$ define a natural transformation in $a$ for each $b \in \mathsf{B}$ and $c \in \mathsf{C}$. The remaining squares assert that the components $\alpha_{a,-,c} : F(a,-,-) \Rightarrow G(a,c,c)$ and $\alpha_{a,b,-} : F(a,b,b) \Rightarrow G(a,-,-)$ define transformations that are respectively extranatural in $b$ and in $c$.  Explain why the functors $F$ and $G$ must have a common target category for this definition to make sense.


SUGGESTION: Natural transformation