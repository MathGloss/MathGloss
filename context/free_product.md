---
layout: page
title: free product
permalink: /context/free_product.md
---
In fact, $\textup{\textsf{Ab}}$ and any category of models for an algebraic theory is cocomplete. However, the construction of those colimits that are not preserved by the monad is more complicated. To explore this problem, consider the monadic forgetful functor $U : \textup{\textsf{Group}} \to \textup{\textsf{Set}}$. Both $\textup{\textsf{Set}}$ and $\textup{\textsf{Group}}$ admit coproducts; in $\textup{\textsf{Set}}$ these are simply disjoint unions, while in $\textup{\textsf{Group}}$ they are given by the free product. The **free product** of groups $G$ and $H$ is the group $G \ast H$ of words whose letters are drawn from the elements of $G$ and $H$ together with formal inverses, modulo relations defined using the group operations in each group. Note, in particular, that $U : \textup{\textsf{Group}} \to \textup{\textsf{Set}}$ does not preserve (and so, in particular, does not create) coproducts. However, there is a more precise description of the free product $G \ast H$ that can be stated entirely in terms of the free $\dashv$ forgetful adjunction
$ \xymatrix{ \textup{\textsf{Set}} \ar@<1ex>[r]^-F \ar@{}[r]|-\perp & \textup{\textsf{Group}}\rlap{,},} \ar@<1ex>[l]^-U}$ which generalizes to define coproducts relative to any monadic adjunction.

SUGGESTION: free product of groups