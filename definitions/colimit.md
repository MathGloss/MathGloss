---
aliases: universal property for colimits
---
Let $F$ be a [[D-shaped diagram]] in the [[category]] $\mathcal D[\mathcal C]$. The **colimit** of $F$, written $\text{colim}F$, is an object of $\mathcal C$ together with a morphism of diagrams $\iota: F\to \underline{\text{colim} F}$ that is [[initial object|initial]] among all such morphisms. That is, if $\eta:F\to \underline A$ is a morphism of diagrams, then there is a unique map $\tilde \eta:\text{colim}(F)\to A$ in $\mathcal C$ such that $\tilde \eta\circ \iota = \eta$.

We can also express this as a diagram. For each map $d:D\to D'$ in $\mathcal D$, the following [[commutative diagram|diagram commutes]]:
![[Screen Shot 2022-01-27 at 11.55.10 AM.png]]

https://www.wikidata.org/wiki/Q1322614