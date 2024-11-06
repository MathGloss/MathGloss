---
layout: page
title: absolute colimit
permalink: /context/absolute_colimit
---
\begin{lem}
The underlying fork of a split coequalizer diagram is a coequalizer. Moreover, it is an **absolute colimit**: any functor preserves this coequalizer.
\end{lem}
\begin{proof}
Given a map $k \colon y \to w$ so that $kf=kg$, we must show that $k$ factors through $h$; uniqueness of a hypothetical factorization follows because $h$ is a split epimorphism. The factorization is given by the map $ks \colon z \to w$, as demonstrated by the following easy diagram chase:
$$ ks h = kft=kgt=k.$$
