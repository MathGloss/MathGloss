---
layout: page
title: cocones
permalink: /context/cocones
---
Cones under a diagram are also called **cocones**---a cone under $F : \mathsf{J} \to \mathsf{C}$ is precisely a cone over $F : \mathsf{J}^\mathrm{op} \to \mathsf{C}^\mathrm{op}$---but we find the terminology  ``under'' and ``over'' to be more evocative.  To illustrate, if $F$ is a diagram indexed by the poset category $(\mathbb{Z},\leq)$, then a cone over $F$ with summit $c$ is comprised of a family of morphisms $(\lambda_n : c \to Fn)_{n \in \mathbb{Z}}$ so that, for each $n \leq m$, the triangle  defined by the morphisms  $\lambda_n$, $\lambda_m$, and $Fn \to Fm$ commutes:
\xymatrix@R=35pt{
&&& c
 \ar[d]|(0.44){\mathrm{co}lorbox{white}{\makebox(10,6){\scriptsize$\lambda_{ 0}$}}}
\ar[dl]|(0.45){\mathrm{co}lorbox{white}{\makebox(10,5){\scriptsize$\lambda_{-1}$}}}
\ar[dr]|(0.44){\mathrm{co}lorbox{white}{\makebox(10,5){\scriptsize$\lambda_{1}$}}}
\ar[dll]|(0.45){\mathrm{co}lorbox{white}{\makebox(12,5){\scriptsize$\lambda_{-2}$}}}
\ar[drr]|(0.44){\mathrm{co}lorbox{white}{\makebox(12,5){\scriptsize$\lambda_{2}$}}}
\ar[drrr]_\cdots
\ar[dlll]^{\cdots}
&&& \\
\cdots \ar[r] & F(-2) \ar[r] & F(-1) \ar[r] & F0 \ar[r] & F1 \ar[r] & F2 \ar[r] & \cdots
}
A cone under $F$ with nadir $c$ is  comprised of a family of morphisms $(\lambda_n : Fn \to c)_{n \in \mathbb{Z}}$ so that, for each $n \leq m$, the triangle defined by the morphisms $\lambda_n$, $\lambda_m$, and $F_n \to F_m$ commutes:
$ \xymatrix@R=35pt{ \cdots \ar[r]  \ar[drrr]^\cdots & F(-2) \ar[r]  \ar[drr]|(0.45){\mathrm{co}lorbox{white}{\makebox(12,5){\scriptsize$\lambda_{-2}$}}}& F(-1) \ar[dr]|(.45){\mathrm{co}lorbox{white}{\makebox(10,5){\scriptsize$\lambda_{-1}$}}}  \ar[r] & F0 \ar[d]|(.44){\mathrm{co}lorbox{white}{\makebox(10,6){\scriptsize$\lambda_{ 0}$}}}   \ar[r] & F1  \ar[dl]|(.44){\mathrm{co}lorbox{white}{\makebox(10,5){\scriptsize$\lambda_{1}$}}} \ar[r] & F2  \ar[dll]|(.44){\mathrm{co}lorbox{white}{\makebox(12,5){\scriptsize$\lambda_{2}$}}}   \ar[r] & \cdots  \ar[dlll]_\cdots \\ & & &c & & &   }$

SUGGESTION: cone