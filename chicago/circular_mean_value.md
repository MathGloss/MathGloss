---
 layout: page
 title: circular mean value
 permalink: /chicago/circular_mean_value
---
Let $D\subset\mathbb R^2$ be [connected](https://mathgloss.github.io/MathGloss/chicago/connected) and [open](https://mathgloss.github.io/MathGloss/chicago/open) and let $f:D\to \mathbb R$ be [continuous](https://mathgloss.github.io/MathGloss/chicago/continuous). Then let $z\in\mathbb R^2$. If for some $\varepsilon > 0$, the [closure](https://mathgloss.github.io/MathGloss/chicago/closure) $\overline{B(z,\varepsilon)}$ of the ball of radius $\varepsilon$ centered at $z$ is contained within $D$ (i.e. $\overline{B(z,\varepsilon)}\subset D$), then the **circular mean value** $MV(f,z,\varepsilon)$ is the average value of $f$ on the [boundary](https://mathgloss.github.io/MathGloss/chicago/boundary) $\partial B(z,\varepsilon)$. This is given by $$MV(f,z,\varepsilon) =\frac{1}{2\pi \varepsilon} \int_{\{w\in\mathbb R^2 \mid {\vert}w-z{\vert}=\varepsilon\}} f(w) {\vert}\text dw{\vert}$$ where the [integral](https://mathgloss.github.io/MathGloss/chicago/Riemann_integrable) is taken with respect to [arc length](https://mathgloss.github.io/MathGloss/chicago/arc_length). Moreover, $$MV(f,z\varepsilon) = \frac{1}{2\pi}\int_0^{2\pi} f(z+\varepsilon e^{i\theta})\text d\theta$$ where $\theta$ is the angle of the [polar coordinate](https://mathgloss.github.io/MathGloss/chicago/polar_coordinates) for $z$. 

