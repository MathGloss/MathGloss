---
layout: page
title: dual vector space
permalink: /context/dual_vector_space.md
---
-  There is a functor $(-)^* : \textup{\textsf{Vect}}_\mathbbe{k}^\mathrm{op} \to \textup{\textsf{Vect}}_\mathbbe{k}$ that carries a vector space to its **dual vector space** $V^* = \mathrm{Hom}(V,\mathbbe{k})$. A vector in $V^*$ is a **linear functional** on $V$, i.e., a linear map $V \to \mathbbe{k}$. This functor is contravariant, with a linear map $\phi : V \to W$ sent to the linear map $\phi^* : W^* \to V^*$ that pre-composes a linear functional $W \xrightarrow{\omega} \mathbbe{k}$ with $\phi$ to obtain a linear functional $V \xrightarrow{\phi} W \xrightarrow{\omega} \mathbbe{k}$.

SUGGESTION: dual vector space