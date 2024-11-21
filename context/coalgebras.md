-  An algebra for the closure closure operator\footnote{This is not a typo: Example \ref{ex:closure-operator} describes a closure operator on the poset of subsets of a topological space that sends a subset to its closure.}
on the poset of subsets of a topological space $X$ is exactly a closed subset of $X$. Dually, a coalgebra\footnote{Interpreting Definition \ref{defn:EM} for a monad $(T,\eta,\mu)$ on $\mathsf{C}^\mathrm{op}$ defines the category of **coalgebras** for the comonad on $\mathsf{C}$; see Exercise \ref{exc:coEM}.} for the interior kernel operator is exactly an open subset.



Various notations are common for the Eilenberg--Moore category, many involving the string ``alg '' to emphasize the interpretation of its objects as ``algebras'' of some sort. The notation used here, while less evocative, has the virtue of being concise.
\
 For any  monad $(T,\eta,\mu)$ acting on a category $\mathsf{C}$, there is an adjunction
$ \xymatrix{ \mathsf{C} \ar@<1ex>[r]^-{F^T} \ar@{}[r]|-\perp & \mathsf{C}^T \ar@<1ex>[l]^-{U^T}}$ between $\mathsf{C}$ and the Eilenberg--Moore category whose induced monad is $(T,\eta,\mu)$.


The functor $U^T : \mathsf{C}^T \to \mathsf{C}$ is the evident forgetful functor.  The functor $F^T : \mathsf{C} \to \mathsf{C}^T$ carries an object $A \in \mathsf{C}$ to the **free $T$-algebra** $ F^T\! A :eqq (TA,\mu_A : T^2A \to TA)$ and carries a morphism $f : A \to B$ to the **free $T$-algebra morphism** $ F^T\! f :eqq  (TA,\mu_A) \xrightarrow{Tf} (TB,\mu_B)\rlap{{\,}.}$ Note that $U^TF^T=T$.

The unit of the adjunction $F^T \dashv U^T$ is given by the natural transformation $\eta : 1_\mathsf{C} \Rightarrow T$. The components of the counit $\epsilon : F^TU^T \Rightarrow 1_{\mathsf{C}^T}$ are defined as follows:
$\epsilon_{(A,a)} :eqq  (TA,\mu_A) \xrightarrow{a} (A,a) \qquad \quad \vcenter{\xymatrix{ T^2A \ar[r]^{Ta} \ar[d]_{\mu_A} & TA \ar[d]^a \\ TA \ar[r]_a & A}}$ That is, the component of the counit at an algebra $(A,a) \in \mathsf{C}^T$ is given by the algebra structure map $a : TA \to A$; the commutative square demonstrates that this map defines a $T$-algebra homomorphism $a : (TA,\mu_A) \to (A,a)$. Note, in particular, that $U^T\epsilon F^T_A = \mu_A$, so that the monad underlying the adjunction $F^T \dashv U^T$ is $(T,\eta,\mu)$. The  straightforward verifications that the unit and counit satisfy the triangle identities are
 left to Exercise \ref{exc:EM}.



A second solution to the problem of finding an adjunction that induces a given monad is given by the Kleisli category construction.





 For instance:


SUGGESTION: coalgebra