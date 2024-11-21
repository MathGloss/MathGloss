---
layout: page
title: exact sequence
permalink: /context/exact_sequence
---
The **image** of a morphism is defined to be the kernel of its cokernel, or equivalently, the cokernel of its kernel; these objects are always isomorphic in an abelian category. This permits the definition of an **exact sequence** in an abelian category, a sequence of composable morphisms $ \xymatrix{ \cdots \ar[r]^{f_{n+2}} & A_{n+1} \ar[r]^{f_{n+1}} \ar[r] & A_n \ar[r]^{f_n} & A_{n-1} \ar[r]^{f_{n-1}} & \cdots}$ so that $\ker f_n = \mathrm{im} f_{n+1}$. Classical results such as the \emph{five lemma}, which is used to detect isomorphisms between a pair of exact sequences, can be proven by general abstract nonsense in any abelian category using the universal properties of kernels and cokernels.

SUGGESTION: exact sequence