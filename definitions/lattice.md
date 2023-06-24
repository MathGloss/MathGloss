---
aliases: absorption laws
---
A **lattice** is a [[partially ordered set]] in which every pair of elements has a unique [[infimum]] and a unique [[supremum]]. 

If $(X, \leq)$ is a lattice, we call the [[supremum]] of $x$ and $y$ the **join** of $x$ and $y$ and denote it $x\lor y$. Similarly, we call the [[infimum]] of $x$ and $y$ their **meet** and denote it $x\land y$. These are in fact [[binary operation|binary operations]] on $X$. Moreover, they respect the [[partially ordered set|partial order]] on $X$.  

We can also define a **lattice** as a triple $(L, \lor,\land)$ where $L$ is a set and $\lor$ and $\land$ are two [[commutative]], [[associative]] [[binary operation|binary operations]] on $L$ satisfying the following **absorption laws** for all $a,b \in L$:
1. $a\lor (a\land b) = a$;
2. $a\land (a\lor b) = a$. 

Immediately following these two laws we have that $a\land a = a$ and $a\lor a = a$. 

It is easy to check that the [[partially ordered set|poset]] notion of a lattice admits a description in the other form. To see the converse, define a [[partially ordered set|partial order]] $\leq$ on $L$ by setting $a\leq b$ if $a= a\land b$ or $a\leq b$ if $b = a\lor b$ for all $a,b\in L$. 