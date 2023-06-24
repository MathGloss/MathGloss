Given a [[group]] $G$ and an [[group action|action]] of $G$ on two sets $X$ and $Y$, then the collection of maps between $X$ and $Y$ (denoted $\text{Maps}[X,Y]$) is naturally a [[group action|G-set]] in the following way:

Given a function $f\in \text{Maps}[X,Y]$, consider the [[graph of a function|graph]] $$\text{Graph}(f) = \{(x,f(x))\in X\times Y \mid x\in X\}.$$

Let $G$ [[group action|act]] diagonally on $X\times Y$: that is, define $g.(x,y) = (g.x,g.y)$. Then define $g^*f$ by $\text{Graph}()g^*f = g(\text{Graph}(f))$. 

Explicitly, for $gx' = x$, we have $$g^*f(x) = g(f(x')) \implies g^*f(x) = gf(g^{-1}x).$$ We can see the map as the [[function composition|composite]]

$$g^*f: X\overset{g^{-1}}{\to} X \overset{f}{\to} Y \overset{g}{\to} Y.$$