-  There is a transitivity map $\tau$ whose domain is the pullback of $t$ along $s$
$ \xymatrix{ R \times_X R \ar[d]_{\tilde{s}} \ar[r]^-{\tilde{t}} \ar@{}[dr]|(.2){\displaystyle\lrcorner} & R \ar[r]^t \ar[d]_s & X \\ R \ar[r]^t \ar[d]_s & X \\ X}$  This diagram defines a cone over the pullback defining $R$ and thus induces a map
$ \xymatrix{ R\times_X R\ar@{-->}[dr]^{\tau} \ar@/^/[drr]^{t\tilde{t}} \ar@/_/[ddr]_{s\tilde{s}}  \\ & R \ar[d]_s \ar[r]^t \ar@{}[dr]|(.2){\displaystyle\lrcorner} & X \ar[d]^f \\ & X \ar[r]_f & Y}$ so that $s\tau = s \tilde{s}$ and $t \tau = t\tilde{t}$.

An  **equivalence relation** in a category $\mathsf{C}$ with finite limits is a subobject $(s,t) : R \rightarrowtail X \times X$ equipped with maps $\rho$, $\sigma$, and $\tau$ commuting with the morphisms $s$ and $t$ in the manner displayed in the diagrams of \eqref{itm:ker-pair-i}, \eqref{itm:ker-pair-ii}, and \eqref{itm:ker-pair-iii}. When it exists, the coequalizer of the maps $s,t : R \rightrightarrows X$ of an equivalence relation defines a quotient object $e : X \twoheadrightarrow X_{/R}$. In $\textup{\textsf{Set}}$, $X_{/R}$ is the set of $R$-equivalence classes of elements of $X$. For equivalence relations arising as kernel pairs, there is a unique factorization
$\xymatrix{ X \ar[rr]^f \ar@{->>}[dr]_e & & Y \\ & X_{/R} \ar@{-->}[ur]_m}$ In good situations, such as when $\mathsf{C}$ is a  \emph{Grothendieck topos} (see \S\ref{sec:topos}), the map $m$ is a monomorphism and this factorization defines the **image factorization** of the map $f$: the monomorphism $X_{/R} \rightarrowtail Y$ identifies the **image** $X_{/R}$ as a subobject of $Y$.




\subsection*{Exercises}%ex

 Let $G$ be a group regarded as 1-object category $\mathsf{B} G$. Describe the colimit of  a diagram $\mathsf{B} G \to \textup{\textsf{Set}}$ in group-theoretic terms, as was done for the limit in Example \ref{ex:fixed-point-limit}.


 Prove that the colimit of any small functor $F : \mathsf{C} \to \textup{\textsf{Set}}$ is isomorphic to the set $\pi_0 (\textstyle{\int}\!{F})$ of connected components of the category of elements of $F$. What is the colimit cone?



 Prove that the category $\textup{\textsf{DirGraph}}$ of directed graphs is complete and cocomplete and explain how to construct its limits and colimits. (Hint: Use Proposition \ref{prop:pointwise-limits}.)


 For a small category $\mathsf{J}$, define a functor $i_0 : \mathsf{J} \to \mathsf{J} \times \mathbbe{2}$ so that the pushout
$ \xymatrix{ \mathsf{J} \ar[d]_{i_0} \ar[r]^-{!} \ar@{}[dr]|(.8){\displaystyle\ulcorner} & \mathbbe{1} \ar[d]^s \\ \mathsf{J} \times \mathbbe{2} \ar[r] & \mathsf{J}^{\triangleleft}}$ in $\textup{\textsf{Cat}}$ defines the **cone** over $\mathsf{J}$, with the functor $s : \mathbbe{1} \to \mathsf{J}^\triangleleft$ picking out the summit object. Remark \ref{rmk:limit-diagram-shape} gives an informal description of this category, which is used to index the diagram formed by a cone over a diagram of shape $\mathsf{J}$.



Describe the limits and colimits in the poset of natural numbers with the order relation $k \leq n$ if and only if $k$ divides $n$.


 Define a contravariant functor _{\mathrm{mono}}$, of finite sets and injections}$\textup{\textsf{Fin}}_{\mathrm{mono}}^\mathrm{op} \to \textup{\textsf{Top}}$ from the category of finite sets and injections to the category of topological spaces that sends a set with $n$ elements to the space $\textup{PConf}_n(X)$ constructed in Example \ref{ex:conf-space}. Explain why this functor does not induce a similar functor sending an $n$-element set to the space $\textup{Conf}_n(X)$.



 Following \cite{grothendieck-kansas}, define a **fiber space** $p : E \to B$ to be a morphism in $\textup{\textsf{Top}}$.  A map of fiber spaces is a commutative square. Thus, the category of fiber spaces is isomorphic to the diagram category $\textup{\textsf{Top}}^\mathbbe{2}$. We are also interested in the non-full subcategory $\textup{\textsf{Top}}/B \subset \textup{\textsf{Top}}^\mathbbe{2}$ of fiber spaces over $B$ and maps whose codomain component is the identity. Prove the following:


SUGGESTION: equivalence relation