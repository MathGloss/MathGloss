---
layout: page
title: $U$-split coequalizer
permalink: /context/$u$-split_coequalizer
---
Given a functor $U \colon \mathsf{D} \to \mathsf{C}$:
1. A **$U$-split coequalizer** is a parallel pair $f,g \colon x \rightrightarrows y$ in $\mathsf{D}$ together with an extension of the pair $Uf,Ug \colon Ux \rightrightarrows Uy$ to a split coequalizer diagram
$$ \xymatrix{ Ux \ar@<.5ex>[r]^{Uf} \ar@<-.5ex>[r]_{Ug} & Uy \ar[r]^h \ar@/^3ex/[l]^t & z \ar@/^/[l]^s}$$ in $\mathsf{C}$.
2. $U$ **creates coequalizers of $U$-split pairs** if any $U$-split coequalizer admits a coequalizer in $\mathsf{D}$ whose image under $U$ is isomorphic to the fork underlying the given $U$-split coequalizer diagram in $\mathsf{C}$, and if any such fork in $\mathsf{D}$ is a coequalizer.
3. $U$ **strictly creates coequalizers of $U$-split pairs** if any $U$-split coequalizer admits a unique lift to a coequalizer  in $\mathsf{D}$ for the given parallel pair.
