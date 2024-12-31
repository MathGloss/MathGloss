---
layout: page
title: Eilenberg-Moore category
permalink: /context/Eilenberg-Moore_category
---
 Let $\mathsf{C}$ be a category with a monad $(T,\eta,\mu)$. The **Eilenberg--Moore category** for $T$ or the **category of $T$-algebras** is the category $\mathsf{C}^T$ whose: 
-  objects are pairs $(A \in \mathsf{C}, a : TA \to A)$, so that the diagrams
 \vcenter{ \xymatrix{ A \ar[r]^-{\eta_A} \ar[dr]_{1_A} & TA \ar[d]^{a} & & T^2A \ar[r]^-{\mu_A} \ar[d]_{Ta} & TA \ar[d]^{a} \\ & A & & TA \ar[r]_-{a} & A}}
commute in $\mathsf{C}$, and
-  morphisms $f : (A,a) \to (B,b)$ are $T$-algebra **homomorphisms**: maps $f : A \to B$ in $\mathsf{C}$ so that the square
$ \xymatrix{ TA \ar[d]_a \ar[r]^{Tf} & TB \ar[d]^b \\ A \ar[r]_f & B}$ commutes,  with composition and identities as in $\mathsf{C}$.



SUGGESTION: Eilenberg-Moore category

From [Category Theory in Context](https://mathgloss.github.io/MathGloss/context.html)