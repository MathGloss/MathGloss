---
layout: page
title: G-equivariant
permalink: /context/G-equivariant
---
-  For $G$ a group, Example \ref{ex:G-actions} shows that a functor $X: \mathsf{B} G \to \mathsf{C}$ corresponds to an object $X \in \mathsf{C}$ equipped with a left action of $G$, which suggests a question: What is a natural transformation between a pair $X,Y : \mathsf{B} G \rightrightarrows \mathsf{C}$ of such functors? Because the category $\mathsf{B} G$ has only one object, the data of $\alpha : X \Rightarrow Y$ consists of a single morphism $\alpha : X \to Y$ in $\mathsf{C}$ that is **$G$-equivariant**, meaning that for each $g \in G$, the diagram
$ \xymatrix{ X \ar[r]^\alpha \ar[d]_{g_*} & Y\ar[d]^{g_*} \\ X \ar[r]_\alpha & Y} $ commutes.

SUGGESTION: $G$-equivariant morphism

From [Category Theory in Context](https://mathgloss.github.io/MathGloss/context.html)