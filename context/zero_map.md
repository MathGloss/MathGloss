---
layout: page
title: zero map
permalink: /context/zero_map.md
---
 In any category with finite limits,  the **kernel pair**\footnote{In the absence of a **zero object**---an object that is both initial and terminal, which can be used to define a **zero map** between any pair of objects---kernel pairs are the best analog of kernels. Barry Fawcett acknowledges the pervasiveness of this sort of construction, writing  ``Category theory tells us: to learn about $A$, study pairs of maps out of [or into] $A$'' \cite{Fawcett:1986ac}.} of a morphism $f : X \to Y$ is the pullback of $f$ along itself:
$ \xymatrix{ R \ar[d]_s \ar[r]^t \ar@{}[dr]|(.2){\displaystyle\lrcorner} & X \ar[d]^f \\ X \ar[r]_f & Y}$ These maps define a monomorphism $(s,t) : R \rightarrowtail X \times X$, so the object $R$ is always a subobject of the product $X \times X$.\footnote{A **subobject** of an object $c$ is a monomorphism with codomain $c$; see Definition \ref{defn:subobject}.} In $\textup{\textsf{Set}}$, a subset $R \subset X \times X$ defines a **relation** on $X$. Indeed, subobjects defined by kernel pairs are always **equivalence relations**,  in the following categorical sense:

-  There is a reflexivity map $\rho$ defined by $ \xymatrix{ X \ar@{-->}[dr]^{\rho} \ar@/^/[drr]^{1_X} \ar@/_/[ddr]_{1_X}  \\ & R \ar[d]_s \ar[r]^t \ar@{}[dr]|(.2){\displaystyle\lrcorner} & X \ar[d]^f \\ & X \ar[r]_f & Y}$
that is a section of both $s$ and $t$, i.e., that defines a factorization of the diagonal $ \xymatrix@R=10pt{ X \ar[rr]^{(1_X,1_X)} \ar[dr]_{\rho} & & X \times X \\ & R \ar@{ >->}[ur]_{(s,t)}}$
-  There is a symmetry map $\sigma$ defined by $ \xymatrix{ R \ar@{-->}[dr]^{\sigma} \ar@/^/[drr]^{s} \ar@/_/[ddr]_{t}  \\ & R \ar[d]_s \ar[r]^t \ar@{}[dr]|(.2){\displaystyle\lrcorner} & X \ar[d]^f \\ & X \ar[r]_f & Y}$ so that $t \sigma =s$ and $s \sigma = t$.
-  There is a transitivity map $\tau$ whose domain is the pullback of $t$ along $s$
$ \xymatrix{ R \times_X R \ar[d]_{\tilde{s}} \ar[r]^-{\tilde{t}} \ar@{}[dr]|(.2){\displaystyle\lrcorner} & R \ar[r]^t \ar[d]_s & X \\ R \ar[r]^t \ar[d]_s & X \\ X}$  This diagram defines a cone over the pullback defining $R$ and thus induces a map
$ \xymatrix{ R\times_X R\ar@{-->}[dr]^{\tau} \ar@/^/[drr]^{t\tilde{t}} \ar@/_/[ddr]_{s\tilde{s}}  \\ & R \ar[d]_s \ar[r]^t \ar@{}[dr]|(.2){\displaystyle\lrcorner} & X \ar[d]^f \\ & X \ar[r]_f & Y}$ so that $s\tau = s \tilde{s}$ and $t \tau = t\tilde{t}$.

An  **equivalence relation** in a category $\mathsf{C}$ with finite limits is a subobject $(s,t) : R \rightarrowtail X \times X$ equipped with maps $\rho$, $\sigma$, and $\tau$ commuting with the morphisms $s$ and $t$ in the manner displayed in the diagrams of \eqref{itm:ker-pair-i}, \eqref{itm:ker-pair-ii}, and \eqref{itm:ker-pair-iii}. When it exists, the coequalizer of the maps $s,t : R \rightrightarrows X$ of an equivalence relation defines a quotient object $e : X \twoheadrightarrow X_{/R}$. In $\textup{\textsf{Set}}$, $X_{/R}$ is the set of $R$-equivalence classes of elements of $X$. For equivalence relations arising as kernel pairs, there is a unique factorization
$\xymatrix{ X \ar[rr]^f \ar@{->>}[dr]_e & & Y \\ & X_{/R} \ar@{-->}[ur]_m}$ In good situations, such as when $\mathsf{C}$ is a  \emph{Grothendieck topos} (see \S\ref{sec:topos}), the map $m$ is a monomorphism and this factorization defines the **image factorization** of the map $f$: the monomorphism $X_{/R} \rightarrowtail Y$ identifies the **image** $X_{/R}$ as a subobject of $Y$.


SUGGESTION: kernel pair