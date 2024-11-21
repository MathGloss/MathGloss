---
layout: page
title: G-space
permalink: /context/G-space.md
---
-  $e_* = 1_X$, where $e \in G$ is the identity element.

In summary, the functor $\mathsf{B} G \to \mathsf{C}$ defines an **action** of the group $G$ on the object $X \in \mathsf{C}$. When $\mathsf{C}=\textup{\textsf{Set}}$, the object $X$ endowed with such an action is called a **$G$-set**. When $\mathsf{C}=\textup{\textsf{Vect}}_\mathbbe{k}$, the object $X$ is called a **$G$-representation**. When $\mathsf{C}=\textup{\textsf{Top}}$, the object $X$ is called a **$G$-space**. Note the utility of this categorical language for defining several analogous concepts simultaneously.


The action specified by a functor $\mathsf{B} G \to \mathsf{C}$ is sometimes called a **left action**. A **right action** is a functor $\mathsf{B} G^\mathrm{op} \to \mathsf{C}$. As before, each $g \in G$ determines an endomorphism $g^* : X \to X$ in $\mathsf{C}$ and the identity element must act trivially. But now, for a pair of elements $g,h \in G$ these actions must satisfy the composition rule $(hg)^*=g^*h^*$.

Because the elements $g \in G$ are isomorphisms when regarded as morphisms in the 1-object category $\mathsf{B} G$ that represents the group, their images under any such functor must also be isomorphisms in the target category. In particular, in the case of a $G$-representation $V : \mathsf{B} G \to \textup{\textsf{Vect}}_\mathbbe{k}$, the linear map $g_* : V \to V$ must be an \emph{automorphism} of the vector space $V$.
The point is that the functoriality axioms \eqref{itm:G-action-i} and \eqref{itm:G-action-ii} imply automatically that each $g_*$ is an automorphism and that $(g^{-1})_* = (g_*)^{-1}$; the proof is a special case of Lemma \ref{lem:functors-pres-isos}.


In summary:

 When a group $G$ acts functorially on an object $X$ in a category $\mathsf{C}$, its elements $g$ must act by automorphisms $g_* : X \to X$ and, moreover, $(g_*)^{-1} = (g^{-1})_*$.


A functor may or may not preserve monomorphisms or epimorphisms, but an argument similar to the proof of Lemma \ref{lem:functors-pres-isos} shows that a functor necessarily preserves split monomorphisms and split epimorphisms. The retraction or section defines an ``equational witness'' for the mono or the epi.



We leave it to the reader to verify that the assignments just described satisfy the two functoriality axioms. Note that Lemma \ref{lem:functors-pres-isos} specializes in the case of represented functors to give a proof of the implications $\eqref{itm:iso-i}\Rightarrow\eqref{lem:iso-post}$ and $\eqref{itm:iso-i}\Rightarrow\eqref{lem:iso-pre}$ of Lemma \ref{lem:iso}. These functors will play a starring role in Chapter \ref{ch:yoneda}, where a number of examples in disguise are discussed.

The data of the covariant and contravariant functors introduced in Definition \ref{defn:rep-functor} may be encoded in a single **bifunctor**, which is the name for a functor of two variables. Its domain is given by the product of a pair of categories.





At the beginning of this section, it was suggested that functors define morphisms between categories. Indeed, categories and functors assemble into a category. Here the size issues are even more significant than we have encountered thus far. To put a lid on things, define $, of small categories and functors}$\textup{\textsf{Cat}}$ to be the category whose objects are small categories and whose morphisms are functors between them. This category is locally small but not small: it contains $\textup{\textsf{Set}}$, $\textup{\textsf{Poset}}$, $, of monoids and homomorphisms}$\textup{\textsf{Monoid}}$,  $\textup{\textsf{Group}}$, and  $\textup{\textsf{Groupoid}}$  as proper subcategories (see Exercises \ref{exc:group-functor} and \ref{exc:preorder-functor}). However, none of these categories are \emph{objects} of $\textup{\textsf{Cat}}$.

 The non-small categories of Example \ref{exs:concrete-categories} are objects of $, of locally small categories and functors}$\textup{\textsf{CAT}}$, some category of ``large'' categories and functors between them. Russell's paradox suggests that $\textup{\textsf{CAT}}$ should not be so large as to contain itself, so we require the objects in $\textup{\textsf{CAT}}$ to be locally small categories; the category $\textup{\textsf{CAT}}$ defined in this way is not locally small, and so is thus excluded. There is an inclusion functor $\textup{\textsf{Cat}}\hookrightarrow\textup{\textsf{CAT}}$ but no obvious functor pointing in the other direction.

The category of categories gives rise to a notion of an **isomorphism of categories**, defined by interpreting Definition \ref{defn:iso} in $\textup{\textsf{Cat}}$ or in $\textup{\textsf{CAT}}$. Namely, an isomorphism of categories is given by a pair of inverse functors $F : \mathsf{C} \to \mathsf{D}$ and $G : \mathsf{D} \to \mathsf{C}$ so that the composites $GF$ and $FG$, respectively, equal the identity functors on $\mathsf{C}$ and on $\mathsf{D}$. An isomorphism induces a bijection between the objects of $\mathsf{C}$ and objects of $\mathsf{D}$ and likewise for the morphisms.

 For instance:


SUGGESTION: G-space