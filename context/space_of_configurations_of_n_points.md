---
layout: page
title: space of configurations of n points
permalink: /context/space_of_configurations_of_n_points
---
More formally, the **space of ordered configurations of $n$ points** is a subspace of the product space $X^n$, namely the complement of the ``fat diagonal''
$ \textup{PConf}_n(X) :eqq \big\{ (x_1,\ldots, x_n) \in X^n \bigm| x_i \neq x_j\ \forall i \neq j\big\}\rlap{,}}$
The symmetric group $\Sigma_n$ acts on $X^n$ by permuting the coordinates, and this action restricts to the subspace $\textup{PConf}_n(X)\subset X^n$. The colimit of the diagram $\textup{PConf}_n(X) : \mathsf{B}\Sigma_n \to \textup{\textsf{Top}}$ defines the **space of configurations of $n$ points**
$ \textup{Conf}_n(X) :eqq \mathrm{colim} \left( \mathsf{B}\Sigma_n \xrightarrow{\textup{PConf}_n(X)} \textup{\textsf{Top}}\right)\rlap{,}}$ Exercise \ref{exc:orbit-colimit} describes its underlying set.


SUGGESTION: space of configurations of n points