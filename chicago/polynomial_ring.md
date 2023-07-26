---
 layout: page
 title: polynomial ring
 permalink: /chicago/polynomial_ring
---


Let $R$ be a [commutative](https://mathgloss.github.io/MathGloss/chicago/commutative) [ring](https://mathgloss.github.io/MathGloss/chicago/ring) and $x$ a variable. Then $R[x]$ is the **polynomial ring** of [polynomials](https://mathgloss.github.io/MathGloss/chicago/polynomial) in $x$ with coefficients in $R$.

We can also define the **polynomial ring** in multiple variables. Let $X = \{x_1,\dots,x_n\}$ be a finite collection of variables. Then $R[X] = R[x_1,\dots,x_n]$ is defined as follows:

To each function $I:X\to \mathbb N$, associate a monomial $$x^I = x_1^{I(x_1)}+\cdots + x_n^{I(x_n)}.$$ Then $$R[X]= \left\{ \sum_{I:X\to \mathbb N} a_IX^I \mid a_I\in R, a_I = 0 \text{ for all but finitely many } I \right\}.$$ Multiplication and addition are defined exactly how you would think. 

Wikidata ID: [Q1455652](https://www.wikidata.org/wiki/Q1455652)