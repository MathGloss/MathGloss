---
 layout: page
 title: circular mean value
 permalink: /chicago/circular_mean_value
---
Let $D\subset\mathbb R^2$ be [connected](https://defsmath.github.io/DefsMath/connected) and [open](https://defsmath.github.io/DefsMath/open) and let $f:D\to \mathbb R$ be [continuous](https://defsmath.github.io/DefsMath/continuous). Then let $z\in\mathbb R^2$. If for some $\varepsilon > 0$, the [closure](https://defsmath.github.io/DefsMath/closure) $\overline{B(z,\varepsilon)}$ of the ball of radius $\varepsilon$ centered at $z$ is contained within $D$ (i.e. $\overline{B(z,\varepsilon)}\subset D$), then the **circular mean value** $MV(f,z,\varepsilon)$ is the average value of $f$ on the [boundary](https://defsmath.github.io/DefsMath/boundary) $\partial B(z,\varepsilon)$. This is given by $$MV(f,z,\varepsilon) =\frac{1}{2\pi \varepsilon} \int_{\{w\in\mathbb R^2 \mid |w-z|=\varepsilon\}} f(w) |\text dw|$$ where the [integral](https://defsmath.github.io/DefsMath/Riemann_integrable) is taken with respect to [arc length](https://defsmath.github.io/DefsMath/arc_length). Moreover, $$MV(f,z\varepsilon) = \frac{1}{2\pi}\int_0^{2\pi} f(z+\varepsilon e^{i\theta})\text d\theta$$ where $\theta$ is the angle of the [polar coordinate](https://defsmath.github.io/DefsMath/polar_coordinates) for $z$. 

