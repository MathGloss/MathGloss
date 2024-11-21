-  By Example \ref{ex:set-cart-closed}, the contravariant power set functor is its own mutual right adjoint:
$ \xymatrix{ \textup{\textsf{Set}} \ar@<1ex>[r]^-P \ar@{}[r]|-\perp & \textup{\textsf{Set}}^\mathrm{op} \ar@<1ex>[l]^-P} \qquad \qquad \textup{\textsf{Set}}(A,PB) \mathrm{co}ng \textup{\textsf{Set}}(B,PA) $ A function from $A$ to the power set of $B$, or equally a function from $B$ to the power set of $A$, can be encoded as a function $A \times B \to \Omega$, i.e., as a subset of $A \times B$. The induced **double power set monad** takes a set $A$ to $P^2A$. The components of the unit are the ``principal ultrafilter'' functions $\eta_A: A \to P^2A$ that send an element $a$ to the set of subsets of $A$ that contain $a$. The components of the multiplication take a set of sets of sets of subsets to the set of subsets of $A$ with the property that one of the sets of sets of subsets is the set of all sets of subsets of $A$ that include that particular subset as an element.\footnote{This is one of those instances where it is easier to speak mathematics than to speak English: the multiplication is the inverse image function for the map $\eta_{PA} : PA \to P^3A$.} A similar monad can be defined with any other set in place of the two-element set $\Omega$; in computer science contexts, these are called **continuation monads**. This construction can also be generalized to other cartesian closed categories. For instance, there is a similar **double dual monad** on $\textup{\textsf{Vect}}_\mathbbe{k}$.




 Monads also arise in nature:


SUGGESTION: continuation monad