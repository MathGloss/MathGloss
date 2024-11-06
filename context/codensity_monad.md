---
layout: page
title: codensity monad
permalink: /context/codensity_monad
---
The **codensity monad** of $G \colon \mathsf{D} \to \mathsf{C}$ is given by the right Kan extension of $G$ along itself, whenever this exists.
$$\xymatrix{ \cD \ar[rr]^G \ar[dr]_G & \ar@{}[d]\mid(.4){\Uparrow \epsilon} & \mathsf{C} \\ & \mathsf{C} \ar@{-->}[ur]_{\Ran_GG\eqqcolon T}}$$
The unit and multiplication natural transformations are defined using the universal property of $\epsilon \colon TG \Rightarrow G$ as follows:
$$\xymatrix{ \cD \ar[rr]^G \ar[dr]_G & \ar@{}[d]\mid(.4){\Uparrow 1_G} & \mathsf{C} \ar@{}[dr]\mid*+{=} & \mathsf{D} \ar[rr]^G \ar[dr]_G & \ar@{}[d]_(.4){\Uparrow\epsilon} \ar@{}[dr]\mid(.58){\exists !
warrow\eta}& \mathsf{C} \\ & \mathsf{C} \ar[ur]_{1_\mathsf{C}} &&  & \mathsf{C} \ar@/^/[ur]^{T} \ar@/_1.5pc/[ur]_{1_\mathsf{C}}& } $$
$$\xymatrix{ \cD \ar[rrr]^G \ar@/^/[drr]^(.6)G \ar[dr]_G &  & \ar@{}[d]\mid(.4){\Uparrow \epsilon} & \mathsf{C} \ar@{}[dr]\mid*+{=} & \mathsf{D} \ar[rrr]^G \ar[dr]_G & \ar@{}[d]\mid(.4){\Uparrow\epsilon} &\ar@{}[d]\mid(.6){\exists !
warrow\mu} &  \mathsf{C} \\ & \mathsf{C} \ar@{}[u]\mid(.4){\Uparrow\epsilon} \ar[r]_T & \mathsf{C} \ar[ur]_{T}  &&  & \mathsf{C} \ar@/^/[urr]^{T} \ar[r]_T & \mathsf{C} \ar[ur]_T } $$
