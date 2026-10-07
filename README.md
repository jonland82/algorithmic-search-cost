# Disorder Potential and the Cost of Search

**Jonathan R. Landers · October 2026**

[Read the website](https://jonland82.github.io/algorithmic-search-cost/) · [Browse the repository](https://github.com/jonland82/algorithmic-search-cost)

Two notes study how an array's disorder affects comparison search. The shared measure is squared rank displacement,

$$
V(A)=\frac12\sum_{i=1}^{n}\bigl(\operatorname{rank}_A(a_i)-i\bigr)^2.
$$

## Papers

| Paper | Main result | PDF | LaTeX |
| --- | --- | --- | --- |
| **Disorder Potential and the Cost of Search** (version 2) | With only $V(A)\le E$, one search has tight worst-case cost $\Theta(\log n+\min\{n,\sqrt E\})$. The paper also shows why the location of disorder matters beyond its total potential. | [PDF](disorder_potential_search_note_v2.pdf) | [Source](disorder_potential_search_note_v2.tex) |
| **Search Under a Disorder Budget** | For $q$ searches on one fixed array, preprocessing yields $T_q^*(n,E)=O(q\log n+\min\{qR_E,n\log(R_E+1)\})$, where $R_E=1+D_E$ and $D_E$ is the displacement bound implied by $E$. The note also explains verified learned certificates. | [PDF](search-under-a-disorder-budget/search_under_a_disorder_budget.pdf) | [Source](search-under-a-disorder-budget/search_under_a_disorder_budget.tex) |

The [archived original draft](archived-draft-materials/disorder_potential_search_note.pdf) and its [LaTeX source](archived-draft-materials/disorder_potential_search_note.tex) remain available for historical context.

## Models

The first paper gives the search algorithm a numerical promise $V(A)\le E$, with no auxiliary index or preprocessing transcript. The extension allows preprocessing comparisons among array keys and an $O(n)$-word index, charging their cost along with the later target comparisons.

The website is the root [index.html](index.html), published through GitHub Pages from master.
