Let $(X,\Sigma, \mu)$ be a [[measure space]]. Let $f = \sum\limits_{k=1}^n a_k \chi_{A_k}$ be a [[simple function]] such that $\mu(A_k) < \infty$ for $a_k \neq 0$.  The **Lebesgue integral of the [[simple function]]** $f$ is defined as $$\int\left(\sum_{k=1}^n a_k\chi_{A_k}\right)d\mu = \sum_{k=1}^n a_k \int\chi_{A_k}d\mu = \sum_{k=1}^n a_k\mu(A_k),$$ consistent with the [[Lebesgue integral of characteristic function|Lebesgue integral of characteristic functions]].

If $B$ is a [[measurable]] subset of $X$ and $g = \sum\limits_{k=1}^n b_k\chi_{B_k}$ is a [[measurable function|measurable]] [[simple function]] on $B$, define $$\int_B gd\mu = \int\chi_Bgd\mu = \sum_{k=1}^nb_k\mu(B_k\cap B).$$

