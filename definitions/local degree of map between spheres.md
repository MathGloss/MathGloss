Let $f:S^n\to S^n$ be a [[continuous]] function such that for some $y\in S^n$, the [[preimage]] $f^{-1}(y)$ is finite. Denote the elements of $f^{-1}(y)$ by $\{x_i\}_{i=1}^m$. Let $\{U_i\}_{i=1}^m$ be disjoint [[neighborhood|neighborhoods]] of the $x_i$. Then $f$ maps each $U_i$ into a [[neighborhood]] $V$ of $y$. Then $$f(U_i \setminus \{x_i\}) \subset B\setminus \{y\}$$ for all $y$ and the following diagram of [[homology group|homology groups]] and [[relative homology groups]] [[commutative diagram|commuptes]]:

![[Screen Shot 2021-12-02 at 10.44.27 AM.png]]

where all of the maps are "obvious:" $k_i$ and $p_i$ are induced by inclusion. The two [[group homomorphism|isomorphisms]] on the top of the diagram come from the [[Excision Theorem]] and the two on the bottom come from the [[long exact sequence of a pair]].

The top two [[group|groups]] are [[reduced homology of the sphere|then]] [[group homomorphism|isomorphic]] to $H_n(S^n) \approx\mathbb Z$, so the top [[group homomorphism|homomorphism]] [[classification of group homomorphisms Z to G|is then]] multiplication by an integer $d$. This integer is the **local degree** of $f$ at $x_i$, written $\text{deg}(f)_{|x_i}$.

