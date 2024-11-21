---
layout: page
title: tensor product bifunctor
permalink: /context/tensor_product_bifunctor.md
---

Consider the hom bifunctor
 $\textup{\textsf{Ab}}^\mathrm{op} \times \textup{\textsf{Ab}} \xrightarrow{{\mathrm{Hom}}} \textup{\textsf{Ab}}\rlap{{\,},}$ where $\mathrm{Hom}(A,B)$ is the group of homomorphisms $A \to B$ with addition defined pointwise in the abelian group $B$.\footnote{Recall from \S\ref{sec:cat} that this is why the collection of morphisms between a fixed pair of objects in a general category is often denoted ``$\mathrm{Hom}$.'' Here we use ``$\textup{\textsf{Ab}}$'' for the mere set of homomorphisms, which in this instance plays a secondary role.}   Fixing the contravariant variable, there is an adjunction
  \xymatrix{ \textup{\textsf{Ab}} \ar@<1ex>[r]^{A \otimes_\mathbb{Z} - } \ar@{}[r]|\perp & \textup{\textsf{Ab}} \ar@<1ex>[l]^{\mathrm{Hom}(A,-)}}
 \qquad\qquad \textup{\textsf{Ab}}(A \otimes_\mathbb{Z} B, C) \mathrm{co}ng \textup{\textsf{Ab}}(B, \mathrm{Hom}(A,C))  defining the tensor product.
Once the objects $A \otimes_\mathbb{Z} B \in \textup{\textsf{Ab}}$ have been defined, Proposition \ref{prop:one-sided-adj} uses the isomorphisms \eqref{eq:tensor-hom-iso} to extend this data into a functor $A \otimes_\mathbb{Z} - : \textup{\textsf{Ab}} \to \textup{\textsf{Ab}}$. Proposition \ref{prop:two-variable-adjunction}\eqref{itm:two-var-i} then extends this data into the **tensor product bifunctor** $ \textup{\textsf{Ab}} \times \textup{\textsf{Ab}} \xrightarrow{\otimes_\mathbb{Z}} \textup{\textsf{Ab}}$ in such a way that the tensor product and the hom define a two-variable adjunction.

SUGGESTION: tensor product bifunctor