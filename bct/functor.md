---
layout: page
title: functor
permalink: /bct/functor
---
Let $\mathscr{A}$ and $\mathscr{B}$ be categories.  A **functor**    $F{\colon}\linebreak[0] \mathscr{A} \to \mathscr{B}$ consists of:   1. a function $$ \ob(\mathscr{A}) \to \ob(\mathscr{B}), $$ written as $A \mapsto F(A)$;\n2. for each $A, A' \in \mathscr{A}$, a function $$ \mathscr{A}(A, A') \to \mathscr{B}(F(A), F(A')), $$ written as $f \mapsto F(f)$,   satisfying the following axioms:   1. $F(f' \circ f) = F(f') \circ F(f)$ whenever $A \stackrel{f}{\longrightarrow} A' \stackrel{f'}{\longrightarrow} A''$ in $\mathscr{A}$;\n2. $F(1_A) = 1_{F(A)}$ whenever $A \in \mathscr{A}$.


From [Basic Category Theory](https://mathgloss.github.io/MathGloss/bct.html)