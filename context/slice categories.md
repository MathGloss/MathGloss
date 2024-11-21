-  There is a category $\mathsf{C}/c$ whose objects are morphisms $f : x \to c$ with codomain $c$ and in which a morphism from $f : x \to c$ to $g : y \to c$ is a map $h : x \to y$ between the domains so that the triangle
$ \xymatrix@=10pt{ x \ar[rr]^h \ar[dr]_f && y \ar[dl]^g \\& c}$ **commutes**, i.e., so that $f = gh$.

The categories $c/\mathsf{C}$ and $\mathsf{C}/c$ are called **slice categories** of $\mathsf{C}$ **under** and **over** $c$, respectively.


\section{Duality}}

\epigraph{ The dual of any axiom for a category is also an axiom \ldots A simple metamathematical argument thus proves the \emph{duality principle}. If any statement about a category is deducible from the axioms for a category, the dual statement is likely deducible.}{Saunders Mac Lane, ``Duality for groups'' \cite{maclane-duality}}

Upon first acquaintance, the primary role played by the notion of a category might appear to be taxonomic: vector spaces and linear maps define one category, manifolds and smooth functions define another. But a category, as defined in \ref{defn:category}, is also a mathematical object in its own right, and as with any mathematical definition, this one is worthy of further consideration. Applying a mathematician's gaze to the definition of a category, the following observation quickly materializes. If we visualize the morphisms in a category as arrows pointing from their domain object to their codomain object, we might imagine simultaneously reversing  the directions of every arrow. This leads to the following notion.



The data described in Definition \ref{defn:op-category} defines a category $\mathsf{C}^\mathrm{op}$---i.e., the composition law is associative and unital---if and only if $\mathsf{C}$ defines a category. In summary, the process of ``turning around the arrows'' or ``exchanging domains and codomains'' exhibits a syntactical self-duality satisfied by the axioms for a category. Note that the category $\mathsf{C}^\mathrm{op}$ contains precisely the same information as the category $\mathsf{C}$. Questions about the one can be answered by examining the other.

 $\quad$


SUGGESTION: slice category