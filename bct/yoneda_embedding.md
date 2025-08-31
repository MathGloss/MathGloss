---
layout: page
title: Yoneda embedding
permalink: /bct/yoneda_embedding
---
Any map $ A \stackrel{f}{\longrightarrow} A' $ in $ \mathscr{A} $ induces a natural transformation $ \xymatrix@C+1em{ \mathscr{A}^\op \rtwocell<4>^{\h_A}_{\h_{A'}}{\hspace{.5em}\h_f} &\mathbf{Set} } $ (also called $ \mathscr{A}( - , f) $ , $ f_* $ or $ f \circ - $ ), whose component at an object $ B \in \mathscr{A} $ is $ \begin{array}{ccc} \h_A(B) = \mathscr{A}(B, A) &\to & \h_{A'}(B) = \mathscr{A}(B, A') \ p &\mapsto & f \circ p. \end{array} $ Let $ \mathscr{A} $ be a locally small category. The **Yoneda embedding** of $ \mathscr{A} $ is the functor $ \h_\bullet{\colon}\linebreak[0] \mathscr{A} \to \ftrcat{\mathscr{A}^\op}{\mathbf{Set}} $ defined on objects $ A $ by $ \h_\bullet(A) = \h_A $ and on maps $ f $ by $ \h_\bullet(f) = \h_f $ . Here is a summary of the definitions so far.


From [Basic Category Theory](https://mathgloss.github.io/MathGloss/bct.html)