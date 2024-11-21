---
layout: page
title: monoidal product
permalink: /context/monoidal_product
---
The data of a **symmetric monoidal category** $(\mathsf{V},\otimes,{*})$ consists of a category $\mathsf{V}$, a bifunctor $-\otimes -: \mathsf{V} \times \mathsf{V} \to \mathsf{V}$ called the **monoidal product**, and a **unit object** ${*} \in \mathsf{V}$ together with specified natural isomorphisms
  v\otimes w \underset{\gamma}{\mathrm{co}ng} w \otimes v \qquad u \otimes (v \otimes w) \underset{\alpha}{\mathrm{co}ng} (u \otimes v) \otimes w \qquad {*} \otimes v \underset{\lambda}{\mathrm{co}ng} v \underset{\rho}{\mathrm{co}ng} v \otimes * witnessing  symmetry, associativity, and unit conditions on the monoidal product. The natural transformations \eqref{eq:symmonisos} must satisfy certain ``coherence conditions'' that will be discussed momentarily. A **mon\-oid\-al category** is defined similarly, except that the first symmetry natural isomorphism is omitted.

SUGGESTION: symmetric monoidal category