---
layout: page
title: coalgebra
permalink: /context/coalgebra
---
 A }}**coalgebra** for an endofunctor $T : \mathsf{C} \to \mathsf{C}$ is an object $C \in \mathsf{C}$ equipped with a map $\gamma : C \to TC$. A morphism $f : (C,\gamma) \to (C',\gamma')$ of coalgebras is a map $f : C \to C'$ so that the square
$ \xymatrix{C \ar[d]_\gamma \ar[r]^f & C' \ar[d]^{\gamma'} \\ TC \ar[r]_{Tf} & TC'}$ commutes. Prove that if $(C,\gamma)$ is a **terminal coalgebra**, that is a terminal object in the category of coalgebras, then the map $\gamma : C  \to TC$ is an isomorphism.


SUGGESTION: terminal coalgebra

From [Category Theory in Context](https://mathgloss.github.io/MathGloss/context.html)