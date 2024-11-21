 Let $\mathsf{C}$ be any category. The **opposite category** $\mathsf{C}^\mathrm{op}$ has

-  the same objects as in $\mathsf{C}$, and
-  a morphism $f^\mathrm{op}$ in $\mathsf{C}^\mathrm{op}$ for each a morphism $f$ in $\mathsf{C}$ so that the domain of $f^\mathrm{op}$ is defined to be the codomain of $f$ and the codomain of $f^\mathrm{op}$ is defined to be the domain of $f$: i.e.,
$ f^{\mathrm{op}} : X \to Y\quad \in \mathsf{C}^\mathrm{op} \qquad \leftrightsquigarrow \qquad f : Y \to X\quad \in \mathsf{C}\rlap{{\,}.}$

That is, $\mathsf{C}^\mathrm{op}$ has the same objects and morphisms as $\mathsf{C}$, except that ``each morphism is pointing in the opposite direction.'' The remaining structure of the category $\mathsf{C}^\mathrm{op}$ is given as follows:

-  For each object $X$, the arrow $1_X^\mathrm{op}$ serves as its identity in $\mathsf{C}^\mathrm{op}$.
-  To define composition, observe that a pair of morphisms $f^\mathrm{op},g^\mathrm{op}$ in $\mathsf{C}^\mathrm{op}$ is composable precisely when the pair $g,f$ is composable in $\mathsf{C}$, i.e., precisely when the codomain of $g$ equals the domain of $f$. We then define $g^\mathrm{op} \cdot  f^\mathrm{op}$ to be $(f\cdot g)^\mathrm{op}$: i.e.,
$ {clccl}
 f^\mathrm{op} : X \to Y,\ g^\mathrm{op} : Y \to Z & \in \mathsf{C}^\mathrm{op}&\rightsquigarrow& g^\mathrm{op} f^\mathrm{op} : X \to Z & \in \mathsf{C}^\mathrm{op}\\ \rotatebox{90}{$\leftrightsquigarrow$} & & & \rotatebox{90}{$\leftrightsquigarrow$}& \\ g : Z \to Y,\ f : Y \to X  &\in \mathsf{C} & \rightsquigarrow &  f g : Z \to X &  \in \mathsf{C}
 $



SUGGESTION: opposite category