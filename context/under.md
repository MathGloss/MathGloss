---
layout: page
title: under
permalink: /context/under
---
 Objects in the category of elements of $\mathsf{C}(c,-)$ are morphisms $f : c \to x$ in $\mathsf{C}$, i.e., the objects of $\textstyle{\int}\!{\mathsf{C}(c,-)}$ are morphisms in $\mathsf{C}$ with domain $c$. A morphism from $f : c \to x$ to $g : c \to y$ is a morphism $h : x \to y$ so that $g = hf$; we say that $h$ is a morphism under $c$:
$ \xymatrix@=10pt{ & c \ar[dl]_f \ar[dr]^g \\ x \ar[rr]_h & & y}$ This category has another name: it is the **slice category** $c/\mathsf{C}$ **under** the object $c \in \mathsf{C}$ introduced in Exercise \ref{exc:slice-category}. The forgetful functor $c/\mathsf{C} \to \mathsf{C}$ sends a morphism $f : c \to x$ to its codomain and a commutative triangle to the leg opposite the object $c$.

SUGGESTION: morphism under $c$

From [Category Theory in Context](https://mathgloss.github.io/MathGloss/context.html)