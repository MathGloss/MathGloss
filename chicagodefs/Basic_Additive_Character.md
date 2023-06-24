---
 layout: page
 title: Basic Additive Character
 permalink: /Basic_Additive_Character
---Let $x$ be a [unit](https://defsmath.github.io/DefsMath/unit_of_a_ring) of the [p-adic field](https://defsmath.github.io/DefsMath/p-adic_field) $\mathbb Q_p$. That is, let $x\in\mathbb Q_p^\times$. Then $x$ has a unique [p-adic expansion](https://defsmath.github.io/DefsMath/p-adic_expansion_is_unique) $$x= \sum_{n=\text{val}(x)}^\infty a_np^n.$$ Denote by $\lambda(x)$ the sum $$\lambda(x) = \sum_{n=\text{val}(x)}^{-1}a_np^n$$ and call it the **tail** of $x$. Then we define the **basic additive character** $\psi:\mathbb Q_p\to \mathbb T\subseteq \mathbb C^\times$ (the middle set being the [circle group](https://defsmath.github.io/DefsMath/circle_group)) by $$\psi(x) = e^{2\pi i \lambda(x)}.$$


 Auxiliary definition
We can also define a "scalar multiple" of the character by defining, for each $u\in\mathbb Q_p$, a new function $\psi_u:\mathbb Q_p\to \mathbb T$ by $x\mapsto \psi(ux)$.  
 Proof that it is a [character](https://defsmath.github.io/DefsMath/multiplicative_character)
First, we show that $\psi_u$ is a [group homomorphism](https://defsmath.github.io/DefsMath/group_homomorphism): $$\psi_u(x+y) = \psi(u(x+y)) = \psi(ux+uy) = \psi(ux)\psi(uy) = \psi_u(x)\psi_u(y)$$ from the fact that $\psi$ is itself a [group homomorphism](https://defsmath.github.io/DefsMath/group_homomorphism). 

Finally, $\psi_u$ is [continuous](https://defsmath.github.io/DefsMath/continuous) because the [composition of continuous functions is continuous](https://defsmath.github.io/DefsMath/composition_of_continuous_functions_is_continuous) and $\psi$ is the composition of $\psi$, which is itself [continuous](https://defsmath.github.io/DefsMath/continuous) by virtue of it being a [multiplicative character](https://defsmath.github.io/DefsMath/multiplicative_character), and because $\mathbb Q_p$ [is](https://defsmath.github.io/DefsMath/Qp_is_a_topological_field) a [topological field](https://defsmath.github.io/DefsMath/topological_field), the map given by "multiplication by $u$" is also [continuous](https://defsmath.github.io/DefsMath/continuous). 