Let $M\subset\mathbb R^n$ be a [[compact]], [[oriented manifold|oriented]] [[embedded m-dimensional manifold with boundary]]. Let $U$ be an [[open]] set containing $M$ and $\omega$ an [[differential k-form|m-form]] on $U$. 

For each $p \in M$, choose a smooth [[local parametrization]] $\phi_p: U_p \to M$ [[compatibility with orientation|compatible]] with the [[orientation]] on $M$. Then the image $\phi_p(U_p)$ is an [[open]] subset of $M$, so there exists an [[open]] set $V_p \subset \mathbb R^n$ such that $\phi_p(U_p) = V_p \cap M$ because of the [[subspace topology]]. Since $M$ is [[compact]], finitely many of these $V_p$ cover $M$. Call them $V_i$ for $1\leq i \leq k$. Then $$V = \bigcup\limits_{i=1}^k V_i$$ is an [[open]] set containing $M$. 

[[existence of partitions of unity|Let]] $\{\psi_j\}$ be a [[partition of unity]] subordinate to the $V_i$. Then $\omega = \sum_{j} \psi_j \omega$, so define $$\int_M \omega = \sum_{j} \psi_j\omega.$$ #todo 

