---
layout: page
title: dependent product
permalink: /context/dependent_product.md
---
 When $\mathsf{C}$ is a discrete category, a functor $F : \mathsf{C} \to \textup{\textsf{Set}}$ encodes an indexed family of sets $(F_c)_{c \in \mathsf{C}}$. The category of elements of $F$ is again a discrete category whose set of objects is $\mathrm{co}prod_{c \in \mathsf{C}} F_c$. The canonical projection $\Pi : \mathrm{co}prod_{c \in \mathsf{C}} F_c \to \mathsf{C}$ is defined so that the fiber over $c \in \mathsf{C}$ is the set $F_c$. The set $\mathrm{co}prod_{c \in \mathsf{C}} F_c$ is called the **dependent sum** of the indexed family of sets $(F_c)_{c \in \mathsf{C}}$. The related **dependent product** $\prod_{c \in \mathsf{C}} F_c$ is the set of sections of the functor $\Pi : \mathrm{co}prod_{c \in \mathsf{C}} F_c \to \mathsf{C}$.


SUGGESTION: dependent product