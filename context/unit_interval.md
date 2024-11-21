---
layout: page
title: unit interval
permalink: /context/unit_interval
---
The **unit interval** is the topological space $I = [0,1] \subset \mathbb{R}$ regarded as a subspace of the real line, with the standard Euclidean metric topology. It is used to define the fundamental groupoid $\Pi_1(X)$ of paths in a topological space $X$. A **path** in $X$ is simply a continuous function $p : I \to X$. The path has two endpoints $p(0), p(1)\in X$ defined by evaluating at the endpoints $0,1 \in I$. If $q : I \to X$ is a second path with the property that $p(1)=q(0)$, then there exists a composite path $p \ast q : I \to X$ defined by the composite continuous function
$ \xymatrix{ I \ar[r]^-{\delta}_-\mathrm{co}ng & I \vee I \ar[r]^-{p \vee q} & X.}$ Here $I \vee I$ is the space formed by gluing two copies of $I$ together by identifying the point $1$ in the left-hand copy with the point $0$ in the right-hand copy:
$ \xymatrix{ \ast \ar[d]_{1} \ar[r]^{0} \ar@{}[dr]|(.8){\displaystyle\ulcorner} & I \ar[d] \\ I \ar[r] & I \vee I}$
The space $I \vee I$ is homeomorphic to the space $[0,2] \subset \mathbb{R}$. The map $\delta : I \to I \vee I$ is the homeomorphism $t \mapsto 2t$. Note that this map sends the endpoints of the domain $I$ to the endpoints of the fattened interval $I \vee I$. Thus, $(p \ast q)(0) = p(0)$ and $(p \ast q)(1) = q(1)$; that is, $p \ast q$ is a path in $X$ from the starting point of the path $p$ to the ending point of the path $q$.

SUGGESTION: unit interval

From [Category Theory in Context](https://mathgloss.github.io/MathGloss/context.html)