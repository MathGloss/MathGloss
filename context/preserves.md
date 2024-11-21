---
layout: page
title: preserves
permalink: /context/preserves
---

A functor $L : \mathsf{E} \to \mathsf{F}$ **preserves** a left Kan extension $(\mathrm{Lan}_KF,\eta)$ if the whiskered composite $(L \mathrm{Lan}_K F, L\eta)$ is the left Kan extension of $LF$ along $K$.
$\xymatrix{ \mathsf{C} \ar[rr]^F \ar[dr]_K & \ar@{}[d]|(.4){\Downarrow \eta} & \mathsf{E} \ar[r]^L & \mathsf{F} \ar@{}[dr]|*+{\mathrm{co}ng} & \mathsf{C} \ar[rr]^{LF} \ar[dr]_K & \ar@{}[d]|(.4){\Downarrow} & \mathsf{F} \\ & \mathsf{D} \ar[ur]_{\mathrm{Lan}_KF} & & & & \mathsf{D} \ar@{-->}[ur]_{\mathrm{Lan}_KLF} }$


SUGGESTION: functor that preserves a left Kan extension

From [Category Theory in Context](https://mathgloss.github.io/MathGloss/context.html)