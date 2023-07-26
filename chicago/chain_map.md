---
 layout: page
 title: chain map
 permalink: /chicago/chain_map
---
Let $f:X\to Y$ be a [continuous](https://mathgloss.github.io/MathGloss/continuous) function between [topological spaces](https://mathgloss.github.io/MathGloss/topological_space) $X$ and $Y$. Let $C_n(X)$ and $C_n(Y)$ be the [groups](https://mathgloss.github.io/MathGloss/group) of [n-chains](https://mathgloss.github.io/MathGloss/n-chain) in the [chain complex](https://mathgloss.github.io/MathGloss/chain_complex) of $X$ and $Y$, respectively. Then we may define a [homomorphism](https://mathgloss.github.io/MathGloss/group_homomorphism) called a **chain map** $f_\sharp:C_n(X)\to C_n(Y)$ by composing each [singular n-simplex](https://mathgloss.github.io/MathGloss/singular_n-simplex) $\sigma:\Delta^n\to X$ with $f$ to get a [singular n-simplex](https://mathgloss.github.io/MathGloss/singular_n-simplex) $f_\sharp(\sigma) = f\sigma:\Delta^n\to Y$ and extending $f_\sharp$ [linearly](https://mathgloss.github.io/MathGloss/linear_transformation) via $$f_\sharp\left(\sum_i n_i\sigma_i\right) = \sum_i n_if_\sharp(\sigma_i) = \sum_i n_if_\sharp\sigma_i.$$

Let $\partial$ be a general [boundary homomorphism](https://mathgloss.github.io/MathGloss/boundary_homomorphism) between $C_{k+1}(X)$ and $C_{k}(X)$ and do a similar thing for  $Y$. Then the maps $f_\sharp:C_n(X)\to C_n(Y)$ satisfy $f_\sharp \partial = \partial f_\sharp$ and the following diagram [commutes](https://mathgloss.github.io/MathGloss/commitative_diagram): 

![Screen Shot 2021-11-04 at 10.37.30 AM.png]