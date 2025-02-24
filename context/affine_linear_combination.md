---
layout: page
title: affine linear combination
permalink: /context/affine_linear_combination
---
There is an equivalent definition that allows us to define an affine space without making use of the auxiliary vector space $V$. If we temporarily fix an origin $\mathbf{o} \in A$, then for any pair of elements $\mathbf{a}, \mathbf{b} \in A$ of the affine space and any scalar $\lambda \in \mathbbe{k}$, we can exploit the bijection $-+\mathbf{o} : V \to A$ to see that there is a unique $\mathbf{c} \in A$ so that
$ \mathbf{c} - \mathbf{o} = \lambda ( \mathbf{a} - \mathbf{o}) + (1-\lambda) (\mathbf{b} - \mathbf{o})\rlap{,}}$ This element $\mathbf{c}$ is sensibly denoted by $\lambda \mathbf{a} + (1-\lambda)\mathbf{b}$ and is independent of the choice of origin. More generally, for any $n$-tuple $\mathbf{a}_1,\ldots, \mathbf{a}_n \in A$ and scalars $\lambda_1,\ldots, \lambda_n \in \mathbbe{k}$ with $\lambda_1 + \cdots + \lambda_n =1$, there is a unique element $\lambda_1 \mathbf{a}_1 + \cdots + \lambda_n \mathbf{a}_n \in A$ defined analogously as an **affine linear combination** of $\mathbf{a}_i$. This leads to a second equivalent definition of affine space.

SUGGESTION: affine linear combination

From [Category Theory in Context](https://mathgloss.github.io/MathGloss/context.html)