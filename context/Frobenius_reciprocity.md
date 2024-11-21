---
layout: page
title: Frobenius reciprocity
permalink: /context/Frobenius_reciprocity.md
---
[\textnormal{Frobenius reciprocity}]
Example \ref{exs:free-forgetful}\eqref{itm:baby-induction} can be generalized: Example \ref{ex:repKan2} proves that for any complete and cocomplete category $\mathsf{C}$ and any group homomorphism $\phi : H \to G$, the restriction functor $\phi^* : \mathsf{C}^{\mathsf{B} G} \to \mathsf{C}^{\mathsf{B} H}$ admits both left and right adjoints. These are most commonly considered for subgroup inclusions $H\subset G$, in which case the left adjoint is called **induction** and the right adjoint is called **coinduction**:
$\vcenter{\xymatrix{\mathsf{C}^{\mathsf{B} G}  \ar[r]|{\mathrm{res}_H^G} & \mathsf{C}^{\mathsf{B} H} \ar@/^1.5pc/[l]^{\mathrm{coin}_H^G} \ar@/_1.5pc/[l]_{\mathrm{ind}_H^G} \ar@{}[l]^*+{\labelstyle{\perp}}_*+{\labelstyle\perp} }}$
Taking $\mathsf{C} = \textup{\textsf{Vect}}_\mathbbe{k}$, the adjunction $\textup{ind}_H^G \dashv \textup{res}_H^G$ between the category $\textup{\textsf{Vect}}_\mathbbe{k}^{\mathsf{B} H}$ of $H$-representations and the category of $\textup{\textsf{Vect}}_\mathbbe{k}^{\mathsf{B} G}$ of $G$-representations is referred to in the representation theory literature as **Frobenius reciprocity**.


SUGGESTION: Frobenius reciprocity