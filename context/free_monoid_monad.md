---
layout: page
title: free monoid monad
permalink: /context/free_monoid_monad.md
---
-  The **free monoid monad** is induced by the free $\dashv$ forgetful adjunction between monoids and sets of Example \ref{exs:free-forgetful}\eqref{itm:mon-free-forgetful}. The endofunctor $T : \textup{\textsf{Set}} \to \textup{\textsf{Set}}$ is defined by $ TA :eqq \mathrm{co}prod_{n\geq 0} A^n\rlap{{\,},}$ that is, $TA$ is the set of finite lists of elements in $A$; in computer science contexts, this monad is often called the **list monad**. The components of the unit $\eta_A : A \to TA$ are defined by the evident coproduct inclusions, sending each element of $A$ to the corresponding singleton list. The components of the multiplication $\mu_A : T^2A \to TA$ are the concatenation functions, sending a list of lists to the composite list. A categorical description of this map is given in Exercise \ref{exc:monoid-mult}, which demonstrates that the free monoid monad can also be defined in any monoidal category with coproducts that distribute over the monoidal product.

SUGGESTION: free monoid monad