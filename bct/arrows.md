---
layout: page
title: arrows
permalink: /bct/arrows
---
A **category**    $\mathscr{A}$ consists of:   1. a collection $\ob(\mathscr{A})$    of **objects**;\n2. for each $A, B \in \ob(\mathscr{A})$, a collection $\mathscr{A}(A, B)$    of **maps**    or **arrows**    or **morphisms**     from $A$ to $B$;\n3. for each $A, B, C \in \ob(\mathscr{A})$, a function $$ \begin{array}{ccc} \mathscr{A}(B, C) \times \mathscr{A}(A, B) & \to	& \mathscr{A}(A, C)	\\ (g, f)	& \mapsto	& g \circ f,    \end{array} $$ called **composition**;\n4. for each $A \in \ob(\mathscr{A})$, an element $1_A$    of $\mathscr{A}(A, A)$, called the **identity**    on $A$,   satisfying the following axioms:   1. **associativity**:    for each $f \in \mathscr{A}(A, B)$, $g \in \mathscr{A}(B, C)$ and $h \in \mathscr{A}(C, D)$, we have $(h \circ g) \circ f = h \circ (g \circ f)$;\n2. **identity    laws**: for each $f \in \mathscr{A}(A, B)$, we have $f \circ 1_A = f = 1_B \circ f$.
