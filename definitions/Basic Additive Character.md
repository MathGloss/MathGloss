Let $x$ be a [[unit of a ring|unit]] of the [[p-adic field]] $\mathbb Q_p$. That is, let $x\in\mathbb Q_p^\times$. Then $x$ has a unique [[p-adic expansion is unique|p-adic expansion]] $$x= \sum_{n=\text{val}(x)}^\infty a_np^n.$$ Denote by $\lambda(x)$ the sum $$\lambda(x) = \sum_{n=\text{val}(x)}^{-1}a_np^n$$ and call it the **tail** of $x$. Then we define the **basic additive character** $\psi:\mathbb Q_p\to \mathbb T\subseteq \mathbb C^\times$ (the middle set being the [[circle group]]) by $$\psi(x) = e^{2\pi i \lambda(x)}.$$


## Auxiliary definition
We can also define a "scalar multiple" of the character by defining, for each $u\in\mathbb Q_p$, a new function $\psi_u:\mathbb Q_p\to \mathbb T$ by $x\mapsto \psi(ux)$.  
## Proof that it is a [[multiplicative character|character]]
First, we show that $\psi_u$ is a [[group homomorphism]]: $$\psi_u(x+y) = \psi(u(x+y)) = \psi(ux+uy) = \psi(ux)\psi(uy) = \psi_u(x)\psi_u(y)$$ from the fact that $\psi$ is itself a [[group homomorphism]]. 

Finally, $\psi_u$ is [[continuous]] because the [[composition of continuous functions is continuous]] and $\psi$ is the composition of $\psi$, which is itself [[continuous]] by virtue of it being a [[multiplicative character]], and because $\mathbb Q_p$ [[Qp is a topological field|is]] a [[topological field]], the map given by "multiplication by $u$" is also [[continuous]]. 