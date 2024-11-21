---
layout: page
title: Grothendieck topos
permalink: /context/Grothendieck_topos
---
Given a small category $\mathsf{C}$, a **presheaf** is another name for a contravariant set-valued functor on $\mathsf{C}$.  A **Grothendieck topos** is a reflective full subcategory $\mathsf{E}$ of a presheaf category
$ \xymatrix{ \mathsf{E} \ar@<-1ex>@{^(->}[r] \ar@{}[r]|-\perp & \textup{\textsf{Set}}^{\mathsf{C}^\mathrm{op}} \ar@<-1ex>[l]_-L}$ with the property that the left adjoint preserves finite limits.\footnote{Propositions \ref{prop:reflective-colimit} and \ref{prop:pointwise-limits} imply that $\mathsf{E}$ is cocomplete, so this adjunction can be defined as in Remark \ref{rmk:lan-adjunction} from the functor $L y : \mathsf{C} \to \mathsf{E}$ that is the restriction of the left adjoint along the Yoneda embedding.}
 Objects in $\mathsf{E}$ can be characterized as sheaves on a small \emph{site}, which specifies a ``covering family'' of morphisms $(f_i : U_i \to U)_i$ for each object $U \in \mathsf{C}$ satisfying a weak pullback condition. A typical example might take $\mathsf{C} =\mathcal{O}(X)$ to be the poset of open sets for a topological space $X$. A presheaf $P : \mathcal{O}(X)^\mathrm{op} \to \textup{\textsf{Set}}$ assigns a set $P(U)$ to each open set $U \subset X$ so that this assignment is functorial with respect to restrictions along inclusion $V \subset U \subset X$ of open subsets. A presheaf $P$ is a **sheaf** if and only if the diagram of restriction maps
$ \xymatrix{ P(U) \ar[r] & \prod\limits_\alpha P(U_\alpha) \ar@<.5ex>[r] \ar@<-.5ex>[r] & \prod\limits_{\alpha,\beta} P(U_\alpha \cap U_\beta)}$ is an equalizer for every open cover $U = \cup_\alpha U_\alpha$ of a $U \in \mathcal{O}(X)$; see Definition \ref{defn:sheaf-axiom}.

SUGGESTION: Grothendieck topos