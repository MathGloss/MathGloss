---
 layout: page
 title: syntactic proof
 permalink: /syntactic_proof
---
Let $\text{Form}(L)$ be a [formal language of propositional logic](https://defsmath.github.io/DefsMath/formal_language_of_propositional_logic). Then a **proof** of $S_k\in \text{Form}(L)$ from a subset $\Gamma\subseteq \text{Form}(L)$ is a finite list of statements $S_1,\dots, S_k$ such that for all $S_i$, at least one of the following is true:
1. $S_i \in \Gamma$;
2. $S_i$ is an [axiom](https://defsmath.github.io/DefsMath/Axioms_of_Propositional_Logic);
3. there exist $j,\ell < i$ such that $S_\ell = S_j \rightarrow S_i$, i.e. that $S_i$ "is there by" [modus ponens](https://defsmath.github.io/DefsMath/modus_ponens).

If there exists a proof from $\Gamma \subseteq \text{Form}(L)$ to $\phi \in \text{Form}(L)$, we say that $\Gamma$ **proves** $\phi$ and we write $\Gamma\vdash \phi$.