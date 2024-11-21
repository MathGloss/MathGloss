---
layout: page
title: morphism of adjunctions
permalink: /context/morphism_of_adjunctions.md
---
 A **morphism of adjunctions** from $F \dashv G$ to $F' \dashv G'$ is comprised of a pair of functors
$ \xymatrix{ \mathsf{C} \ar[r]^H \ar@<-1ex>[d]_F \ar@{}[d]|\dashv & \mathsf{C}' \ar@<-1ex>[d]_{F'} \ar@{}[d]|\dashv \\ \mathsf{D} \ar@<-1ex>[u]_G \ar[r]_K & \mathsf{D}' \ar@<-1ex>[u]_{G'}}$ so that the square with the left adjoints and the square with the right adjoints both commute (i.e., $KF=F'H$ and $HG = G'K$) and satisfying one additional condition, which takes a number of equivalent forms. Prove that the following are equivalent:

-   $H\eta = \eta' H$, where $\eta$ and $\eta'$ denote the respective units of the adjunctions.
-  $K\epsilon = \epsilon' K$, where $\epsilon$ and $\epsilon'$ denote the respective counits of the adjunctions.
-  Transposition across the adjunctions commutes with application of the functors $H$ and $K$, i.e., for every $c \in \mathsf{C}$ and $d \in \mathsf{D}$, the diagram
$ \xymatrix@=10pt{ \mathsf{D}(Fc,d) \ar[r]^\mathrm{co}ng \ar[d]_K & \mathsf{C}(c,Gd) \ar[d]^H \\ \mathsf{D}'(KFc,Kd) \ar@{=}[d] & \mathsf{C}'(Hc, HGd) \ar@{=}[d] \\ \mathsf{D}'(F'Hc,Kd) \ar[r]_\mathrm{co}ng & \mathsf{C}'(Hc, G'Kd)}$ commutes.



SUGGESTION: morphism of adjunctions