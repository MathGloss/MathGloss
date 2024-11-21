 A **monad** on a category $\mathsf{C}$ consists of

-  an endofunctor $T : \mathsf{C} \to \mathsf{C}$,
-  a **unit** natural transformation $\eta : 1_\mathsf{C} \Rightarrow T$, and
-  a **multiplication** natural transformation $\mu : T^2 \Rightarrow T$,

so that the following diagrams commute in $\mathsf{C}^\mathsf{C}$:
$ \xymatrix{ T^3 \ar@{=>}[r]^{T\mu} \ar@{=>}[d]_{\mu T} & T^2 \ar@{=>}[d]^{\mu} & & T \ar@{=>}[r]^{\eta T} \ar@{=>}[dr]_{1_T} & T^2 \ar@{=>}[d]^\mu & T \ar@{=>}[l]_{T\eta} \ar@{=>}[dl]^{1_T} \\ T^2 \ar@{=>}[r]_{\mu} & T & & & T}$


SUGGESTION: monad on a category