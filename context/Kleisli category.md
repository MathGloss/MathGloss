 Let $\mathsf{C}$ be a category with a monad $(T,\eta,\mu)$. The **Kleisli category**  $\mathsf{C}_T$ is defined so that

-   its objects are the objects of $\mathsf{C}$, and
-   a morphism from $A$ to $B$ in $\mathsf{C}_T$, depicted as $A \rightsquigarrow B$,  is a morphism $A \to TB$ in $\mathsf{C}$.
 Identities and composition are defined using the monad structure:

-  The unit $\eta_A : A \to TA$ defines the identity morphism $A \rightsquigarrow A  \in \mathsf{C}_T$.
-  The composite of a morphism $f : A \to TB$ from $A$ to $B$ with a morphism $g : B \to TC$ from $B$ to $C$ is defined to be
$ \xymatrix{ A \ar[r]^f & TB \ar[r]^{Tg} & T^2C \ar[r]^{\mu_C} & TC\rlap{{\,}.}}$

The verification that these operations are associative and unital is left as Exercise \ref{exc:kleisli-cat}.


SUGGESTION: Kleisli category