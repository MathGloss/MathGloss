---
layout: page
title: adjunction
permalink: /context/adjunction
---
An **adjunction** consists of an opposing pair of functors $F \colon \mathsf{C} \rightleftarrows \mathsf{D} \colon G$, together with natural transformations $\eta \colon 1_\mathsf{C} \Rightarrow GF$ and $\epsilon \colon FG \Rightarrow 1_\mathsf{D}$ that satisfy the **triangle identities**:
$$ \xymatrix{ F \ar@{=>}[r]^-{F\eta} \ar@{=>}[dr]_{1_F} & FGF \ar@{=>}[d]^{\epsilon F}  & & G \ar@{=>}[r]^-{\eta G} \ar@{=>}[dr]_{1_G} & GFG \ar@{=>}[d]^{G\epsilon} \\ & F & & & G}$$
