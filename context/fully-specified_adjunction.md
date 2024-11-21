---
layout: page
title: fully-specified adjunction
permalink: /context/fully-specified_adjunction.md
---
 Proposition  \ref{prop:unified-adjunction} reveals that the data of a **fully-specified adjunction** can be presented in two equivalent forms: it consists of a pair of functors $F : \mathsf{C} \rightleftarrows \mathsf{D} : G$ together with

-  a natural family of isomorphisms $\mathsf{D}(Fc,d) \mathrm{co}ng \mathsf{C}(c,Gd)$ for all $c \in \mathsf{C}$ and $d \in \mathsf{D}$,

or, equivalently,
[resume]
-  natural transformations $\eta : 1_\mathsf{C} \Rightarrow GF$ and $\epsilon : FG \Rightarrow 1_\mathsf{D}$ so that $G\epsilon \cdot \eta G = 1_G$ and $\epsilon F \cdot F \eta = 1_F$.

Indeed, either of the unit and the counit alone, satisfying an appropriate universal property, suffices to determine a fully specified adjunction: \eqref{itm:original-defn} and \eqref{itm:unit-counit-defn} are each equivalent to either of
[resume]
-  a natural transformation $\eta : 1_\mathsf{C} \Rightarrow GF$ so that the function
$ \xymatrix{ \mathsf{D}(Fc,d) \ar[r]^-G & \mathsf{C}(GFc,Gd) \ar[r]^-{(\eta_c)^*} & \mathsf{C}(c,Gd)}$ defines an isomorphism for all $c \in \mathsf{C}$ and $d \in \mathsf{D}$,

or, equivalently, and dually,
[resume]
-  a natural transformation $\epsilon : FG \Rightarrow 1_\mathsf{D}$ so that the function
$ \xymatrix{ \mathsf{C}(c,Gd) \ar[r]^-F & \mathsf{D}(Fc,FGd) \ar[r]^-{(\epsilon_d)_*} & \mathsf{D}(Fc,d)}$ defines an isomorphism for all $c \in \mathsf{C}$ and $d \in \mathsf{D}$.

In particular, a morphism of adjunctions, introduced in Exercise \ref{exc:adj-mor}, is defined to be a morphism of fully-specified adjunctions. On account of the equivalence between \eqref{itm:original-defn}, \eqref{itm:unit-counit-defn}, \eqref{itm:unit-formula}, and \eqref{itm:counit-formula}, this notion can be presented in several equivalent ways.


SUGGESTION: fully-specified adjunction