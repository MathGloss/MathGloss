---
layout: page
title: Étale space
permalink: /context/etale_space
---
 For a fixed topological space $X$, there is a natural inclusion $\mathcal{O}(X) \to \textup{\textsf{Top}}/X$ that sends an open subset $U \subset X$ to the continuous function $U \hookrightarrow X$. Apply the construction of Remark \ref{rmk:lan-adjunction} to this functor to define an adjunction
$ \xymatrix{ \textup{\textsf{Top}}/X \ar@<-1ex>[r] \ar@{}[r]|-\perp & \textup{\textsf{Set}}^{\mathcal{O}(X)^\mathrm{op}} \ar@<-1ex>[l]}$
between the category of presheaves on $\mathcal{O}(X)$ and the category of spaces over $X$. By Exercise \ref{exc:equiv-in-adjoint}, this adjunction, like all adjunctions, restricts to define an adjoint equivalence of categories, in this case between the category of **sheaves** on $X$ and the category of **Étale spaces** over $X$.


SUGGESTION: Étale space

From [Category Theory in Context](https://mathgloss.github.io/MathGloss/context.html)