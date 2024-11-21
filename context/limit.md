[\textnormal{limits and colimits II}] For any diagram $F : \mathsf{J} \to \mathsf{C}$, a **limit** is a terminal object in the category of cones over $F$, i.e., in the category $\textstyle{\int}\!{\textup{Cone}(-,F)}$.  An object in the category of cones over $F$ is a cone over $F$, with any summit. In particular, the data of a terminal object in the category of cones consists of a limit object in $\mathsf{C}$ together with a specified  **limit cone**.  A morphism from a cone $\lambda : c \Rightarrow F$ to a cone $\mu : d \Rightarrow F$ is a morphism $f : c \to d$ in $\mathsf{C}$ so that for each $j \in \mathsf{J}$, $\mu_j \cdot f = \lambda_j$. In other words, a morphism of cones is a map between the summits so that each leg of the domain cone factors  through the corresponding leg of the codomain cone along this map.
$\xymatrix@C=35pt{ & & & c \ar[d]_f
 \ar@/^2.5ex/[dd]|(.4){\mathrm{co}lorbox{white}{\makebox(9,5){\scriptsize$\lambda_{ 0}$}}}
   \ar[ddl]|(.41){\mathrm{co}lorbox{white}{\makebox(9,4){\scriptsize$\lambda_{-1}$}}}
    \ar[ddlll]^\cdots \ar[ddll]|(.41){\mathrm{co}lorbox{white}{\makebox(9,4){\scriptsize$\lambda_{-2}$}}}
     \ar[ddr]|(.4){\mathrm{co}lorbox{white}{\makebox(7,4){\scriptsize$\lambda_{1}$}}}
      \ar[ddrr]|(.4){\mathrm{co}lorbox{white}{\makebox(9,4){\scriptsize$\lambda_{2}$}}}
        \ar[ddrrr]_\cdots \\
        & & & d \ar[d]|{\mathrm{co}lorbox{white}{\makebox(7,3){\scriptsize$\mu_{ 0}$}}}
         \ar[dl]|(.51){\mathrm{co}lorbox{white}{\makebox(9,4){\scriptsize$\mu_{-1}$}}}
          \ar[dlll]^\cdots \ar[dll]|(.51){\mathrm{co}lorbox{white}{\makebox(8,3){\scriptsize$\mu_{-2}$}}}
           \ar[dr]|{\mathrm{co}lorbox{white}{\makebox(8,3){\scriptsize$\mu_{1}$}}}
            \ar[drr]|{\mathrm{co}lorbox{white}{\makebox(9,4){\scriptsize$\mu_{2}$}}}
              \ar[drrr]_\cdots  & & &\\
         \cdots \ar[r] & F(-2) \ar[r] & F(-1) \ar[r] & F0 \ar[r] & F1 \ar[r] & F2 \ar[r] & \cdots }$
The forgetful functor $\textstyle{\int}\!{\textup{Cone}(-,F)} \to \mathsf{C}$ takes a cone to its summit.

Dually, a **colimit** is an initial object in the category of cones under $F$, i.e., in the category $\textstyle{\int}\!{\textup{Cone}(F,-)}$. An object in the category of cones under $F$ is a cone under $F$, with any nadir. In particular, the data of an initial object is comprised of the colimit object in $\mathsf{C}$ together with a specified  **colimit cone**. A morphism from a cone $\lambda : F \Rightarrow c$ to a cone $\mu : F \Rightarrow d$ is a morphism $f : c \to d$ so that for each $j \in \mathsf{J}$, $\mu_j = f \cdot \lambda_j$. In other words, a morphism of cones is a map between the nadirs so that each leg of the codomain cone factors through the corresponding leg of the domain cone along this map. The forgetful functor $\textstyle{\int}\!{\textup{Cone}(F,-)} \to \mathsf{C}$ takes a cone to its nadir.


SUGGESTION: limit object