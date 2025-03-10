---
layout: page
title: truncation
permalink: /context/truncation
---

Write $\DDelta_{\leq n}$ for the full subcategory spanned by the first $n+1$ ordinals $[0],\ldots, [n]$ in $\DDelta$. Restriction along the inclusion functor $i_n : \DDelta_{\leq n} \hookrightarrow \DDelta$ is called $n$-**truncation**. As $\textup{\textsf{Set}}$ is complete and cocomplete, Corollary \ref{cor:kan-exist} implies that $n$-truncation admits both left and right adjoints:
 $\xymatrix{\textup{\textsf{Set}}^{\DDelta^\mathrm{op}}  \ar[r]|{i_n^*} & \textup{\textsf{Set}}^{\DDelta_{\leq n}^\mathrm{op}} \ar@/^1.5pc/[l]^{\mathrm{Ran}_{i_n}} \ar@/_1.5pc/[l]_{\mathrm{Lan}_{i_n}} \ar@{}[l]^*+{\labelstyle{\perp}}_*+{\labelstyle\perp} }$ The composite comonad on $\textup{\textsf{Set}}^{\DDelta^\mathrm{op}}$ is sk$_n$, the functor that maps a simplicial set to its $n$-**skeleton**. The composite monad on $\textup{\textsf{Set}}^{\DDelta^\mathrm{op}}$ is cosk$_n$, the functor that maps a simplicial set to its $n$-**coskeleton**. Furthermore, sk$_n$ is left adjoint to cosk$_n$, as is the case for any comonad and monad arising in this way (see Exercise \ref{exc:adjoint-comonad-monad}).

SUGGESTION: n-truncation

From [Category Theory in Context](https://mathgloss.github.io/MathGloss/context.html)