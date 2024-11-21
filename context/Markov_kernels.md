---
layout: page
title: Markov kernels
permalink: /context/Markov_kernels
---
-  The Kleisli category for the Giry monad of Example \ref{exs:nat-monads}\eqref{itm:Giry} is the category of measurable spaces and **Markov kernels**. For instance, a finite set defines a measurable space with discrete $\sigma$-algebra. An endomorphism of this object in the Kleisli category is a **discrete time Markov chain**.



 For any  monad $(T,\eta,\mu)$ acting on a category $\mathsf{C}$, there is an adjunction
$ \xymatrix{ \mathsf{C} \ar@<1ex>[r]^-{F_T} \ar@{}[r]|-\perp & \mathsf{C}_T \ar@<1ex>[l]^-{U_T}}$ between $\mathsf{C}$ and the Kleisli category whose induced monad is $(T,\eta,\mu)$.


The functor $F_T$ is the identity on objects and carries a morphism $f : A \to B$ in $\mathsf{C}$ to the morphism $A \rightsquigarrow B$ in $\mathsf{C}_T$ defined by
$ F_Tf :eqq A \xrightarrow{f} B \xrightarrow{\eta_B} TB\rlap{,}}$ The functor $U_T$ sends an object $A \in \mathsf{C}_T$ to $TA \in \mathsf{C}$ and sends a morphism $A \rightsquigarrow B$ represented by $g : A \to TB$ to
$ U_Tg :eqq TA \xrightarrow{Tg} T^2B \xrightarrow{\mu_B} TB\rlap{,}}$
Elementary diagram chases, left as Exercise \ref{exc:kleisli}, demonstrate that both mappings are functorial.  Note in particular that $U_T F_T = T$. From the definition of the hom-sets in $\mathsf{C}_T$, there are isomorphisms
$ \mathsf{C}_T(F_TA,B) \mathrm{co}ng \mathsf{C}(A,TB) \mathrm{co}ng \mathsf{C}(A,U_TB)\rlap{,},}$ which are natural in both variables. This establishes the adjunction $F_T \dashv U_T$.




For any monad $(T,\eta,\mu)$ on $\mathsf{C}$, there is a category _{T}$, of adjunctions inducing a monad $T$ and maps of adjunctions}$\textup{\textsf{Adj}}_{T}$ whose objects are fully-specified adjunctions
$ \xymatrix{ \mathsf{C} \ar@<1ex>[r]^F \ar@{}[r]|\perp & \mathsf{D} \ar@<1ex>[l]^U} \qquad\qquad \eta : 1_\mathsf{C} \Rightarrow UF,\quad \epsilon : FU \Rightarrow 1_\mathsf{D}$
inducing the monad $(T,\eta,\mu)$ on $\mathsf{C}$. A morphism
$ \xymatrix{ \mathsf{D} \ar[rr]^K \ar@<1ex>[dr]^U  \ar@{}[dr]|{\rotatebox{45}{$\dashv$}} & & \mathsf{D}' \ar@<1ex>[dl]^{U'} \ar@{}[dl]|{\rotatebox{-45}{$\dashv$}} \\ & \mathsf{C} \ar@<1ex>[ul]^F \ar@<1ex>[ur]^{F'}}$
from $F\dashv U$ to $F'\dashv U'$ is a functor $K : \mathsf{D} \to \mathsf{D}'$ commuting with both the left and right adjoints, i.e., so that $KF =F'$ and $U'K =U$. Because the units of $F \dashv U$ and $F' \dashv U'$ are the same, by Exercise \ref{exc:adj-mor} the commutativity of $K$ with the right and left adjoints implies further that


SUGGESTION: adjunction