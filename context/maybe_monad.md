---
layout: page
title: maybe monad
permalink: /context/maybe_monad
---
-  The free $\dashv$ forgetful adjunction between pointed sets and ordinary sets of Example \ref{exs:free-forgetful}\eqref{itm:pointed-free-forgetful} induces a monad on $\textup{\textsf{Set}}$ whose endofunctor $(-)_+ : \textup{\textsf{Set}} \to \textup{\textsf{Set}}$ adds a new disjoint point. The components of the unit are given by the obvious natural inclusions $\eta_A : A \to A_+$. The components of the multiplication $\mu_A : (A_+)_+ \to A_+$ are defined to be the identity on the subset $A$ and to send the two new points in $(A_+)_+$ to the new point in $A_+$. By Lemma \ref{lem:monad-from-adj}, or by a direct verification, the diagrams
$ \xymatrix{ ((A_+)_+)_+ \ar[r]^-{(\mu_A)_+} \ar[d]_{\mu_{A_+}} & (A_+)_+ \ar[d]^{\mu_A} & & A_+ \ar[r]^-{\eta_{A_+}} \ar[dr]_{1_{A_+}} & (A_+)_+ \ar[d]^{\mu_A} & A_+ \ar[l]_-{(\eta_A)_+} \ar[dl]^{1_{A_+}} \\ (A_+)_+ \ar[r]_-{\mu_A} & A_+ & & & A_+}$ commute. Particularly in computer science, this monad is called the **maybe monad**, for reasons that are explained in Example \ref{exs:kleisli}\eqref{itm:maybe}. There is a similar monad on $\textup{\textsf{Top}}$, or any category with coproducts, which acts by adjoining a copy of a fixed object (in this case a point).

SUGGESTION: maybe monad

From [Category Theory in Context](https://mathgloss.github.io/MathGloss/context.html)