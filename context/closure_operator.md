---
layout: page
title: closure operator
permalink: /context/closure_operator.md
---
 A topological space may be defined to be a set $X$ equipped with a **closure operator** $\overline{(-)} : PX \to PX$ on its set of subsets satisfying four axioms for all $A,B \in PX$:
$ (\mathrm{i})\ \overline{\emptyset} = \emptyset, \qquad (\mathrm{ii})\ A \subset\overline{A}, \qquad (\mathrm{iii})\
\overline{\overline{A}} = \overline{A}, \qquad (\mathrm{iv})\  \overline{A \cup B} = \overline{A} \cup \overline{B}\rlap{,}}$
A function $f : X \to Y$ between topological spaces is **continuous** if and only if $f(\overline{A}) \subset \overline{f(A)}$ for all $A \subset X$ and **closed**\footnote{A continuous function is **closed** if it preserves closed subsets.} if and only if $f(\overline{A}) = \overline{f(A)}$. All continuous functions between compact Hausdorff spaces are closed; that is, a function $f : X \to Y$ between compact Hausdorff spaces lifts to a map in $\textup{\textsf{cHaus}}$ if and only if it preserves the closure operator.

SUGGESTION: closure operator