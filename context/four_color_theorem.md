---
layout: page
title: four color theorem
permalink: /context/four_color_theorem
---
To illustrate, consider the set of vertex colorings of a graph subject to the requirement that  adjacent vertices are assigned distinct colors.  There is a contravariant functor from the category of graphs to the category of sets that takes a graph to the set of $n$-colorings of its vertices. To explain the contravariance, note that an $n$-coloring of a graph $G$ and a graph homomorphism $G' \to G$  induce an $n$-coloring of $G'$ that colors each vertex of $G'$ to match the color of its image: as graph homomorphisms preserve the incidence relation on vertices, any two adjacent vertices of $G'$ are assigned distinct colors. This defines the action of the functor $n\text{-}\textup{Color} : \textup{\textsf{Graph}}^\mathrm{op} \to \textup{\textsf{Set}}$ on morphisms.\footnote{The **four color theorem** states that if $G$ is a simple planar graph, then the set $4$-$\textup{Color}(G)$ is non-empty. Functoriality implies that any graph admitting a graph homomorphism to a planar graph also admits a 4-coloring. For instance, complete bipartite graphs, which are typically non-planar, will admit homomorphisms of this type.}

SUGGESTION: Four color theorem