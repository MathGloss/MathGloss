---
layout: page
title: cycles
permalink: /context/cycles
---
-  For each $n \in \mathbb{Z}$, there are functors $Z_n, B_n, H_n : \textup{\textsf{Ch}}_R \to \textup{\textsf{Mod}}_R$. The functor $Z_n$ computes the $n$-**cycles** defined by $Z_nC_\bullet = \textup{ker}(d : C_n \to C_{n-1})$. The functor $B_n$ computes the $n$-**boundary** defined by $B_nC_\bullet = \textup{im}(d : C_{n+1} \to C_n)$. The functor $H_n$ computes the $n$th **homology** $H_nC_\bullet :eqq Z_nC_\bullet / B_nC_\bullet$. We leave it to the reader to verify that each of these three constructions is functorial. Considering all degrees simultaneously, the cycle, boundary, and homology functors assemble into functors $Z_*,B_*, H_* : \textup{\textsf{Ch}}_R \to \textup{\textsf{GrMod}}_R$_R$, of $\mathbb{Z}$-graded $R$-modules and graded homomorphisms} from the category of chain complexes to the category of graded $R$-modules. The singular homology of a topological space is defined by precomposing $H_*$ with a suitable functor $\textup{\textsf{Top}} \to \textup{\textsf{Ch}}_R$.

SUGGESTION: n-cycles