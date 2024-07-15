---
 layout: page
 title: lattice
 permalink: /chicago/lattice
---

A **lattice** is a [partially ordered set](https://mathgloss.github.io/MathGloss/chicago/partially_ordered_set) in which every pair of elements has a unique [infimum](https://mathgloss.github.io/MathGloss/chicago/infimum) and a unique [supremum](https://mathgloss.github.io/MathGloss/chicago/supremum). 

If $(X, \leq)$ is a lattice, we call the [supremum](https://mathgloss.github.io/MathGloss/chicago/supremum) of $x$ and $y$ the **join** of $x$ and $y$ and denote it $x\lor y$. Similarly, we call the [infimum](https://mathgloss.github.io/MathGloss/chicago/infimum) of $x$ and $y$ their **meet** and denote it $x\land y$. These are in fact [binary operations](https://mathgloss.github.io/MathGloss/chicago/binary_operation) on $X$. Moreover, they respect the [partial order](https://mathgloss.github.io/MathGloss/chicago/partially_ordered_set) on $X$.  

We can also define a **lattice** as a triple $(L, \lor,\land)$ where $L$ is a set and $\lor$ and $\land$ are two [commutative](https://mathgloss.github.io/MathGloss/chicago/commutative), [associative](https://mathgloss.github.io/MathGloss/chicago/associative) [binary operations](https://mathgloss.github.io/MathGloss/chicago/binary_operation) on $L$ satisfying the following **absorption laws** for all $a,b \in L$:
1. $a\lor (a\land b) = a$;
2. $a\land (a\lor b) = a$. 