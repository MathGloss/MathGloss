---
layout: page
title: total derivative
permalink: /context/total_derivative
---
-  The chain rule expresses the functoriality of the derivative. Let _*$, of pointed Euclidean spaces and pointed differentiable functions}$\textup{\textsf{Euclid}}_*$ denote the category whose objects are pointed finite-dimensional Euclidean spaces $(\mathbb{R}^n,a)$---or, better, open subsets thereof---and whose morphisms are pointed differentiable functions. The **total derivative** of $f : \mathbb{R}^n \to \mathbb{R}^m$, evaluated at the designated basepoint $a \in \mathbb{R}^n$,  gives rise to a matrix called the **Jacobian matrix** defining the directional derivatives of $f$ at the point $a$. If $f$ is given by component functions $f_1,\ldots, f_m : \mathbb{R}^n \to \mathbb{R}$, the $(i,j)$-entry of this matrix is $\frac{\partial}{\partial x_j} f_i(a)$.  This defines the action on morphisms of a functor $D : \textup{\textsf{Euclid}}_* \to \textup{\textsf{Mat}}_\mathbb{R}$; on objects, $D$ assigns a pointed Euclidean space its dimension. Given $g : \mathbb{R}^m \to \mathbb{R}^k$ carrying the designated basepoint $f(a) \in \mathbb{R}^m$ to $gf(a) \in \mathbb{R}^k$, functoriality of $D$ asserts that the product of the Jacobian of $f$ at $a$ with the Jacobian of $g$ at $f(a)$ equals the Jacobian of $gf$ at $a$. This is the chain rule from multivariable calculus.\footnote{Taking a more sophisticated perspective,  the derivative defines the action on morphisms of a functor from the category _*$, of pointed smooth manifolds and  pointed smooth functions}$\textup{\textsf{Man}}_*$ to the category of real vector spaces that sends a pointed manifold to its tangent space.}

SUGGESTION: total derivative

From [Category Theory in Context](https://mathgloss.github.io/MathGloss/context.html)