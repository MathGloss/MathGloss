---
layout: page
title: category of $T$-algebras
permalink: /context/category_of_$t$-algebras
---
Let $\mathsf{C}$ be a category with a monad $(T,\eta,\mu)$. The **Eilenberg--Moore category** for $T$ or the **category of $T$-algebras** is the category $\mathsf{C}^T$ whose: 1. objects are pairs $(A \in \mathsf{C}, a \colon TA \to A)$, so that the diagrams
$$ \vcenter{ \xymatrix{ A \ar[r]^-{\eta_A} \ar[dr]_{1_A} & TA \ar[d]^{a} & & T^2A \ar[r]^-{\mu_A} \ar[d]_{Ta} & TA \ar[d]^{a} \\ & A & & TA \ar[r]_-{a} & A}}$$
commute in $\mathsf{C}$, and
2. morphisms $f \colon (A,a) \to (B,b)$ are $T$-algebra **homomorphisms**: maps $f \colon A \to B$ in $\mathsf{C}$ so that the square
$$ \xymatrix{ TA \ar[d]_a \ar[r]^{Tf} & TB \ar[d]^b \\ A \ar[r]_f & B}$$ commutes,  with composition and identities as in $\mathsf{C}$.
