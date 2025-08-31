---
layout: page
title: commutative cube
permalink: /context/commutative_cube
---
This very simple result underlies most proofs by ``diagram chasing.'' When a diagram is depicted by a simple (meaning there is at most one edge between any two vertices) acyclic directed graph, the most common convention is to include commutativity relations that assert that any two paths in the diagram with a common source and target commute, i.e., that the directed graph represents a poset category. For example, the category $\mathbbe{2} \times \mathbbe{2} \times \mathbbe{2}$ indexes the **commutative cube**, which is typically depicted as follows:
$ \xymatrix@=10pt{ \bullet \ar[rr] \ar[dd] \ar[dr] & & \bullet \ar'[d][dd] \ar[dr] \\ & \bullet \ar[rr] \ar[dd] & & \bullet \ar[dd] \\ \bullet \ar[dr] \ar'[r][rr] & & \bullet \ar[dr] \\ & \bullet \ar[rr] & & \bullet}$ In such cases, Lemma \ref{lem:comp-relation} and transitivity of equality implies that commutativity of the entire diagram may be checked by establishing commutativity of each minimal subdiagram in the directed graph. Here, a minimal subdiagram corresponds to a composition relation $h_n \cdots h_1 = k_m \cdots k_1$ that cannot be factored into a relation between shorter paths of composable morphisms. The graph corresponding to a minimal relation is a ``directed polygon''
$ \xymatrix@=10pt{  & \bullet \ar[r]^{h_2} & \bullet \ar@{..}[r] & \bullet \ar[r]^{h_{n-1}} & \bullet \ar[dr]^{h_n} \\ \bullet \ar[ur]^{h_1} \ar[dr]_{k_1} & & & &  & \bullet \\ & \bullet \ar[r]_{k_2} & \bullet \ar@{..}[r] & \bullet \ar[r]_{k_{m-1}} &  \bullet \ar[ur]_{k_m}}$ with a commutative triangle, as in \eqref{eq:triangle}, being the simplest case. This sort of argument is called ``equational reasoning'' in \cite[2.1]{simmons-introduction}, which provides an excellent short introduction to diagram chasing.

SUGGESTION: commutative cube

From [Category Theory in Context](https://mathgloss.github.io/MathGloss/context.html)