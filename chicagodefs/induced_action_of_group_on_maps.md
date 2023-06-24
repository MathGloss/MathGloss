---
 layout: page
 title: induced action of group on maps
 permalink: /induced_action_of_group_on_maps
---
Given a [group](https://defsmath.github.io/DefsMath/group) $G$ and an [action](https://defsmath.github.io/DefsMath/group_action) of $G$ on two sets $X$ and $Y$, then the collection of maps between $X$ and $Y$ (denoted $\text{Maps}[X,Y]$) is naturally a [G-set](https://defsmath.github.io/DefsMath/#############G-set) in the following way:

Given a function $f\in \text{Maps}[X,Y]$, consider the [graph](https://defsmath.github.io/DefsMath/graph_of_a_function) $$\text{Graph}(f) = \{(x,f(x))\in X\times Y \mid x\in X\}.$$

Let $G$ [act](https://defsmath.github.io/DefsMath/#############act) diagonally on $X\times Y$: that is, define $g.(x,y) = (g.x,g.y)$. Then define $g^*f$ by $\text{Graph}()g^*f = g(\text{Graph}(f))$. 

Explicitly, for $gx' = x$, we have $$g^*f(x) = g(f(x')) \implies g^*f(x) = gf(g^{-1}x).$$ We can see the map as the [composite](https://defsmath.github.io/DefsMath/function_composition)

$$g^*f: X\overset{g^{-1}}{\to} X \overset{f}{\to} Y \overset{g}{\to} Y.$$