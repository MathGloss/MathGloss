---
layout: page
title: free group on a single generator
permalink: /context/free_group_on_a_single_generator
---
-  The forgetful functor $U : \textup{\textsf{Group}} \to \textup{\textsf{Set}}$ is represented by the group $\mathbb{Z}$. That is, for any group $G$, there is a natural isomorphism $\textup{\textsf{Group}}(\mathbb{Z},G) \mathrm{co}ng UG$ that associates, to every element $g \in UG$, the unique homomorphism $\mathbb{Z} \to G$ that maps the integer 1 to $g$. This defines a bijection because every homomorphism $\mathbb{Z} \to G$ is determined by the image of the generator $1$; that is to say, $\mathbb{Z}$ is the **free group on a single generator**. This bijection is natural because the composite group homomorphism $\mathbb{Z} \xrightarrow{g} G \xrightarrow{\phi} H$ carries the integer 1 to $\phi(g) \in H$.

SUGGESTION: free group on a single generator

From [Category Theory in Context](https://mathgloss.github.io/MathGloss/context.html)