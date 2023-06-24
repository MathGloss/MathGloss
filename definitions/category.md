---
aliases: morphism, object
---
A **category** $\mathcal C$ is a collection of **objects** together with a set $\mathcal C(A,B)$ of **morphisms** or maps between any two objects. In particular, there is always for each object $A$ in $\mathcal C$ an identity morphism $\text{id}_A \in\mathcal C(A,A)$. Finally, a category must obey the following composition law: $$\circ: \mathcal C(B,C)\times \mathcal C(A,B) \to \mathcal C(A,C)$$ for all triples $A$, $B$, $C$ of objects such that composition is [[associative]], and identity morphisms  are [[identity element|identities]] for composition. That is, 
- $h\circ(g\circ f) = (h\circ g)\circ f$;
- $\text{id}\circ f = f$;
- $f\circ \text{id} = f$.

https://www.wikidata.org/wiki/Q719395