A **graded algebra** over the [[field]] $k$ is a [[graded vector space]] $A = \bigoplus_{i\geq 0} A_i$ equipped with an [[algebra over a field|algebra]] structure such that 
1. multiplication is compatible with the grading: i.e. $A_iA_i\subseteq A_{i+j}$ for all $i,j\geq 0$.
2. The [[identity element]] on $A$, written $1_A$, is in $A_0$.

The [[vector subspace|subspaces]] $A_i$ of $A$ are called **homogeneous components** of $A$, and an element $a\in A$ is **homogeneous of degree $d$** if $a\in A_d$. By simple linear algebra, any element $a\in A$ can be written *uniquely* as a sum $$\sum_{i\geq 0} a^{(i)}$$ where $a^{(i)}$ is homogeneous of degree $i$ and $a^{(i)} = 0$ for all but finitely many $i$.grt