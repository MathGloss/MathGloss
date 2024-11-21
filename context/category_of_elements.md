---
layout: page
title: category of elements
permalink: /context/category_of_elements
---
 The  **category of elements** $, the category of elements for a set-valued functor $F$}$}$\textstyle{\int}\!{F}$ of a contravariant functor $F : \mathsf{C}^\mathrm{op} \to \textup{\textsf{Set}}$  has

-  as objects, pairs $(c,x)$ where $c \in \mathsf{C}$ and $x \in Fc$, and
-  a morphism $(c,x) \to (c',x')$ is a morphism $f : c \to c'$ in $\mathsf{C}$ so that $Ff(x') = x$.

The category of elements has an evident forgetful functor $\Pi : \textstyle{\int}\!{F} \to \mathsf{C}$.
$ \xymatrix{ \mathrm{If}\ Ff(x')=x,\ \mathrm{then} &  (c,x) \ar[r]^f \ar@{}[dr]|{\rotatebox{-90}{$\mapsto$}}^(.6){\Pi} & (c',x') &  \in & \textstyle{\int}\!{F} \ar[d]^\Pi \\ & c \ar[r]_f & c' & \in  & \mathsf{C}}$


SUGGESTION: category of elements