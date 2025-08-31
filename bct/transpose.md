---
layout: page
title: transpose
permalink: /bct/transpose
---
Given objects $ A \in \mathscr{A} $ and $ B \in \mathscr{B} $ , the correspondence X between maps $ F(A) \to B $ and $ A \to G(B) $ is denoted by a horizontal bar, in both directions: $ \begin{array}{ccc} \Bigl(F(A) \stackrel{g}{\longrightarrow} B\Bigr) & \mapsto & \Bigl(A \stackrel{\bar{g}{\longrightarrow}} G(B)\Bigr), \ \Bigl(F(A) \stackrel{\bar{f}{\longrightarrow}} B\Bigr) & \mathrel{\reflectbox{\ensuremath{\mapsto}}} & \Bigl(A \stackrel{f}{\longrightarrow} G(B)\Bigr). \end{array} $ So $ \bar{\bar{f}} = f $ and $ \bar{\bar{g}} = g $ . We call $ \bar{f} $ the **transpose** of $ f $ , and similarly for $ g $ . The naturality axiom has two parts: $ \overline{\Bigl(F(A) \stackrel{g}{\longrightarrow} B \stackrel{q}{\longrightarrow} B'\Bigr)} \quad = \quad \Bigl(A \stackrel{\bar{g}{\longrightarrow}} G(B) \stackrel{G(q)}{\longrightarrow} G(B')\Bigr) $ (that is, $ \overline{q \circ g} = G(q) \circ \bar{g} $ ) for all $ g $ and $ q $ , and $ \overline{\Bigl(A' \stackrel{p}{\longrightarrow} A \stackrel{f}{\longrightarrow} G(B)\Bigr)} \quad = \quad \Bigl(F(A') \stackrel{F(p)}{\longrightarrow} F(A) \stackrel{\bar{f}{\longrightarrow}} B\Bigr) $ for all $ p $ and $ f $ .


From [Basic Category Theory](https://mathgloss.github.io/MathGloss/bct.html)