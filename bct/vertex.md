---
layout: page
title: vertex
permalink: /bct/vertex
---
Let $\mathscr{A}$ be a category, $\mathbf{I}$ a small category, and $D{\colon}\linebreak[0] \mathbf{I} \to \mathscr{A}$ a diagram in $\mathscr{A}$.    1. A **cone**    on $D$ is an object $A \in \mathscr{A}$ (the **vertex**    of the cone) together with a family   $$          \Bigl( A \stackrel{f_I}{\longrightarrow} D(I) \Bigr)_{I \in \mathbf{I}} $$   of maps in $\mathscr{A}$ such that for all maps $I \stackrel{u}{\longrightarrow} J$ in $\mathbf{I}$, the triangle $$ \xymatrix@R=1ex{                                 &D(I) \ar[dd]^{Du}      \\ A \ar[ru]^{f_I} \ar[rd]_{f_J}   &                       \\                                 &D(J) } $$ commutes.  (Here and later, we abbreviate $D(u)$ as $Du$.)\n2. A **limit**    of $D$ is a cone $\Bigl(L \stackrel{p_I}{\longrightarrow} D(I)\Bigr)_{I \in \mathbf{I}}$ with the property that for any cone~ on $D$, there exists a unique map $\bar{f}{\colon}\linebreak[0] A \to L$    such that $p_I \circ \bar{f} = f_I$ for all $I \in \mathbf{I}$.  The maps $p_I$ are called the **projections**    of the limit.


From [Basic Category Theory](https://mathgloss.github.io/MathGloss/bct.html)