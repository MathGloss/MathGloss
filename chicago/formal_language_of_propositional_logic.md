---
 layout: page
 title: formal language of propositional logic
 permalink: /chicago/formal_language_of_propositional_logic
---
An at-most-[countable](https://mathgloss.github.io/MathGloss/countable) collection $\{A_i\}_{i\in I}$ whose elements are called **atomic formulae** or **propositional variables** together with some subset of the **logical connectors** $(\land, \lor, \rightarrow, \leftrightarrow, \neg)$ and $\{\top, \bot\}$ is called a **language for propositional logic**. Name this whole agglomeration $L$. Then $\text{Form}(L)$ is the smallest set containing $\{A_i\}_{i\in I}$, $\top$, and $\bot$ that is closed under the remaining logical operators, which at their most basic take two (one in the case of $\neg$) atomic variables and spit out a new formula.

We know that this set is nonempty because there exists a set $D$ consisting of all finite strings with characters drawn from $\{A_i\}_{i\in I}$, $\top$, $\bot$, and $\{\land,\lor, \rightarrow, \leftrightarrow, \neg\}$. Consider $\bigcap _{S\in F}S$ where $F$ is a collection of sets that are subsets of $D$ satisfying the closure property.  This is the smallest such set, but it does not tell us what the elements look like. 

Consider a map $LC: \mathcal P(D) \to \mathcal P(D)$ given by $$LC(S)= S\cup\{(B)\rightarrow (C), (B)\leftrightarrow (C), (B)\land (C), (B)\lor (C), \neg(B) \mid B,C\in S\}.$$ Let $$H = \bigcup_{i\in \mathbb N} LC^i (\{A_j\}_{j\in I} \cup \{\bot,\top\}).$$ Then $H = \text{Form}(L)$:

Let $S$ be some candidate set for $\text{Form}(L)$. It suffices to show that $H\subseteq S$. To show this it suffices to show that $LC^i (\{A_j\}_{j\in I} \cup \{\bot,\top\}) \subseteq S$ for all $i$. The base case $i=0$ follows from the definition we are looking to satisfy and the hypothesis that $S$ satisfies it. The inductive step follows immediately from the definition and its closure property. 