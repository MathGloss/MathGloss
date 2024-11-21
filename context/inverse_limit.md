---
layout: page
title: inverse limit
permalink: /context/inverse_limit
---
 The limit of a diagram indexed by the category $\bbomega^\mathrm{op}$ is called an **inverse limit** of a tower or a sequence of morphisms. On account of this example, the term ``inverse limit'' is sometimes used to refer to limits of any shape. A diagram indexed by $\bbomega^\mathrm{op}$ consists of a sequence of objects and morphisms
$ \xymatrix{ \cdots \ar[r] & F_3 \ar[r] & F_2 \ar[r] & F_1 \ar[r] & F_0}$ together with composites and identities, which are not displayed. A cone over this diagram is an extension of this data to a diagram of shape $(\bbomega +1)^\mathrm{op}$. Explicitly, a cone consists of a new object ``all the way to the left'' together with morphisms making every triangle commute:
$ \xymatrix@=35pt{ c \ar[d]^\cdots \ar[dr]|{\mathrm{co}lorbox{white}{\makebox(9,5){\scriptsize$\lambda_{3}$}}} \ar[drr]|{\mathrm{co}lorbox{white}{\makebox(9,5){\scriptsize$\lambda_{ 2}$}}} \ar[drrr]|{\mathrm{co}lorbox{white}{\makebox(9,5){\scriptsize$\lambda_{ 1}$}}} \ar[drrrr]|{\mathrm{co}lorbox{white}{\makebox(8,4){\scriptsize$\lambda_{ 0}$}}} \\  \cdots \ar[r] & F_3 \ar[r] & F_2 \ar[r] & F_1 \ar[r] & F_0}$ The inverse limit,  frequently denoted by $\varprojlim F_n$, is the terminal cone. Similar remarks apply with any limit ordinal\footnote{Exercise \ref{exc:limit-initial-object} explains the limited interest of limits of diagrams indexed by opposites of successor ordinals.} $\bbalpha$ in place of $\bbomega$.


SUGGESTION: inverse limit

From [Category Theory in Context](https://mathgloss.github.io/MathGloss/context.html)