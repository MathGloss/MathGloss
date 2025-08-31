---
layout: page
title: path components functor
permalink: /context/path_components_functor
---
 Recall the functor $\textup{Path} : \textup{\textsf{Top}} \to \textup{\textsf{Set}}$ that carries a space $X$ to the set $\textup{Path}(X) :eqq \textup{\textsf{Top}}(I,X)$, where $I$ is the standard unit interval. Precomposing with the endpoint inclusions $0,1 : * \rightrightarrows I$ defines a functor $P : \textup{\textsf{Top}} \to \textup{\textsf{Set}}^{\bullet \rightrightarrows \bullet}$ that carries a space $X$ to the parallel pair of functions
$ \xymatrix{ \textup{Path}(X) \mathrm{co}ng \textup{\textsf{Top}}(I,X) \ar@<.5ex>[r]^-{\mathrm{ev}_0} \ar@<-.5ex>[r]_-{\mathrm{ev}_1} & \textup{\textsf{Top}}(*,X) \mathrm{co}ng \textup{Point}(X)}$
that evaluate a path at its endpoints. Their coequalizer
$ \xymatrix{ \textup{Path}(X) \ar@<.5ex>[r]^-{\mathrm{ev}_0} \ar@<-.5ex>[r]_-{\mathrm{ev}_1} & \textup{Point}(X) \ar@{->>}[r] & \pi_0 X}$ defines the set of **path components** of $X$, the quotient of the set of points in $X$ by the relation that identifies any pair of points connected by a path. Proposition \ref{prop:limit-functor} tells us that this coequalizer defines a functor, the **path components functor** $
\pi_0 :eqq \xymatrix{ \textup{\textsf{Top}} \ar[r]^-P &  \textup{\textsf{Set}}^{\bullet \rightrightarrows \bullet} \ar[r]^-{\textup{colim}} & \textup{\textsf{Set}}.}$


SUGGESTION: path components functor

From [Category Theory in Context](https://mathgloss.github.io/MathGloss/context.html)