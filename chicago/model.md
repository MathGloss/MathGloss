---
 layout: page
 title: model
 permalink: /chicago/model
---

Let $L$ be a [formal language of propositional logic](https://mathgloss.github.io/MathGloss/formal_language_of_propositional_logic) and let $\Gamma\subseteq \text{Form}(L)$. A **model** for $\Gamma$ is a [truth function](https://mathgloss.github.io/MathGloss/semantic_notion_of_truth) $t:\text{Form}(L) \to \{0,1\}$ such that $t(\gamma) = 1$ for all $\gamma\in \Gamma$. 

For any $\phi \in \text{Form}(L)$, we say that $\Gamma$ **models** $\phi$ if for every model $t$ of $\Gamma$, $t(\phi) = 1$. 