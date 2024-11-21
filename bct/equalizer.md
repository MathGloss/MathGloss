---
layout: page
title: equalizer
permalink: /bct/equalizer
---
Let $\mathscr{A}$ be a category and let $\parpairi{X}{Y}{s}{t}$ be objects and maps in $\mathscr{A}$.  An **equalizer**    of $s$ and $t$ is an object $E$ together with a map $E \stackrel{i}{\longrightarrow} X$ such that $$ \xymatrix{ E \ar[r]^i   & X \ar@<.5ex>[r]^s \ar@<-.5ex>[r]_t    & Y } $$ is a fork, and with the property that for any fork~, there exists a unique map $\bar{f}{\colon}\linebreak[0] A \to E$ such that   $$          \begin{array}{c} \xymatrix{ A \ar@{.>}[d]_{\bar{f}} \ar[rd]^f    &       \\ E \ar[r]_i                      &X } \end{array} $$   commutes.


From [Basic Category Theory](https://mathgloss.github.io/MathGloss/bct.html)