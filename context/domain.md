---
layout: page
title: domain
permalink: /context/domain
---
 A **category** consists of

-  a collection of **objects** $X, Y, Z, \ldots$
-  a collection of }}**morphisms** $f, g, h, \ldots $

so that:

-  Each morphism has specified **domain** and **codomain**  objects; the notation $f : X \to Y$ signifies that $f$ is a morphism with domain $X$ and codomain $Y$.
-  Each object has a designated **identity morphism** $1_X : X \to X$.
-  For any pair of morphisms $f,g$ with the codomain of $f$ equal to the domain of $g$, there exists a specified **composite morphism**\footnote{The composite may be written less concisely as $g \cdot f$ when this adds typographical clarity.} $gf$ whose domain is equal to the domain of $f$ and whose codomain is equal to the codomain of $g$, i.e.,:
$ f : X \to Y,\quad g : Y \to Z \qquad \rightsquigarrow\qquad gf : X \to Z\rlap{,}}$

This data is subject to the following two axioms:

-  For any $f : X \to Y$, the composites $1_Y f$ and $f 1_X$ are both equal to $f$.
-  For any composable triple of morphisms $f,g,h$, the composites $h(gf)$ and $(hg)f$ are equal and henceforth denoted by $hgf$.
$ f : X \to Y,\quad g : Y \to Z,\quad h : Z \to W \qquad \rightsquigarrow\qquad hgf : X \to W\rlap{,}}$

That is,  the composition law is associative and unital with the identity morphisms serving as two-sided identities.


SUGGESTION: domain morphism