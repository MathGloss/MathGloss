---
layout: page
title: right adjoint
permalink: /context/right_adjoint
---
[\textnormal{adjunctions I}] An **adjunction** consists of a pair of functors $F : \mathsf{C} \to \mathsf{D}$ and $G : \mathsf{D} \to \mathsf{C}$ together with an isomorphism \mathsf{D}(Fc,d) \mathrm{co}ng \mathsf{C}(c,Gd) for each $c \in \mathsf{C}$ and $d \in \mathsf{D}$ that is natural in both variables. Here $F$ is **left adjoint** to $G$ and $G$ is **right adjoint** to $F$. The morphisms $ \xymatrix{ Fc \ar[r]^{f^\sharp} & d} \qquad \leftrightsquigarrow\qquad \xymatrix{ c \ar[r]^{f^\flat} & Gd}$ corresponding under the bijection \eqref{eq:hom-set-adj} are **adjunct** or are **transposes** of each other.\footnote{For now, we use ``$(-)^\sharp$'' and ``$(-)^\flat$'' to decorate a pair of adjunct arrows, but in practice it tends to be most convenient to use some symbol, such as  ``$(-)^\dagger$'' or ``$\hat{(-)}$''  to signal any adjoint transpose, with no preference as to which of the adjunct pair is decorated in this way.}


SUGGESTION: right adjoint functor

From [Category Theory in Context](https://mathgloss.github.io/MathGloss/context.html)