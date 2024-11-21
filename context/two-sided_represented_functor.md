---
layout: page
title: two-sided represented functor
permalink: /context/two-sided_represented_functor.md
---
 If $\mathsf{C}$ is locally small, then there is a **two-sided represented functor**
$ \mathsf{C}(-,-) : \mathsf{C}^\mathrm{op} \times \mathsf{C} \to \textup{\textsf{Set}}$ defined in the evident manner. A pair of objects $(x,y)$ is mapped to the hom-set $\mathsf{C}(x,y)$. A pair of morphisms $f : w \to x$ and $h : y \to z$ is sent to the function $  \xymatrix@C=8pt@R=8pt{\mathsf{C}(x,y) \ar[rr]^-{(f^*,h_*)} &&  \mathsf{C}(w,z) \\ g  & \mapsto & hgf}$ that takes an arrow $g : x \to y$ and then pre-composes with $f$ and post-composes with $h$ to obtain $hgf : w \to z$.


SUGGESTION: two-sided represented functor