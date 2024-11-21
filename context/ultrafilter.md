---
layout: page
title: ultrafilter
permalink: /context/ultrafilter.md
---
-  The composite adjunction
$ \xymatrix{ \textup{\textsf{cHaus}} \ar@<-1ex>[r] \ar@{}[r]|-\perp & \textup{\textsf{Top}} \ar@<-1ex>[l]_-\beta \ar@<-1ex>[r]_U \ar@{}[r]|\perp & \textup{\textsf{Set}} \ar@<-1ex>[l]_D}$ induces a monad $\beta : \textup{\textsf{Set}} \to \textup{\textsf{Set}}$ that sends a set to the underlying set of the Stone--\v{C}ech compactification of the discrete space on that set. There is a simpler description: $\beta(A)$ is the set of ultrafilters on $A$. An **ultrafilter** is a set of subsets of $A$ that is upward closed, closed under finite intersections, and for each subset of $A$ contains either that subset or its complement but not both; see Exercise \ref{exc:ultra-monad}.

SUGGESTION: ultrafilter