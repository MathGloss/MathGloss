---
layout: page
title: classifying function
permalink: /context/classifying_function.md
---
-  The contravariant power set functor $P : \textup{\textsf{Set}}^\mathrm{op} \to \textup{\textsf{Set}}$ is represented by the set $\Omega = \{\top,\bot\}$ with two elements. The natural isomorphism $\textup{\textsf{Set}}(A,\Omega) \mathrm{co}ng PA$ is defined by the bijection that associates a function $A \to \Omega$ with the subset that is the preimage of $\top$; reversing perspectives, a subset $A' \subset A$ is identified with its **classifying function** $\chi_{A'} : A \to \Omega$, which sends exactly the elements of $A'$ to the element $\top$. The naturality condition stipulates that for any function $f : A \to B$, the diagram
$ \xymatrix{ \textup{\textsf{Set}}(B,\Omega) \ar[r]^-{\mathrm{co}ng} \ar[d]_{f^{*}} & PB \ar[d]^{f^{-1}} \\ \textup{\textsf{Set}}(A,\Omega) \ar[r]_-\mathrm{co}ng & PA}$ commutes. That is, naturality asserts that given a function $\chi_{B'} : B \to \Omega$ classifying the subset $B' \subset B$, the composite function $A \xrightarrow{f} B \xrightarrow{\chi_{B'}} \Omega$ classifies the subset $f^{-1}(B')\subset A$.

SUGGESTION: classifying function