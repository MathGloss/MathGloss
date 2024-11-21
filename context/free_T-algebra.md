---
layout: page
title: free T-algebra
permalink: /context/free_T-algebra
---
Various notations are common for the Eilenberg--Moore category, many involving the string ``alg '' to emphasize the interpretation of its objects as ``algebras'' of some sort. The notation used here, while less evocative, has the virtue of being concise.
\
 For any  monad $(T,\eta,\mu)$ acting on a category $\mathsf{C}$, there is an adjunction
$ \xymatrix{ \mathsf{C} \ar@<1ex>[r]^-{F^T} \ar@{}[r]|-\perp & \mathsf{C}^T \ar@<1ex>[l]^-{U^T}}$ between $\mathsf{C}$ and the Eilenberg--Moore category whose induced monad is $(T,\eta,\mu)$.


The functor $U^T : \mathsf{C}^T \to \mathsf{C}$ is the evident forgetful functor.  The functor $F^T : \mathsf{C} \to \mathsf{C}^T$ carries an object $A \in \mathsf{C}$ to the **free $T$-algebra** $ F^T\! A :eqq (TA,\mu_A : T^2A \to TA)$ and carries a morphism $f : A \to B$ to the **free $T$-algebra morphism** $ F^T\! f :eqq  (TA,\mu_A) \xrightarrow{Tf} (TB,\mu_B)\rlap{,}}$ Note that $U^TF^T=T$.

SUGGESTION: free T-algebra