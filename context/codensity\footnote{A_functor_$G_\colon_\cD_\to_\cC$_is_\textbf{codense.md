---
layout: page
title: codensity\footnote{A functor $G \colon \cD \to \cC$ is \textbf{codense
permalink: /context/codensity\footnote{A_functor_$G_\colon_\cD_\to_\cC$_is_\textbf{codense.md
---
[\textnormal{monads as Kan extensions}] The **codensity\footnote{A functor $G : \mathsf{D** \to \mathsf{C}$ is **codense** if its right Kan extension along itself is the identity $1_\mathsf{C}$; compare with the statement of Theorem \ref{thm:density-ii}.} monad} of $G : \mathsf{D} \to \mathsf{C}$ is given by the right Kan extension of $G$ along itself, whenever this exists.\footnote{In particular, ``sufficient limits'' in $\mathsf{C}$ means those necessary to define $\mathrm{Ran}_GG$ as a pointwise right Kan extension.}
$\xymatrix{ \mathsf{D} \ar[rr]^G \ar[dr]_G & \ar@{}[d]|(.4){\Uparrow \epsilon} & \mathsf{C} \\ & \mathsf{C} \ar@{-->}[ur]_{\mathrm{Ran}_GG\eqqcolon T}}$
The unit and multiplication natural transformations are defined using the universal property of $\epsilon : TG \Rightarrow G$ as follows:
$\xymatrix{ \mathsf{D} \ar[rr]^G \ar[dr]_G & \ar@{}[d]|(.4){\Uparrow 1_G} & \mathsf{C} \ar@{}[dr]|*+{=} & \mathsf{D} \ar[rr]^G \ar[dr]_G & \ar@{}[d]_(.4){\Uparrow\epsilon} \ar@{}[dr]|(.58){\exists !\Nwarrow\eta}& \mathsf{C} \\ & \mathsf{C} \ar[ur]_{1_\mathsf{C}} &&  & \mathsf{C} \ar@/^/[ur]^{T} \ar@/_1.5pc/[ur]_{1_\mathsf{C}}& } $
$\xymatrix{ \mathsf{D} \ar[rrr]^G \ar@/^/[drr]^(.6)G \ar[dr]_G &  & \ar@{}[d]|(.4){\Uparrow \epsilon} & \mathsf{C} \ar@{}[dr]|*+{=} & \mathsf{D} \ar[rrr]^G \ar[dr]_G & \ar@{}[d]|(.4){\Uparrow\epsilon} &\ar@{}[d]|(.6){\exists !\Nwarrow\mu} &  \mathsf{C} \\ & \mathsf{C} \ar@{}[u]|(.4){\Uparrow\epsilon} \ar[r]_T & \mathsf{C} \ar[ur]_{T}  &&  & \mathsf{C} \ar@/^/[urr]^{T} \ar[r]_T & \mathsf{C} \ar[ur]_T } $


SUGGESTION: codensity monad