---
layout: page
title: comonad
permalink: /context/comonad
---
A **comonad** on $\mathsf{C}$ is a monad on $\mathsf{C}^\mathrm{op}$: explicitly, a comonad consists of an endofunctor $K \colon \mathsf{C} \to \mathsf{C}$ together with natural transformations $\epsilon \colon K \Rightarrow 1_\mathsf{C}$ and $\delta \colon K \Rightarrow K^2$ so that the diagrams dual to Definition \ref{defn:monad} commute in $\mathsf{C}^\mathsf{C}$.
