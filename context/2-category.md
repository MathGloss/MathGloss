---
layout: page
title: 2-category
permalink: /context/2-category
---
A **2-category** is comprised of:
1. objects, for example the categories $\mathsf{C}$,
2. 1-morphisms between pairs of objects, for example, the functors $\mathsf{C} \xrightarrow{F} \mathsf{D}$, and
3. 2-morphisms between parallel pairs of 1-morphisms, for example, the natural transformations $\xymatrix{ \cC \ar@/^2ex/[r]^*{F} \ar@/_2ex/[r]_*{G} \ar@{}[r]\mid*{\Downarrow \alpha} & \mathsf{D} }$
so that:
1. The objects and 1-morphisms form a category, with identities $1_{\mathsf{C}} \colon \mathsf{C} \to \mathsf{C}$.
2. For each fixed pair of objects $\mathsf{C}$ and $\mathsf{D}$, the 1-morphisms $F \colon \mathsf{C} \to \mathsf{D}$ and 2-morphisms between such form a category under an operation called vertical composition, as described in Lemma \ref{lem:vert-comp}, with identities $\xymatrix{ \cC \ar@/^2ex/[r]^*{F} \ar@/_2ex/[r]_*{F} \ar@{}[r]\mid*{\Downarrow 1_F} & \mathsf{D} }$.
3. There is also a  category whose objects are the objects in which a morphism from $\mathsf{C}$ to $\mathsf{D}$ is a 2-cell $\xymatrix{ \cC \ar@/^2ex/[r]^*{F} \ar@/_2ex/[r]_*{G} \ar@{}[r]\mid*{\Downarrow \alpha} & \mathsf{D} }$ under an operation called horizontal composition, with identities $\xymatrix{ \cC \ar@/^2ex/[r]^*{1_\cC} \ar@/_2ex/[r]_*{1_\mathsf{C}} \ar@{}[r]\mid*{\Downarrow 1_{1_\mathsf{C}}} & \mathsf{C} }$. The source and target 1-morphisms of a horizontal composition must have the form described in Lemma \ref{lem:horiz-comp}.
4. The horizontal composite $1_H \ast 1_F$ of identities for vertical composition must be the identity $1_{HF}$ for for the composite 1-morphisms.
5. The law of middle four interchange described in Lemma \ref{lem:cat-is-2-cat} holds.
