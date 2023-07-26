---
 layout: page
 title: induced action of group on maps
 permalink: /chicago/induced_action_of_group_on_maps
---
Given a [group](https://mathgloss.github.io/MathGloss/group) $G$ and an [action](https://mathgloss.github.io/MathGloss/group_action) of $G$ on two sets $X$ and $Y$, then the collection of maps between $X$ and $Y$ (denoted $\text{Maps}[X,Y]$) is naturally a [G-set](https://mathgloss.github.io/MathGloss/#############G-set) in the following way:

Given a function $f\in \text{Maps}[X,Y]$, consider the [graph](https://mathgloss.github.io/MathGloss/graph_of_a_function) $$\text{Graph}(f) = \{(x,f(x))\in X\times Y \mid x\in X\}.$$

Let $G$ [act](https://mathgloss.github.io/MathGloss/#############act) diagonally on $X\times Y$: that is, define $g.(x,y) = (g.x,g.y)$. Then define $g^*f$ by $\text{Graph}()g^*f = g(\text{Graph}(f))$. 

Explicitly, for $gx' = x$, we have $$g^*f(x) = g(f(x')) \implies g^*f(x) = gf(g^{-1}x).$$ We can see the map as the [composite](https://mathgloss.github.io/MathGloss/function_composition)

$$g^*f: X\overset{g^{-1}}{\to} X \overset{f}{\to} Y \overset{g}{\to} Y.$$