---
 layout: page
 title: sign of permutation
 permalink: /chicago/sign_of_permutation
---
For $\sigma$ a [permutation](https://mathgloss.github.io/MathGloss/chicago/symmetric_group) in $S_n$, the **sign** of $\sigma$ denoted $\text{sgn}(\sigma)$ is the [determinant](https://mathgloss.github.io/MathGloss/chicago/determinant) of the [linear transformation](https://mathgloss.github.io/MathGloss/chicago/linear_transformation) $P_\sigma:\mathbb R^n\to\mathbb R^n$ given by $$P_\sigma(x_1,\dots,x_n) =(x_{\sigma(1)},\dots, x_{\sigma(n)}).$$

Equivalently, let $\{x_i\}_{i=1}^n$ be $n$ distinct variables and let $\Delta$ be the [polynomial](https://mathgloss.github.io/MathGloss/chicago/polynomial) $$\Delta = \prod_{1\leq i\leq j \leq n}(x_i-x_j).$$ For each $\sigma\in S_n$, let $\sigma$ act on $\Delta$ by permuting the variables as their indices. That is, $$\sigma(\Delta)=\prod_{1\leq i\leq j\leq n} (x_{\sigma(i)}- x_{\sigma(j)}).$$ Note that in general, $\Delta$ contains one factor of $(x_i-x_j)$ for all $i < j$. Because $\sigma$ is a [bijection](https://mathgloss.github.io/MathGloss/chicago/bijective) on the indices, $\sigma(\Delta)$ contains either a factor of $(x_i-x_j)$ or a factor of $(x_j-x_i)$ but not both. If the latter, we may write it as $(-1)(x_i-x_j))$. Collect the $-1$ factors in the product and define $$\epsilon(\sigma) = \begin{cases}1 & \sigma(\Delta) = \Delta \\ -1 & \sigma(\Delta) = -\Delta.\end{cases}$$ The function $\epsilon$ gives the **sign** of $\sigma$.

Wikidata ID: [Q1064405](https://www.wikidata.org/wiki/Q1064405)