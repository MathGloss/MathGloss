---
layout: page
title: group extension
permalink: /context/group_extension.md
---
A **group extension** of an abelian group $H$ by an abelian group $G$ consists of a group $E$ together with an inclusion of $G \hookrightarrow E$ as a normal subgroup and a surjective homomorphism $E \twoheadrightarrow H$ that displays $H$ as the quotient group $E/G$. This data is typically displayed in a diagram of group homomorphisms:
$ 0 \to G \to E \to H \to 0.\footnote{The zeros appearing on the ends provide no additional data. Instead, the first zero implicitly asserts that the map $G \to E$ is an inclusion and the second that the map $E \to H$ is a surjection. More precisely, the displayed sequence of group homomorphisms is **exact**, meaning that the kernel of each homomorphism equals the image of the preceding homomorphism.}$
A pair of group extensions $E$ and $E'$ of $G$ and $H$ are considered to be equivalent whenever there is an isomorphism $E \mathrm{co}ng E'$ that \emph{commutes with} the inclusions of $G$ and quotient maps to $H$, in a sense that is made precise in \S\ref{sec:diagram-chase}. The set of equivalence classes of \emph{abelian} group extensions $E$ of $H$ by $G$ defines an abelian group $\mathrm{Ext}(H,G)$.

SUGGESTION: group extension