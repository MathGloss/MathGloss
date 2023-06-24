---
aliases: truth function
---
A **truth function** on a [[formal language of propositional logic]] $L$ (using [[all logical operators can be replaced with implies and bottom|only]] the logical operators $\rightarrow$ and $\bot$) is a function $f:\text{Form}(L) \to \{0,1\}$ such that $t(\bot) = 0$, $t(\top) = 1$, and $$t(A\rightarrow B) = \begin{cases}0 & \text{if } t(A) = 1 \text{ and } f(B) = 0\\ 1 &\text{otherwise} \end{cases}$$ for all $A,B \in \text{Form}(L)$.