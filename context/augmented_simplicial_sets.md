---
layout: page
title: augmented simplicial sets
permalink: /context/augmented_simplicial_sets
---
The category ${\mathbbe{\Delta}}$ of finite non-empty ordinals and order-preserving maps is a full subcategory containing all but the initial object of the category $\DDelta_+$, of finite ordinals and order-preserving maps. Presheaves on ${\mathbbe{\Delta}}$ are **simplicial sets**, while presheaves on $\DDelta_+$ are called **augmented simplicial sets**. Left Kan extension defines a left adjoint to restriction $$ \xymatrix{ \cat{Set}^{\DDelta_+^\mathrm{op}} \ar[r]\mid{\mathrm{res}}  \ar@{}[r]^*+{\labelstyle{\perp}}_*+{\labelstyle{\perp}} &  \textup{\textsf{cat}}^{{\mathbbe{\Delta}}^\mathrm{op}} \ar@/_1.5pc/[l]_{\pi_0} \ar@/^1.5pc/[l]^{\mathrm{triv}}}$$ that augments a simplicial set $X$ with its set $\pi_0 X$ of path components. Right Kan extension assigns a simplicial set the trivial augmentation built from the one-point set, as can easily be verified by readers familiar with the combinatorics of simplicial sets.
