---
layout: page
title: cone
permalink: /context/cone
---
The **cone** under a small category $\mathsf{J}$ is the category $\mathsf{J}^\triangleright$ defined as the pushout of the inclusion $i_1 : \mathsf{J} \hookrightarrow \mathsf{J} \times \mathbbe{2}$ of $\mathsf{J}$ as the ``right end'' of the cylinder $\mathsf{J} \times \mathbbe{2}$ along the unique functor $\mathsf{J} \to \mathbbe{1}$.
$ \xymatrix{ \mathsf{J} \ar[d]_{i_1} \ar[r]^-{!} \ar@{}[dr]|(.8){\displaystyle\ulcorner} & \mathbbe{1} \ar[d] \\ \mathsf{J} \times \mathbbe{2} \ar[r] & \mathsf{J}^{\triangleright}}$ The effect of this pushout is to collapse the right end of the cylinder to a single object. The category $\mathsf{J}^\triangleright$ has one new object, a freely-adjoined terminal object $t$ that serves as the nadir of a new cone under the inclusion $\mathsf{J} \hookrightarrow \mathsf{J}^{\triangleright}$. There are no additional new objects or morphisms. A dual pushout along the other inclusion $i_0 : \mathsf{J} \hookrightarrow \mathsf{J} \times \mathbbe{2}$ defines a category $\mathsf{J}^\triangleleft$ with a freely-adjoined initial object. See Exercise \ref{exc:cone-cat-construction}.

SUGGESTION: cone under a small category