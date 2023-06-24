---
aliases: integral
---
To define the **Lebesgue integral** for a general real-valued function, we must first define it for nonnegative functions.

Let $(X,\Sigma,\mu)$ be a [[measure space]] and let $f$ be a nonnegative, [[measurable function|measurable]], extended-real-valued function on $X$ (that is, $f(x) \geq 0$ for all $x \in X$, and it may be the case that $f(x) = +\infty$). Define $$\int_X fd\mu = \sup\left\{\int_X sd\mu \mid 0\leq s\leq f, s \text{ simple}\right\}$$ where the [[supremum]] is taken over the [[Lebesgue integral of a simple function|Lebesgue integrals]] of nonnegative [[simple function|simple functions]] $s$ less than $f$.

Now let $f$ be a [[measurable function|measurable]] extended-real-valued function on $X$. Then $f$ may be written as $f = f^+ - f^-$ where $$f^+(x) =\begin{cases}f(x) & f(x)>0 \\0 &\text{otherwise} \end{cases} \quad\text{and}\quad f^-(x) = \begin{cases}-f(x) & f(x)<0 \\ 0 &\text{otherwise} \end{cases}$$ so that $f^+$ and $f^-$ are both nonnegative and [[measurable function|measurable]]. Note that $|f| = f^+ + f^-$. The Lebesgue integral of the [[measurable function]] $f$ **exists** if at least one of $\int f^+d\mu$ and $\int f^- d\mu$ is finite. In this case, define $$\int f d\mu = \int f^+d\mu - \int f^-d\mu.$$ If $\int|f|d\mu < \infty$, then $f$ is **Lebesgue integrable**.