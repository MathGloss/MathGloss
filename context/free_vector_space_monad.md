---
layout: page
title: free vector space monad
permalink: /context/free_vector_space_monad.md
---
-  The free $\dashv$ forgetful adjunction between sets and the category of $R$-modules of Example \ref{exs:free-forgetful}\eqref{itm:mod-free-forgetful} induces the **free $R$-module monad** $R[-] : \textup{\textsf{Set}} \to \textup{\textsf{Set}}$. Define $R[A]$ to be the set of finite formal $R$-linear combinations of elements of $A$. Formally, a finite $R$-linear combination is a finitely supported function $\chi: A \to R$, meaning a function for which only finitely many elements of its domain take non-zero values. Such a function might be written as $\sum_{a \in A} \chi(a) \cdot a$. The components $\eta_A : A \to R[A]$ of the unit send an element $a \in A$ to the singleton formal $R$-linear combination corresponding to the function $\chi_a : A \to R$ that sends $a$ to $1 \in R$ and every other element to zero. The components $\mu_A : R[R[A]] \to R[A]$ of the multiplication are defined by distributing the coefficients in a formal sum of formal sums.   Special cases of interest include the **free abelian group monad** and the **free vector space monad**.

SUGGESTION: free $R$-module monad