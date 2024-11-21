---
layout: page
title: point-set left derived functor
permalink: /context/point-set_left_derived_functor
---
[\normalfont{point-set derived functors}] Consider a pair of homotopical categories and localization functors $\gamma : \mathsf{C} \to \textup{\textsf{Ho}}\mathsf{C}$ and $\delta : \mathsf{D} \to \textup{\textsf{Ho}}\mathsf{D}$.

-  A **point-set left derived functor** of $F : \mathsf{C} \to \mathsf{D}$ is a homotopical functor $\mathbb{L} F : \mathsf{C} \to \mathsf{D}$  equipped with a natural transformation $\lambda : \mathbb{L} F \Rightarrow F$ so that $\delta \mathbb{L} F$ (which by Remark \ref{rmk:2-cat-loc} is equivalently encoded by a functor $\delta \mathbb{L} F : \textup{\textsf{Ho}} \mathsf{C} \to \textup{\textsf{Ho}}\mathsf{D}$) and $\delta \lambda : \delta  \mathbb{L} F \Rightarrow \delta F$ define a total left derived functor of $F$.
$ \vcenter{\xymatrix@R=5pt{ \mathsf{C} \ar@/^1pc/[rr]^F \ar@/_1pc/[rr]_{\mathbb{L} F} &  \labelstyle{\Uparrow\lambda}  & \mathsf{D} \ar[r]^-\delta & \textup{\textsf{Ho}}\mathsf{D}}} \qquad \leftrightsquigarrow \qquad \vcenter{\xymatrix{ \mathsf{C} \ar@{}[dr]|{\Uparrow\delta \lambda} \ar[r]^F \ar[d]_\gamma & \mathsf{D} \ar[d]^\delta \\ \textup{\textsf{Ho}}\mathsf{C} \ar[r]_{\delta \mathbb{L} F} & \textup{\textsf{Ho}}\mathsf{D}}}$
-  A **point-set right derived functor** of $F : \mathsf{C} \to \mathsf{D}$ is a homotopical functor $\mathbb{R} F : \mathsf{C} \to \mathsf{D}$  equipped with a natural transformation $\rho : F \Rightarrow \mathbb{R} F$ so that $\delta \mathbb{R} F$ (which by Remark \ref{rmk:2-cat-loc} is equivalently encoded by a functor $\delta \mathbb{R} F : \textup{\textsf{Ho}}\mathsf{C} \to \textup{\textsf{Ho}}\mathsf{D}$) and $\delta \rho : \delta  F \Rightarrow  \delta \mathbb{R} F$ define a total right derived functor of $F$.
$ \vcenter{\xymatrix@R=5pt{ \mathsf{C} \ar@/_1pc/[rr]_{\mathbb{R} F} \ar@/^1pc/[rr]^F&  \labelstyle{\Downarrow\rho} & \mathsf{D} \ar[r]^-\delta & \textup{\textsf{Ho}}\mathsf{D}  }} \qquad \leftrightsquigarrow \qquad \vcenter{\xymatrix{ \mathsf{C} \ar@{}[dr]|{\Downarrow\delta\rho} \ar[r]^F \ar[d]_\gamma & \mathsf{D} \ar[d]^\delta \\ \textup{\textsf{Ho}}\mathsf{C} \ar[r]_{\delta \mathbb{R} F} & \textup{\textsf{Ho}}\mathsf{D}}}$



SUGGESTION: point-set left derived functor

From [Category Theory in Context](https://mathgloss.github.io/MathGloss/context.html)