---
layout: page
title: category
permalink: /context/category
---
A **category** consists of
1. a collection of **objects** $X, Y, Z, \ldots$
2. a collection of **morphisms** $f, g, h, \ldots $
so that:
1. Each morphism has specified **domain** and **codomain**  objects; the notation $f \colon X \to Y$ signifies that $f$ is a morphism with domain $X$ and codomain $Y$.
2. Each object has a designated **identity morphism** $1_X \colon X \to X$.
3. For any pair of morphisms $f,g$ with the codomain of $f$ equal to the domain of $g$, there exists a specified **composite morphism** $gf$ whose domain is equal to the domain of $f$ and whose codomain is equal to the codomain of $g$, i.e.,:
$$ f \colon X \to Y,\quad g \colon Y \to Z \qquad \rightsquigarrow\qquad gf \colon X \to Z.$$
This data is subject to the following two axioms:
1. For any $f \colon X \to Y$, the composites $1_Y f$ and $f 1_X$ are both equal to $f$.
2. For any composable triple of morphisms $f,g,h$, the composites $h(gf)$ and $(hg)f$ are equal and henceforth denoted by $hgf$.
$$ f \colon X \to Y,\quad g \colon Y \to Z,\quad h \colon Z \to W \qquad \rightsquigarrow\qquad hgf \colon X \to W.$$
That is,  the composition law is associative and unital with the identity morphisms serving as two-sided identities.
