---
layout: page
title: apex
permalink: /context/apex
---
A **cone over** a diagram $F \colon \mathsf{J} \to \mathsf{C}$ with **summit** or **apex** $c \in \mathsf{C}$ is a natural transformation $\lambda \colon c \Rightarrow F$ whose domain is the constant functor at $c$. The components $(\lambda_j \colon c \to Fj)_{j\in \mathsf{J}}$ of the natural transformation are called the **legs** of the cone. Explicitly:
1. The data of a cone over $F \colon \mathsf{J} \to \mathsf{C}$ with summit $c$ is a collection of morphisms $\lambda_j \colon c \to Fj$, indexed by the objects $j \in \mathsf{J}$.
2. A family of morphisms $(\lambda_j \colon c \to F_j)_{j \in \mathsf{J}}$ defines a cone over $F$ if and only if, for each  morphism $f \colon j \to k$ in $\mathsf{J}$, the following triangle commutes in $\mathsf{C}$:
$$\begin{gathered} \xymatrix@=10pt{ & c \ar[dl]_{\lambda_j} \ar[dr]^{\lambda_k} \\ Fj \ar[rr]_{Ff} & & Fk}\end{gathered}$$

Dually, a **cone under** $F$ with **nadir** $c$ is a natural transformation $\lambda \colon F \Rightarrow c$, whose **legs** are  the components $(\lambda_j \colon F_j \to c)_{j \in \mathsf{J}}$. The naturality condition asserts that, for each  morphism $f \colon j \to k$ of $\mathsf{J}$, the triangle
$$ \xymatrix@=10pt{ Fj \ar[dr]_{\lambda_j} \ar[rr]^{Ff} & & Fk\ar[dl]^{\lambda_k} \\ & c}$$ commutes in $\mathsf{C}$.
