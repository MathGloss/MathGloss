---
layout: page
title: codensity monad
permalink: /context/codensity_monad
---
[\textnormal{monads as Kan extensions}] The **codensity monad of $G : \mathsf{D} \to \mathsf{C}$** is given by the right Kan extension of $G$ along itself, whenever this exists.\footnote{In particular, ``sufficient limits'' in $\mathsf{C}$ means those necessary to define $\mathrm{Ran}_GG$ as a pointwise right Kan extension.}
$\xymatrix{ \mathsf{D} \ar[rr]^G \ar[dr]_G & \ar@{}[d]|(.4){\Uparrow \epsilon} & \mathsf{C} \\ & \mathsf{C} \ar@{-->}[ur]_{\mathrm{Ran}_GG\eqqcolon T}}$
The unit and multiplication natural transformations are defined using the universal property of $\epsilon : TG \Rightarrow G$ as follows:
$\xymatrix{ \mathsf{D} \ar[rr]^G \ar[dr]_G & \ar@{}[d]|(.4){\Uparrow 1_G} & \mathsf{C} \ar@{}[dr]|*+{=} & \mathsf{D} \ar[rr]^G \ar[dr]_G & \ar@{}[d]_(.4){\Uparrow\epsilon} \ar@{}[dr]|(.58){\exists !\Nwarrow\eta}& \mathsf{C} \\ & \mathsf{C} \ar[ur]_{1_\mathsf{C}} &&  & \mathsf{C} \ar@/^/[ur]^{T} \ar@/_1.5pc/[ur]_{1_\mathsf{C}}& } $
$\xymatrix{ \mathsf{D} \ar[rrr]^G \ar@/^/[drr]^(.6)G \ar[dr]_G &  & \ar@{}[d]|(.4){\Uparrow \epsilon} & \mathsf{C} \ar@{}[dr]|*+{=} & \mathsf{D} \ar[rrr]^G \ar[dr]_G & \ar@{}[d]|(.4){\Uparrow\epsilon} &\ar@{}[d]|(.6){\exists !\Nwarrow\mu} &  \mathsf{C} \\ & \mathsf{C} \ar@{}[u]|(.4){\Uparrow\epsilon} \ar[r]_T & \mathsf{C} \ar[ur]_{T}  &&  & \mathsf{C} \ar@/^/[urr]^{T} \ar[r]_T & \mathsf{C} \ar[ur]_T } $



SUGGESTION: codensity monad

From [Category Theory in Context](https://mathgloss.github.io/MathGloss/context.html)