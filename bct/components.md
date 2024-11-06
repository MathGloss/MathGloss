---
layout: page
title: components
permalink: /bct/components
---
Let $\mathscr{A}$ and $\mathscr{B}$ be categories and let $\parpairi{\mathscr{A}}{\mathscr{B}}{F}{G}$ be functors.  A **natural    transformation** $\alpha{\colon}\linebreak[0] F \to G$ is a family $\Bigl( F(A) \stackrel{\alpha_A}{\longrightarrow} G(A) \Bigr)_{A \in \mathscr{A}}$    of maps in $\mathscr{B}$ such that for every map $A \stackrel{f}{\longrightarrow} A'$ in $\mathscr{A}$, the square   $$          \begin{array}{c} \xymatrix{ F(A) \ar[r]^{F(f)} \ar[d]_{\alpha_A}    & F(A') \ar[d]^{\alpha_{A'}}      \\ G(A) \ar[r]_{G(f)}      & G(A') }  \end{array} $$   commutes.  The maps $\alpha_A$ are called the **components**    of $\alpha$.
