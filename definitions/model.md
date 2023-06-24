---
aliases: models
---
Let $L$ be a [[formal language of propositional logic]] and let $\Gamma\subseteq \text{Form}(L)$. A **model** for $\Gamma$ is a [[semantic notion of truth|truth function]] $t:\text{Form}(L) \to \{0,1\}$ such that $t(\gamma) = 1$ for all $\gamma\in \Gamma$. 

For any $\phi \in \text{Form}(L)$, we say that $\Gamma$ **models** $\phi$ if for every model $t$ of $\Gamma$, $t(\phi) = 1$. 