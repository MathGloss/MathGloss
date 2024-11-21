---
layout: page
title: local
permalink: /context/local.md
---
-  Show that the essential image of $\mathsf{D}$ consists of those objects $c$ that are **local** for the class of morphisms that are inverted by $L$. That is, $c$ is in the essential image if and only if the pre-composition functions
$ \mathsf{C}(b,c) \xrightarrow{f^*} \mathsf{C}(a,c)$ are isomorphisms for all maps $f : a \to b$ in $\mathsf{C}$ for which $Lf$ is an isomorphism in $\mathsf{D}$. This explains why the reflector is also referred to as ``localization.''



 Find an example which demonstrates that the inclusion of a reflective subcategory does not create all colimits.



\section{Existence of adjoint functors}

Does the inclusion $\textup{\textsf{Ring}}\hookrightarrow\textup{\textsf{Rng}}$ of the category of unital rings into the category of possibly non-unital rings have any adjoints? A first strategy to probe a question of this form might be called the ``initial and terminal objects test'': by Theorems \ref{thm:RAPL} and \ref{thm:LAPC}, a functor admitting a left adjoint must necessarily preserve all limits while a functor admitting a right adjoint must necessarily preserve all colimits. The ring $\mathbb{Z}$ is initial in $\textup{\textsf{Ring}}$ but not in $\textup{\textsf{Rng}}$, so  there can be no right adjoint. The zero ring is terminal in both categories, so a left adjoint to the inclusion might be possible. Indeed, $\textup{\textsf{Ring}}$ has all limits and the inclusion preserves them.\footnote{As an application of Theorem \ref{thm:monadic-limits}, the forgetful functors from $\textup{\textsf{Ring}}$ or from $\textup{\textsf{Rng}}$ to $\textup{\textsf{Set}}$ both create all limits. On account of the commuting triangle $ \xymatrix@=10pt{ \textup{\textsf{Ring}}\ \ar[dr]_U \ar@{^(->}[rr] & & \textup{\textsf{Rng}} \ar[dl]^U \\ & \textup{\textsf{Set}}}$ it follows that the inclusion preserves all limits.}

The search for a left adjoint to $\textup{\textsf{Ring}}\hookrightarrow\textup{\textsf{Rng}}$ might be thought of as some sort of formulaic (that is to say \emph{functorial}) optimization problem, whose aim is to adjoin a multiplicative unit to a possibly non-unital ring $R$ in the ``most efficient way possible.'' The Yoneda lemma can be used to make this intuition precise. To define the value of a hypothetical left adjoint on a possibly non-unital ring $R$, we seek a unital ring $R^*$ together with a natural isomorphism
$ \textup{\textsf{Ring}}(R^*,S) \mathrm{co}ng \textup{\textsf{Rng}}(R,S)$ for all unital rings $S$. Note that even if $R$ has a unit, the ring $R^*$ will still differ from $R$ because homomorphisms in $\textup{\textsf{Ring}}$ must preserve units, while homomorphisms in $\textup{\textsf{Rng}}$ need not.

To define this natural isomorphism is to define a representation $R^*$ for the functor $\textup{\textsf{Rng}}(R,-) : \textup{\textsf{Ring}} \to \textup{\textsf{Set}}$. By Proposition \ref{prop:rep-crit}, a representation defines an initial object in the category of elements $\textstyle{\int}\!{\textup{\textsf{Rng}}(R,-)}$. Objects in this category are homomorphisms $R \to S$ whose codomain is a unital ring;  morphisms are commutative triangles
$ \xymatrix@=10pt{ & R \ar[dl] \ar[dr] \\ S \ar[rr] & & S'}$
whose leg opposite $R$ is a unital ring homomorphism but whose legs with domain $R$ do not necessarily preserve the multiplicative unit, if $R$ happens to have one. This category of elements is isomorphic to the comma category $R \mathrm{co}mma \textup{\textsf{Ring}}$ of non-unital homomorphisms from $R$ to a unital ring.  The optimization problem is solved if we can find a unital ring $R^*$ and ring homomorphism $R \to R^*$ that is initial in this category.\footnote{The optimization problem intuition for the construction of adjoint functors is explained very well on \href{http://en.wikipedia.org/wiki/Adjoint_functors}{Wikipedia's ``adjoint functors'' entry} (retrieved on April 14, 2015). However, Wikipedia's suggestion that ``picking the right category [to express the universal property of the adjoint construction] is something of a knack'' is incorrect. A left adjoint to a functor $U : \mathsf{A} \to \mathsf{S}$ at an object $s \in \mathsf{S}$ defines an initial object in the category of elements of the functor $\mathsf{S}(s,U-) : \mathsf{A}\to \textup{\textsf{Set}}$; dually, a right adjoint defines a terminal object in the category of elements of $\mathsf{S}(U-,s) : \mathsf{A}^\mathrm{op} \to \textup{\textsf{Set}}$. See Proposition \ref{prop:rep-crit}.}



The same line of reasoning proves the following general result.

 A  functor $U : \mathsf{A} \to \mathsf{S}$ admits a left adjoint if and only if for each $s \in \mathsf{S}$ the comma category $s \mathrm{co}mma U$ has an initial object.


Comma categories are defined in Exercise \ref{exc:comma-category}: here, objects of $s \mathrm{co}mma U$ are  pairs $(a \in \mathsf{A}, f : s \to Ua \in \mathsf{S})$ and a morphism from $f : s \to Ua$ to $f' : s \to Ua'$ is a map  $h : a \to a' \in \mathsf{A}$ so that the evident triangle commutes in $\mathsf{S}$.


The comma category $s \mathrm{co}mma U$ is isomorphic to the category of elements for the functor $\mathsf{S}(s,U-) : \mathsf{A} \to \textup{\textsf{Set}}$. If a left adjoint $F$ exists, then the component of the unit  at $s$ defines an initial object $\eta_s : s \to UFs$ in this category; see Proposition \ref{prop:rep-crit} or Exercise \ref{exc:counit-UP}.

  Conversely, suppose each $s \mathrm{co}mma U$ admits an initial object, which we suggestively denote by $\eta_s : s \to UFs$. This defines the value of a function $F : \mathrm{ob}\mathsf{S} \to \mathrm{ob}\mathsf{A}$, which we now extend to a functor; the proof of Proposition \ref{prop:one-sided-adj} gives an alternate account of this same construction. For each morphism $f : s \to s'$ in $\mathsf{S}$, define $Ff : Fs \to Fs'$ to be the unique morphism in $\mathsf{A}$ making the square
$ \xymatrix{ s \ar[d]_f \ar[r]^-{\eta_s} & UFs \ar@{-->}[d]^{UFf} \\ s' \ar[r]_-{\eta_{s'}} & UFs'}$ commute; the fact that $\eta_s$ is initial in $s \mathrm{co}mma U$ implies the existence and uniqueness of such a map. The functoriality of $F$ follows from the uniqueness of these choices, so this construction defines a functor $F : \mathsf{S} \to  \mathsf{A}$ together with a natural transformation $\eta : 1_\mathsf{S} \Rightarrow UF$.

This data allows us to define a natural transformation $\phi : \mathsf{A}(F-,-) \Rightarrow \mathsf{S}(-,U-)$ with components
$ \phi_{s,a} : \mathsf{A}(Fs, a) \to \mathsf{S}(s,Ua)$ defined as in Remark \ref{rmk:unified-adjunction}\eqref{itm:unit-formula}: given a map $g : Fs \to a$ in $\mathsf{A}$, define $ \xymatrix{\phi_{s,a}(g) :=  s \ar[r]^-{\eta_s} & UFs \ar[r]^-{Ug} &Ua\rlap{,}}}$  Injectivity and surjectivity of $\phi_{s,a}$ follows immediately from the uniqueness and existence of morphisms from $\eta_s$ to any particular object $s \to Ua$ in $s \mathrm{co}mma U$. By Remark \ref{rmk:unified-adjunction}, this natural isomorphism proves that $F \dashv U$ with unit $\eta$.


Recall that a limit-preserving functor is called **continuous**; a colimit-preserving functor is called **cocontinuous**. Lemma \ref{lem:adjoint-criterion} reduces the problem of finding a left adjoint to a continuous functor $U : \mathsf{A} \to \mathsf{S}$ to the problem of finding an initial object in the comma category $s \mathrm{co}mma U$ defined for each $s \in \mathsf{S}$. This comma category, as the category of elements for $\mathsf{S}(s,U-) : \mathsf{A} \to \textup{\textsf{Set}}$, comes with a canonical forgetful functor $\Pi: s \mathrm{co}mma U \to \mathsf{A}$ that carries an object $s \to Ua$ to the object $a$.

 For any functor $U : \mathsf{A} \to \mathsf{S}$ and object $s \in \mathsf{S}$, the associated forgetful functor $\Pi : s \mathrm{co}mma U \to \mathsf{A}$ strictly creates the limit of any diagram whose limit exists in $\mathsf{A}$ and is preserved by $U$. In particular, if $\mathsf{A}$ is complete and $U$ is continuous, then $s \mathrm{co}mma U$ is complete.

 Lemma \ref{lem:comma-creates} is a special case of Exercise \ref{exc:elements-creates}, or can be proven directly via a straightforward extension of the argument used to prove Proposition \ref{prop:slice-creates}.


Lemma \ref{lem:comma-creates} can be used to produce an initial object in $s \mathrm{co}mma U$. By Lemma \ref{lem:terminal-colimit}, an initial object is equally the \emph{limit} of the identity functor. Applying Lemma \ref{lem:comma-creates}, a limit of the identity functor on $s \mathrm{co}mma U$ exists if and only if the limit of the forgetful functor $\Pi : s \mathrm{co}mma U \to \mathsf{A}$ exists in $\mathsf{A}$.

This line of reasoning seems to imply that all continuous functors whose domains are complete should admit left adjoints. This is not the case: the problem is that $s \mathrm{co}mma U$ is not in general a small category, so even if $\mathsf{A}$ admits all small limits it may not admit a limit of the large diagram $\Pi : s \mathrm{co}mma U \to \mathsf{A}$. The \emph{adjoint functor theorems}, the two most common of which are discussed here, supply conditions under which this large limit can be reduced to a small one that $\mathsf{A}$ possesses.

[\textnormal{General Adjoint Functor Theorem}] Let $U : \mathsf{A} \to \mathsf{S}$ be a continuous functor whose domain is locally small and complete. Suppose that $U$ satisfies the following **solution set condition**:


SUGGESTION: initial object