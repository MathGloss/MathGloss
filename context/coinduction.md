---
layout: page
title: coinduction
permalink: /context/coinduction
---

The objects of the functor category _\mathbbe{k}^{\mathsf{B} G}$, of $G$-representations and equivariant linear maps}$\textup{\textsf{Vect}}_\mathbbe{k}^{\mathsf{B} G}$ are $G$-representations over the field $\mathbbe{k}$, and arrows are $G$-equivariant linear maps. If $H$ is a subgroup of $G$, restriction $\textup{res}_H^G : \textup{\textsf{Vect}}_\mathbbe{k}^{\mathsf{B} G} \to \textup{\textsf{Vect}}_\mathbbe{k}^{\mathsf{B} H}$ of a $G$-representation to an $H$-representation is simply pre-composition by the inclusion functor $\mathsf{B} H \hookrightarrow \mathsf{B} G$. This functor has a left adjoint, called **induction**, and a  right adjoint, called **coinduction**.
  $\vcenter{\xymatrix{\textup{\textsf{Vect}}_\mathbbe{k}^{\mathsf{B} G}  \ar[r]|{\mathrm{res}_H^G} & \textup{\textsf{Vect}}_\mathbbe{k}^{\mathsf{B} H} \ar@/^1.5pc/[l]^{\mathrm{coind}_H^G} \ar@/_1.5pc/[l]_{\mathrm{ind}_H^G} \ar@{}[l]^*+{\labelstyle{\perp}}_*+{\labelstyle\perp} }}$
  By Proposition \ref{prop:kan-adjoint}, the induction functor is given by left Kan extension along the inclusion $\mathsf{B} H \hookrightarrow \mathsf{B} G$, while coinduction is given by right Kan extension. The reader unfamiliar with the construction of induced representations need not remain in suspense for very long; see Theorem \ref{thm:Kan-formula} and Example \ref{ex:repKan2}. Similar remarks apply for $G$-sets, $G$-spaces, based $G$-spaces, or indeed $G$-objects in any category, although if the ambient category has few limits and colimits, these adjoints need not exist.
 

SUGGESTION: coinduction

From [Category Theory in Context](https://mathgloss.github.io/MathGloss/context.html)