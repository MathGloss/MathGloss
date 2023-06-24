---
 layout: page
 title: ∆-complex.
 permalink: /∆-complex.
---% Options for packages loaded elsewhere
\PassOptionsToPackage{unicode}{hyperref}
\PassOptionsToPackage{hyphens}{url}
%
\documentclass[
]{article}
\usepackage{amsmath,amssymb}
\usepackage{lmodern}
\usepackage{iftex}
\ifPDFTeX
  \usepackage[T1]{fontenc}
  \usepackage[utf8]{inputenc}
  \usepackage{textcomp} % provide euro and other symbols
\else % if luatex or xetex
  \usepackage{unicode-math}
  \defaultfontfeatures{Scale=MatchLowercase}
  \defaultfontfeatures[\rmfamily]{Ligatures=TeX,Scale=1}
\fi
% Use upquote if available, for straight quotes in verbatim environments
\IfFileExists{upquote.sty}{\usepackage{upquote}}{}
\IfFileExists{microtype.sty}{% use microtype if available
  \usepackage[]{microtype}
  \UseMicrotypeSet[protrusion]{basicmath} % disable protrusion for tt fonts
}{}
\makeatletter
\@ifundefined{KOMAClassName}{% if non-KOMA class
  \IfFileExists{parskip.sty}{%
    \usepackage{parskip}
  }{% else
    \setlength{\parindent}{0pt}
    \setlength{\parskip}{6pt plus 2pt minus 1pt}}
}{% if KOMA class
  \KOMAoptions{parskip=half}}
\makeatother
\usepackage{xcolor}
\setlength{\emergencystretch}{3em} % prevent overfull lines
\providecommand{\tightlist}{%
  \setlength{\itemsep}{0pt}\setlength{\parskip}{0pt}}
\setcounter{secnumdepth}{-\maxdimen} % remove section numbering
\ifLuaTeX
  \usepackage{selnolig}  % disable illegal ligatures
\fi
\IfFileExists{bookmark.sty}{\usepackage{bookmark}}{\usepackage{hyperref}}
\IfFileExists{xurl.sty}{\usepackage{xurl}}{} % add URL line breaks if available
\urlstyle{same} % disable monospaced font for URLs
\hypersetup{
  pdftitle={∆-complex},
  hidelinks,
  pdfcreator={LaTeX via pandoc}}

\title{∆-complex}
\author{}
\date{}

\begin{document}
\maketitle

A \textbf{Δ-complex} is a quotient vector space of a collection of
disjoint simplices obtained by identifying certain faces by the
canonical linear homeomorphisms described in the definition of
barycentric coordinates.

Consider a collection of n-simplices {\(\Delta_{\alpha}^{n}\)} of
various dimension (i.e. {\(n\)} is not fixed) and some sets
{\(\mathcal{F}_{i}\)} of faces of the {\(\Delta_{\alpha}^{n}\)} such
that within each {\(\mathcal{F}_{i}\)}, each face has the same dimension
(i.e. value for {\(n\)}). We can take a quotient vector space of the
disjoint union {\(\coprod\limits_{\alpha}\Delta_{\alpha}^{n}\)} by
identifying all of the faces in each {\(\mathcal{F}_{i}\)} via the
canonical linear homeomorphisms described in the definition of
barycentric coordinates.

\end{document}
