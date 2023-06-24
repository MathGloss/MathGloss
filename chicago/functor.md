---
 layout: page
 title: functor
 permalink: /chicago/functor
---
A covariant **functor** $F:\mathcal C\to \mathcal D$ is a map between [categories](https://defsmath.github.io/DefsMath/category) $\mathcal C$ and $\mathcal D$. It must assign to each object $A$ of $\mathcal C$ an object $F(A)$ an object of $\mathcal D$ and to each morphism $f:A\to B$ of $\mathcal C$ a morphism $F(f):f(A) \to f(B)$ of $\mathcal D$ such that
- $F(\text{id}_A)) = \text{id}_{F(A)}$;
- $F(g\circ f) = F(g)\circ F(f)$.

A contravariant functor "reverses the direction of arrows;" that is $F$ sends $f:A\to B$ to $F(f): f(B) \to f(A)$ and $F(g\circ f) = F(f) \circ F(g)$.

Wikidata ID: [Q864475](https://www.wikidata.org/wiki/Q864475)