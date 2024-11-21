---
layout: page
title: discrete dynamical system
permalink: /context/discrete_dynamical_system
---

A set $X$ with an endomorphism $f : X \to X$ and a distinguished element $x_0$ is called a **discrete dynamical system**. This data allows one to consider the discrete-time evolution of the initial element $x_0$, a sequence defined by $x_{n+1} :eqq f(x_n)$. The principle of mathematical recursion asserts that the natural numbers $\mathbb{N}$, the successor function $s : \mathbb{N} \to \mathbb{N}$, and the element $0 \in \mathbb{N}$ define the **universal discrete dynamical system**: which is to say, there is a unique function $r : \mathbb{N} \to X$ so that $r(n) = x_n$ for each $n$, i.e., so that $r(0)=x_0$ and so that the diagram
\vcenter{\xymatrix{ \mathbb{N} \ar[r]^s \ar[d]_r & \mathbb{N} \ar[d]^r \\ X \ar[r]_f & X}} commutes.


SUGGESTION: discrete dynamical system

From [Category Theory in Context](https://mathgloss.github.io/MathGloss/context.html)