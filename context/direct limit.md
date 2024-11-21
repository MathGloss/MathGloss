
Definitions \ref{defn:product}, \ref{defn:terminal}, \ref{defn:equalizer}, \ref{defn:pullback}, and \ref{defn:inverse} dualize to define:

-  A  **coproduct** $} $\mathrm{co}prod_{j \in J} A_j$ is the colimit of a diagram $(A_j)_{j \in J}$ indexed by a discrete category $J$. The legs of the colimit cone $\iota_{j'} : A_{j'} \to \mathrm{co}prod_{j \in J} A_j$ are referred to as **coproduct injections**, though in pathological cases these maps might not be monomorphisms (see Exercise \ref{exc:injection-mono}).
-  An **initial object** is the colimit of the empty diagram.
-  A  **coequalizer** is a colimit of a diagram indexed by the parallel pair category $\bullet\rightrightarrows \bullet$. The coequalizer of a parallel pair of maps $f,g : A \rightrightarrows B$ is the universal map $h : B \to C$ with the property that $hf = hg$.  The colimit cone
$ \xymatrix{A \ar@<.5ex>[r]^f \ar@<-.5ex>[r]_g & B \ar@{->>}[r]^h & C}$ is called a **coequalizer diagram**. Diagrams of this shape are also called **forks**.
-  A **pushout** is a colimit of a diagram indexed by  the poset category $\bullet \leftarrow \bullet \to \bullet$.  Dualizing the convention introduced in Definition \ref{defn:pullback}, the symbol ``$\ulcorner$'' indicates that a commutative square
$ \xymatrix{ A \ar[r]^f \ar[d]_g \ar@{}[dr]|(.8){\ulcorner} & B \ar[d]^k \\ C \ar[r]_h & P}$ is a pushout,  i.e., is a colimit diagram. The pushout is the universal commutative square under the maps $f$ and $g$.
-  The colimit of a diagram indexed by the ordinal $\bbomega$ is called a **sequential colimit** or **direct limit**. The colimit of a diagram
$ \xymatrix{ F_0 \ar[r] & F_1 \ar[r] & F_2 \ar[r] & F_3 \ar[r] & \cdots}$ frequently denoted by $\varinjlim F_n$, defines a diagram of shape $\bbomega +1$. The term ``direct limit'' is sometimes also used to refer to colimits of any shape.



SUGGESTION: direct limit