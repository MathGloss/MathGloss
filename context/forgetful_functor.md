---
layout: page
title: forgetful functor
permalink: /context/forgetful_functor
---
-  Each of the categories listed in Example \ref{exs:concrete-categories} has a **forgetful functor**, a general term that is used for any functor that forgets structure, whose codomain is the category of sets. For example, $U : \textup{\textsf{Group}} \to \textup{\textsf{Set}}$ sends a group to its underlying set and a group homomorphism to its underlying function. The functor $U : \textup{\textsf{Top}} \to \textup{\textsf{Set}}$ sends a space to its set of points. There are two natural forgetful functors $V,E : \textup{\textsf{Graph}} \rightrightarrows \textup{\textsf{Set}}$ that send a graph to its vertex or edge sets, respectively; if desired, these can be combined to define a single functor $V \sqcup E : \textup{\textsf{Graph}} \to \textup{\textsf{Set}}$ that carries a graph to the disjoint union of its vertex and edge sets. These mappings are functorial because in each instance a morphism in the domain category has an underlying function.

SUGGESTION: forgetful functor

From [Category Theory in Context](https://mathgloss.github.io/MathGloss/context.html)