---
layout: page
title: currying
permalink: /context/currying.md
---
 The product bifunctor
$\textup{\textsf{Set}} \times \textup{\textsf{Set}} \xrightarrow{\times} \textup{\textsf{Set}}$ is closed: the operation called **currying** in computer science defines a family of natural isomorphisms
$ \{ A \times B \xrightarrow{f} C \} \mathrm{co}ng \{ A \xrightarrow{f} C^B\} \mathrm{co}ng \{ B \xrightarrow{f} C^A\}\rlap{{\,}.}$ Thus, the product and exponential bifunctors $ \textup{\textsf{Set}} \times \textup{\textsf{Set}} \xrightarrow{\times} \textup{\textsf{Set}}, \quad \textup{\textsf{Set}}^\mathrm{op} \times \textup{\textsf{Set}} \xrightarrow{(-)^{(-)}}  \textup{\textsf{Set}}, \quad \textup{\textsf{Set}}^\mathrm{op} \times \textup{\textsf{Set}} \xrightarrow{(-)^{(-)}}  \textup{\textsf{Set}} $ define a two-variable adjunction.


SUGGESTION: currying