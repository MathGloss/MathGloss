---
layout: page
title: universal vector space equipped with a bilinear map
permalink: /context/universal_vector_space_equipped_with_a_bilinear_map
---
Theorem \ref{thm:yoneda} tells us that the natural isomorphism \eqref{eq:tensor-defn} is determined by a universal element of $\textup{Bilin}(V,W;V \otimes_\mathbbe{k} W)$, i.e., by a bilinear map $\otimes : V \times W \to V \otimes_\mathbbe{k} W$. The tensor product $V \otimes_\mathbbe{k} W$ is the **universal vector space equipped with a bilinear map** from $V \times W$. The Yoneda lemma can be used to unpack what this means. The natural isomorphism \eqref{eq:tensor-defn} identifies any bilinear map $f : V \times W \to U$ with a linear map $\bar{f} : V \otimes_\mathbbe{k} W \to U$. To understand this identification, consider the naturality square induced by $\bar{f}$.
$ \xymatrix{ \textup{\textsf{Vect}}_\mathbbe{k}(V \otimes_\mathbbe{k} W, V \otimes_\mathbbe{k} W) \ar[r]^-\mathrm{co}ng \ar[d]_{\bar{f}_*} & \textup{Bilin}(V,W;V \otimes_\mathbbe{k} W)\ar[d]^{\bar{f}_*} \\ \textup{\textsf{Vect}}_\mathbbe{k}(V \otimes_\mathbbe{k} W, U)  \ar[r]_-\mathrm{co}ng &  \textup{Bilin}(V,W;U)}$ Tracing $1_{V \otimes_\mathbbe{k} W}$ around this commutative square reveals that the bilinear map $f$ factors uniquely through the bilinear map $\otimes$ along the linear map $\bar{f}$.
$ \xymatrix{ V \times W \ar[dr]_f \ar[r]^-\otimes & V \otimes_\mathbbe{k} W \ar@{-->}[d]^{\bar{f}}_{\exists !} \\ & U}$
In other words, the bijection \eqref{eq:tensor-defn} is implemented by composing a linear map $V \otimes_\mathbbe{k} W \to U$ with the universal bilinear map $\otimes$. This universal property tells us that the bilinear map $\otimes : V \times W \to V \otimes_\mathbbe{k} W$ is initial in a category that will be described in Example \ref{exs:cat-of-elements}\eqref{itm:bilin}.

SUGGESTION: universal vector space