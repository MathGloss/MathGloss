---
layout: page
title: colimit cone
permalink: /context/colimit_cone
---
For any diagram $F \colon \mathsf{J} \to \mathsf{C}$, a **limit** is a terminal object in the category of cones over $F$, i.e., in the category $\textstyle{\int}\!{el}(-,F)}$.  An object in the category of cones over $F$ is a cone over $F$, with any summit. In particular, the data of a terminal object in the category of cones consists of a limit object in $\mathsf{C}$ together with a specified  **limit cone**.  A morphism from a cone $\lambda \colon c \Rightarrow F$ to a cone $\mu \colon d \Rightarrow F$ is a morphism $f \colon c \to d$ in $\mathsf{C}$ so that for each $j \in \mathsf{J}$, $\mu_j \cdot f = \lambda_j$. In other words, a morphism of cones is a map between the summits so that each leg of the domain cone factors  through the corresponding leg of the codomain cone along this map.
$$\xymatrix@C=35pt{ & & & c \ar[d]_f
 \ar@/^2.5ex/[dd]\mid(.4){\colorbox{white}{\makebox(9,5){\scriptsize$\lambda_{ 0}$}}}
   \ar[ddl]\mid(.41){\colorbox{white}{\makebox(9,4){\scriptsize$\lambda_{-1}$}}}
    \ar[ddlll]^\cdots \ar[ddll]\mid(.41){\colorbox{white}{\makebox(9,4){\scriptsize$\lambda_{-2}$}}}
     \ar[ddr]\mid(.4){\colorbox{white}{\makebox(7,4){\scriptsize$\lambda_{1}$}}}
      \ar[ddrr]\mid(.4){\colorbox{white}{\makebox(9,4){\scriptsize$\lambda_{2}$}}}
        \ar[ddrrr]_\cdots \\
        & & & d \ar[d]\mid{\colorbox{white}{\makebox(7,3){\scriptsize$\mu_{ 0}$}}}
         \ar[dl]\mid(.51){\colorbox{white}{\makebox(9,4){\scriptsize$\mu_{-1}$}}}
          \ar[dlll]^\cdots \ar[dll]\mid(.51){\colorbox{white}{\makebox(8,3){\scriptsize$\mu_{-2}$}}}
           \ar[dr]\mid{\colorbox{white}{\makebox(8,3){\scriptsize$\mu_{1}$}}}
            \ar[drr]\mid{\colorbox{white}{\makebox(9,4){\scriptsize$\mu_{2}$}}}
              \ar[drrr]_\cdots  & & &\\
         \cdots \ar[r] & F(-2) \ar[r] & F(-1) \ar[r] & F0 \ar[r] & F1 \ar[r] & F2 \ar[r] & \cdots }$$
The forgetful functor $\textstyle{\int}\!{el}(-,F)} \to \mathsf{C}$ takes a cone to its summit.

Dually, a **colimit** is an initial object in the category of cones under $F$, i.e., in the category $\textstyle{\int}\!{el}(F,-)}$. An object in the category of cones under $F$ is a cone under $F$, with any nadir. In particular, the data of an initial object is comprised of the colimit object in $\mathsf{C}$ together with a specified  **colimit cone**. A morphism from a cone $\lambda \colon F \Rightarrow c$ to a cone $\mu \colon F \Rightarrow d$ is a morphism $f \colon c \to d$ so that for each $j \in \mathsf{J}$, $\mu_j = f \cdot \lambda_j$. In other words, a morphism of cones is a map between the nadirs so that each leg of the codomain cone factors through the corresponding leg of the domain cone along this map. The forgetful functor $\textstyle{\int}\!{el}(F,-)} \to \mathsf{C}$ takes a cone to its nadir.
