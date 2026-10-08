# Disorder Potential and the Cost of Search

**Jonathan R. Landers · October 2026**

[Read the website](https://jonland82.github.io/algorithmic-search-cost/) · [Browse the repository](https://github.com/jonland82/algorithmic-search-cost)

Three notes study how array disorder and target uncertainty affect comparison search. Let $x_i$ be the rank of the entry at position $i$. Their shared measure is

$$
V(A)=\frac{1}{2}\sum_{i=1}^{n}(x_i-i)^2.
$$

## Papers

| Paper | Main result | HTML | PDF | LaTeX |
| --- | --- | --- | --- | --- |
| **Disorder Potential and the Cost of Search** (version 2) | With only $V(A)\le E$, one search has tight worst-case cost $\Theta(\log n+\min\{n,\sqrt E\})$. The paper also shows why the location of disorder matters beyond its total potential. | [HTML](disorder_potential_search_note_v2.html) | [PDF](disorder_potential_search_note_v2.pdf) | [Source](disorder_potential_search_note_v2.tex) |
| **Search Under a Disorder Budget** | For $q$ searches on one fixed array, preprocessing yields $T_q^*(n,E)=O(q\log n+\min\{qR_E,n\log(R_E+1)\})$, where $R_E=1+D_E$ and $D_E$ is the displacement bound implied by $E$. The note also explains verified learned certificates. | [HTML](search-under-a-disorder-budget/search_under_a_disorder_budget.html) | [PDF](search-under-a-disorder-budget/search_under_a_disorder_budget.pdf) | [Source](search-under-a-disorder-budget/search_under_a_disorder_budget.tex) |
| **Search Under Disorder and Query Entropy** | For a known query-rank law $w$, a sorted index built from the disorder promise gives $O(n\log(R_E+1)+q(H(w)+1))$ expected comparisons; the target-entropy term is necessary up to constants. | [HTML](search-under-query-entropy/search_under_query_entropy.html) | [PDF](search-under-query-entropy/search_under_query_entropy.pdf) | [Source](search-under-query-entropy/search_under_query_entropy.tex) |

The [archived original draft](archived-draft-materials/disorder_potential_search_note.pdf) and its [LaTeX source](archived-draft-materials/disorder_potential_search_note.tex) remain available for historical context.

## Experiment

[Potential across random permutations](experiments/n9-potential-distribution/README.md) shows the exact $n=9$ histogram and explains the distribution and search-bound implications for general $n$.

## Models

The first paper gives the search algorithm a numerical promise $V(A)\le E$, with no auxiliary index or preprocessing transcript. The extension allows preprocessing comparisons among array keys and an $O(n)$-word index, charging their cost along with the later target comparisons. The query-entropy extension adds a known distribution over target ranks and gaps, and counts the comparisons needed to build the index before measuring expected search cost.

The website is the root [index.html](index.html), published through GitHub Pages from master. The mobile-friendly HTML papers are generated from the LaTeX sources by [build_paper_html.py](scripts/build_paper_html.py) (requires Pandoc and Beautiful Soup).
