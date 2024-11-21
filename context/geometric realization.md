 Apply the construction of Remark \ref{rmk:lan-adjunction} to the functor $\Delta : \DDelta \to \textup{\textsf{Top}}$ that sends the ordinal $[n]= 0 \to 1 \to \cdots \to n$ to the topological $n$-simplex
$ \Delta^n :eqq \left\{ (x_0,\ldots, x_n) \in \mathbb{R}^{n+1} \Biggm| \sum_i x_i = 1, x_i \geq 0\right\}\rlap{{\,}.}$
The left adjoint, defined by left Kan extension, forms the **geometric realization** of a simplicial set. The right adjoint is the **total singular complex functor**, which is used to define singular homology:
$ \xymatrix{ \textup{\textsf{Top}} \ar@<-1ex>[r]_-{\textup{Sing}} \ar@{}[r]|-\perp & \textup{\textsf{Set}}^{\DDelta^\mathrm{op}}\rlap{{\,}.}\ar@<-1ex>[l]_-{|-|}}$


SUGGESTION: geometric realization of a simplicial set