---
layout: page
title: lim sup
permalink: /context/lim_sup
---
A function $x : \mathbb{N} \to \mathbb{R}$ defines a sequence $(x_n)_{n \in \mathbb{N}}$ of real numbers. The **lim inf** and **lim sup** is defined by regarding the sequence as a bifunctor $\mathbb{N} \times \mathbb{N} \xrightarrow{+} \mathbb{N} \xrightarrow{x} \mathbb{R}$ indexed by the discrete category $\mathbb{N} \times \mathbb{N}$:
$ \lim \inf_{n \to \infty} x_n = \adjustlimits\sup_{n \geq 0} \inf_{m \geq n} x_m = \adjustlimits\sup_{n \geq 0} \inf_{m \geq 0} x_{n+m} = \mathrm{colim}_n \lim_m x_{n+m}$
$ \lim \sup_{n \to \infty} x_n = \adjustlimits\inf_{n \geq 0} \sup_{m \geq n} x_m = \adjustlimits\inf_{n \geq 0} \sup_{m \geq 0} x_{n+m} = \lim_n \mathrm{colim}_m x_{n+m}$
Having translated these analytic notions into categorical ones, Lemma \ref{lem:lim-colim-map} applies in the form of an inequality:
$ \lim\inf_{n \to \infty} x_n \leq \lim\sup_{n \to \infty} x_n\rlap{,}}$
 The  limit of this sequence exists if and only if this inequality is an equality.


SUGGESTION: lim sup of a sequence

From [Category Theory in Context](https://mathgloss.github.io/MathGloss/context.html)