---
layout: page
title: adic integers
permalink: /context/adic_integers.md
---
 For instance, the $p$-**adic integers** are defined to be the limit of an $\bbomega^\mathrm{op}$-indexed diagram of rings
$ \xymatrix{ \mathbb{Z}_p :eqq \lim_n \mathbb{Z}/p^n \ar[r] & \cdots \ar[r] & \mathbb{Z}/p^3 \ar[r] & \mathbb{Z}/p^2 \ar[r] & \mathbb{Z}/p}$ By Example \ref{ex:set-inverse}, because  $U : \textup{\textsf{Ring}} \to \textup{\textsf{Set}}$ preserves limits, as a set
$ \mathbb{Z}_p = \Big\{ (a_1 \in \mathbb{Z}/p, a_2 \in \mathbb{Z}/p^2, a_3 \in \mathbb{Z}/p^3,\ldots) \Bigm| a_n \equiv a_m\ \mathrm{mod}\ p^{\mathrm{min}(n,m)}\Big\}\rlap{,}}$ That is, a $p$-adic integer is a sequence of elements $a_n \in \mathbb{Z}/p^n$ that are compatible modulo congruence.

SUGGESTION: p-adic integer