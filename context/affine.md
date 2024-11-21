---
layout: page
title: affine
permalink: /context/affine
---
To make this precise, define $\textup{Aff}_\mathbbe{k}(A)$ to be the set of finite formal affine linear combinations  $\sum_{i=1}^n\lambda_i \mathbf{a}_i$ so that $\sum_{i=1}^n \lambda_i = 1$; a sum is **affine** precisely when the coefficients sum to $1 \in \mathbbe{k}$. Two finite formal affine linear combinations are identified if they can be converted to one another by permuting the summands, deleting  summands whose coefficient is 0, and combining summands involving the same element $\mathbf{a} \in A$ by adding the field coefficients. To say ``these can be evaluated'' means there is a function $\mathrm{ev}_A : \textup{Aff}_\mathbbe{k}(A) \to A$.  For this map to define a reasonable evaluation function, a few axioms are required:

-  If $\eta_A : A \to \textup{Aff}_\mathbbe{k}(A)$ is the ``singleton'' function and $\mu_A : \textup{Aff}_\mathbbe{k}(\textup{Aff}_\mathbbe{k}(A)) \to \textup{Aff}_\mathbbe{k}(A)$ is the ``distributivity'' function, then the following diagrams
$ \xymatrix{ A \ar[r]^-{\eta_A} \ar[dr]_{1_A} & \textup{Aff}_\mathbbe{k}(A) \ar[d]^{\mathrm{ev}_A} & & \textup{Aff}_\mathbbe{k}(\textup{Aff}_\mathbbe{k}(A)) \ar[r]^-{\mu_A} \ar[d]_{\textup{Aff}_\mathbbe{k}(\mathrm{ev}_A)} & \textup{Aff}_\mathbbe{k}(A) \ar[d]^{\mathrm{ev}_A} \\ & A & & \textup{Aff}_\mathbbe{k}(A) \ar[r]_-{\mathrm{ev}_A} & A}$ commute in $\textup{\textsf{Set}}$.

The first condition says that the value of a singleton sum $1 \cdot \mathbf{a}$ is the element $\mathbf{a}$. The second condition says that an affine linear combination of affine linear combinations
$ \lambda_1 \cdot (\mu_{11}\mathbf{a}_{11} + \cdots + \mu_{1n_1}\mathbf{a}_{1n_1}) + \cdots + \lambda_k \cdot (\mu_{k1}\mathbf{a}_{k1} + \cdots + \mu_{kn_k}\mathbf{a}_{kn_k})$ can be evaluated by first distributing---note that $\sum_{i}\sum_j \lambda_i \mu_{ij} =1$---and then evaluating or by first evaluating inside each of the $k$ sets of parentheses and then evaluating the resulting affine linear combination. In summary, the precise meaning of Definition \ref{defn:affine-2} is:

SUGGESTION: affine linear combination