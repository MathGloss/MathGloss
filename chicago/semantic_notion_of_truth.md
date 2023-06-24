---
 layout: page
 title: semantic notion of truth
 permalink: /chicago/semantic_notion_of_truth
---

A **truth function** on a [formal language of propositional logic](https://defsmath.github.io/DefsMath/formal_language_of_propositional_logic) $L$ (using [only](https://defsmath.github.io/DefsMath/all_logical_operators_can_be_replaced_with_implies_and_bottom) the logical operators $\rightarrow$ and $\bot$) is a function $f:\text{Form}(L) \to \{0,1\}$ such that $t(\bot) = 0$, $t(\top) = 1$, and $$t(A\rightarrow B) = \begin{cases}0 & \text{if } t(A) = 1 \text{ and } f(B) = 0\\ 1 &\text{otherwise} \end{cases}$$ for all $A,B \in \text{Form}(L)$.