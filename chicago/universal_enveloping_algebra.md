---
 layout: page
 title: universal enveloping algebra
 permalink: /chicago/universal_enveloping_algebra
---
Let $\mathfrak g$ be a [Lie algebra](https://defsmath.github.io/DefsMath/quotient_of_Lie_algebra_by_ideal) over the [field](https://defsmath.github.io/DefsMath/Lie_algebra) $F$ with a [basis](https://defsmath.github.io/DefsMath/field) $\{x_i\}$ and a Lie bracket given by $$[x_i,x_j] = \sum_k = c_{ij}^kx_k.$$ The **universal enveloping algebra** $\mathcal U(\mathfrak g)$ is the [associative algebra](https://defsmath.github.io/DefsMath/basis) [generated](https://defsmath.github.io/DefsMath/associative_algebra) by the $x_i$ with the relations $$x_ix_j-x_jx_i = \sum_k c_{ij}^k x_k.$$ The $c_{ij}^k$ are the [structure constants](https://defsmath.github.io/DefsMath/generate_an_associative_algebra) of $\mathcal U(\mathfrak g)$.

The [universal property](https://defsmath.github.io/DefsMath/structure_constants) for the universal enveloping algebra is as follows: Let $\mathfrak g$ be a [Lie algebra](https://defsmath.github.io/DefsMath/universal_property) over the [field](https://defsmath.github.io/DefsMath/Lie_algebra) $F$ and let $A$ be an [associative algebra](https://defsmath.github.io/DefsMath/field) over $F$. By endowing $A$ with the [commutator](https://defsmath.github.io/DefsMath/associative_algebra) as a Lie bracket, $A$ becomes a [Lie algebra](https://defsmath.github.io/DefsMath/commutator). Let $\phi: \mathfrak g \to A$ be a [Lie algebra homomorphism](https://defsmath.github.io/DefsMath/Lie_algebra). Then the **universal enveloping algebra** $\mathcal U(\mathfrak g)$ is the algebra such that the following [diagram commutes](https://defsmath.github.io/DefsMath/Lie_algebra_homomorphism):

![Screen Shot 2021-07-26 at 11.31.16 AM.png](https://defsmath.github.io/DefsMath/commutative_diagram)

In a [basis](https://defsmath.github.io/DefsMath/basis)-free setting, let $\mathfrak g$ be a [Lie algebra](https://defsmath.github.io/DefsMath/Lie_algebra) over the [field](https://defsmath.github.io/DefsMath/field) $F$ and let $T\mathfrak g$ be the [tensor algebra](https://defsmath.github.io/DefsMath/tensor_algebra) of $\mathfrak g$. Consider the [ideal](https://defsmath.github.io/DefsMath/ideal) $$\mathcal I = \langle x\otimes y - y\otimes x - [x,y] \mid x,y \in \mathfrak g\rangle$$ of $T\mathfrak g$. Then the **universal enveloping algebra** $\mathcal U(\mathfrak g)$ is defined as the [quotient](https://defsmath.github.io/DefsMath/quotient_of_Lie_algebra_by_ideal) $T\mathfrak g/\mathcal I$.

Wikidata ID: [Q1673406](https://www.wikidata.org/wiki/Q1673406)