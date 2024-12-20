---
layout: page
title: pullback
permalink: /bct/pullback
---
Let $\mathscr{A}$ be a category, and take objects and maps   $$          \begin{array}{c} \xymatrix{                 &Y \ar[d]^t     \\ X \ar[r]_s      &Z } \end{array} $$   in $\mathscr{A}$.  A **pullback**    of this diagram is an object $P \in \mathscr{A}$ together with maps $p_1{\colon}\linebreak[0] P \to X$ and $p_2{\colon}\linebreak[0] P \to Y$ such that   $$          \begin{array}{c} \xymatrix{ P \ar[r]^{p_2} \ar[d]_{p_1}     & Y \ar[d]^t      \\ X \ar[r]_s      & Z } \end{array} $$   commutes, and with the property that for any commutative square   $$          \begin{array}{c} \xymatrix{ A \ar[r]^{f_2} \ar[d]_{f_1}     & Y \ar[d]^t      \\ X \ar[r]_s      & Z } \end{array} $$   in $\mathscr{A}$, there is a unique map $\bar{f}{\colon}\linebreak[0] A \to P$ such that   $$          \begin{array}{c} \xymatrix{ A \ar@/^/[rrd]^{f_2} \ar@{.>}[rd]|{\bar{f}} \ar@/_/[rdd]_{f_1}&                &       \\         & P \ar[r]^{p_2} \ar[d]_{p_1}     & Y \ar[d]^t      \\         & X \ar[r]_s      &Z } \end{array} $$   commutes.  (For~ to commute means only that $p_1 \bar{f} = f_1$ and $p_2 \bar{f} = f_2$, since the commutativity of the square is already given.)


From [Basic Category Theory](https://mathgloss.github.io/MathGloss/bct.html)