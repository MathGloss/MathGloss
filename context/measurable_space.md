---
layout: page
title: measurable space
permalink: /context/measurable_space
---
-  The **Giry monad** acts on the category $\textup{\textsf{Meas}}$ of measurable spaces and measurable functions. A **measurable space** is a set equipped with a $\sigma$-\emph{algebra} of ``measurable'' subsets, and a function $f : A \to B$ between measurable spaces is **measurable** if the preimage of any measurable subset of $B$ is a measurable subset of $A$. The Giry monad sends a measurable space $A$ to the measurable space $\textup{Prob}(A)$ of \emph{probability measures} on $A$, equipped with the smallest $\sigma$-algebra so that, for each measurable subset $X \subset A$, the evaluation function $\mathrm{ev}_X : \textup{Prob}(A) \to I$ is measurable. The unit is the measurable function  $\eta_A : A \to \textup{Prob}(A)$  that sends each element $a \in A$ to the Dirac measure, which assigns a subset the probability 1 if it contains $a$ and 0 otherwise.   The multiplication is defined using integration; see \cite{Giry-Probability} or \cite{Avery-Codensity} for details.



Briefly:



A comonad is a comonoid in the category of endofunctors of $\mathsf{C}$. By the dual to Lemma \ref{lem:monad-from-adj}, any adjunction induces a comonad on the domain of its right adjoint.

 A monad on a preorder $(\mathsf{P}, \leq)$ is given by an order-preserving function $T : \mathsf{P} \to \mathsf{P}$ that is so that $p \leq Tp$ and  $T^2p \leq Tp$. If $\mathsf{P}$ is a poset, so that isomorphic objects are equal, these two conditions imply that $T^2 p = Tp$. An order-preserving function $T$ so that $p \leq Tp$ and $T^2 p = Tp$ is called a **closure operator**.  Dually, a comonad on a poset category $(\mathsf{P}, \leq)$ defines a **kernel operator**: an order-preserving function $K$ so that $Kp \leq p$ and $K p = K^2 p$.

For example, the poset $PX$ of subsets of a topological space $X$ admits a closure operator $TA = \overline{A}$, where $\overline{A}$ is the closure of $A \subset X$, and a kernel operator $KA = A^\circ$, where $A^\circ$ is the interior of $A \subset X$.\footnote{The **closure** of $A$ is the smallest closed set containing $A$, equally the intersection of all closed sets containing $A$; the **interior** is defined dually.}



\subsection*{Exercises}%mon


Suppose $\mathsf{V}$ is a monoidal category (see \S\ref{sec:monoidal}), i.e., a category with a bifunctor $\otimes : \mathsf{V} \times \mathsf{V} \to \mathsf{V}$ that is associative up to coherent natural isomorphism\footnote{Rather than worry about what this means, feel free to assume that there is a well-defined $n$-ary functor $\mathsf{V}^{\times n} \xrightarrow{\otimes^n} \mathsf{V}$ built from the bifunctor $\otimes$.}  and a unit object $* \in \mathsf{V}$ with natural isomorphisms $v \otimes * \mathrm{co}ng v \mathrm{co}ng * \otimes v$.
Suppose also that $\mathsf{V}$ has finite coproducts and that the bifunctor $\otimes$ preserves them in each variable.\footnote{In particular, $(v \sqcup v') \otimes (w \sqcup w') \mathrm{co}ng v\otimes w \sqcup v' \otimes w \sqcup v \otimes w' \sqcup v' \otimes w'$.}
Show that $T(X) = \mathrm{co}prod_{n \geq 0} X^{\otimes n}$ defines a monad on $\mathsf{V}$ by defining natural transformations $\eta : 1_\mathsf{V} \Rightarrow T$ and  $\mu : T^2 \Rightarrow T$ that satisfy the required conditions.



Show that the functor $\beta : \textup{\textsf{Set}} \to \textup{\textsf{Set}}$ that carries a set to the set of ultrafilters on that set is a monad by defining unit and multiplication natural transformations that satisfy the unit and associativity laws. (Hint: The ultrafilter monad is a submonad of the double power set monad $P^2 : \textup{\textsf{Set}} \to \textup{\textsf{Set}}$.)



The adjunction associated to a reflective subcategory of $\mathsf{C}$ induces an **idempotent monad** on $\mathsf{C}$. Prove that the following three characterizations of an idempotent monad $(T,\eta,\mu)$ are equivalent:


SUGGESTION: monad

From [Category Theory in Context](https://mathgloss.github.io/MathGloss/context.html)