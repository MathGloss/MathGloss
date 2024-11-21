---
layout: page
title: horizontal composition
permalink: /context/horizontal_composition.md
---
The composition operation defined in Lemma \ref{lem:vert-comp} is called **vertical composition**. Drawing the parallel functors horizontally, a composable pair of natural transformations in the category $\mathsf{D}^\mathsf{C}$ fits into a \emph{pasting diagram}
$ \xymatrix@C=30pt{ \mathsf{C} \ar@/^4ex/[r]^*{F}_*{\Downarrow\alpha} \ar[r]|*{G} \ar@/_4ex/[r]_*{H}^*{\Downarrow\beta} & \mathsf{D} \ar@{}[r]|{\displaystyle =} & \mathsf{C} \ar@/^4ex/[r]^*{F} \ar@/_4ex/[r]_*{H} \ar@{}[r]|*{\Downarrow\beta \cdot \alpha} & \mathsf{D}}$
As the terminology suggests, there is also a **horizontal composition** operation
$ \xymatrix@C=30pt{ \mathsf{C} \ar@/^4ex/[r]^*{F} \ar@/_4ex/[r]_*{G} \ar@{}[r]|*{\Downarrow \alpha} & \mathsf{D} \ar@/^4ex/[r]^*{H} \ar@/_4ex/[r]_*{K} \ar@{}[r]|*{\Downarrow\beta} & \mathsf{E}  \ar@{}[r]|{\displaystyle =} &  \mathsf{C} \ar@/^4ex/[r]^*{HF} \ar@/_4ex/[r]_*{KG} \ar@{}[r]|*{\Downarrow\beta \ast \alpha} & \mathsf{E}   }$
  defined by the following lemma.

SUGGESTION: horizontal composition