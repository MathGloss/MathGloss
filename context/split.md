---
layout: page
title: split
permalink: /context/split
---
Alternatively, applying Theorem \ref{thm:set-prod-equalizer} in the simplified form of Exercise \ref{exc:simplified-limit-formula}, the limit $A^e$ is constructed as the equalizer
$ \xymatrix{A^e\ \ar@{>->}[r]^s & A \ar@<.5ex>[r]^1 \ar@<-.5ex>[r]_e & A}$ The universal property of the equalizer  implies that $e$ factors through $s$ along a unique map $r$.
$ \xymatrix{A \ar[dr]^e \ar@{-->}[d]_r \\ A^e\ \ar@{>->}[r]^s & A \ar@<.5ex>[r]^1 \ar@<-.5ex>[r]_e & A}$ The factorization $e = sr$ is said to **split** the idempotent.
Now $srs = es =s$ implies that $rs$ and $1_{A^e}$ both define factorizations of the diagram
$ \xymatrix{A^e \ar[dr]^s \ar@{-->}@<-.5ex>[d]_{rs} \ar@{-->}@<.5ex>[d]^{1_{A^e}} \\ A^e\ \ar@{>->}[r]^s & A \ar@<.5ex>[r]^1 \ar@<-.5ex>[r]_e & A}$ Uniqueness implies $rs = 1_{A^e}$ so $A^e$ is a retract of $A$. Conversely, any retract diagram
$ \xymatrix{ B\ \ar@{>->}[r]^s & A \ar@{->>}[r]^r & B & rs= 1_B}$ gives rise to an idempotent $sr$ on $A$, which is split by  $B$.


SUGGESTION: split idempotent