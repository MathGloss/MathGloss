---
layout: page
title: idempotent monad
permalink: /context/idempotent_monad
---
A particularly simple family of examples of monadic functors is given by inclusions of reflective subcategories (see Definition \ref{defn:reflective-subcat}). Consider a reflective subcategory $\mathsf{D} \hookrightarrow \mathsf{C}$ with reflector $L$. The induced endofunctor $L : \mathsf{C} \to \mathsf{C}$ defines a monad on $\mathsf{C}$ with unit $\eta_C : C \to LC$ and multiplication a natural isomorphism $L^2C \mathrm{co}ng LC$. A monad whose multiplication natural transformation is invertible is called an **idempotent monad**; see  Exercises \ref{exc:reflective-subcategory} and \ref{exc:reflective-monad}.

SUGGESTION: idempotent monad

From [Category Theory in Context](https://mathgloss.github.io/MathGloss/context.html)