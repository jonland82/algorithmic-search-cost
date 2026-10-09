# Disorder Potential and the Cost of Search

**Jonathan R. Landers · October 2026**

[Read the website](https://jonland82.github.io/algorithmic-search-cost/) · [Browse the repository](https://github.com/jonland82/algorithmic-search-cost)

Two papers and a companion note study how array disorder affects comparison search. A third note on query entropy is retained as work in progress. Let $x_i$ be the rank of the entry at position $i$. Their shared measure is

$$
V(A)=\frac{1}{2}\sum_{i=1}^{n}(x_i-i)^2.
$$

## Papers

| Paper | Main result | HTML | PDF | LaTeX |
| --- | --- | --- | --- | --- |
| **Disorder Potential and the Cost of Search** (version 2) | With only $V(A)\le E$, one search has tight worst-case cost $\Theta(\log n+\min\{n,\sqrt E\})$. The paper also shows why the location of disorder matters beyond its total potential. | [HTML](disorder_potential_search_note_v2.html) | [PDF](disorder_potential_search_note_v2.pdf) | [Source](disorder_potential_search_note_v2.tex) |
| **Search Under a Disorder Budget** | For $q$ searches on one fixed array, preprocessing yields $T_q^*(n,E)=O(q\log n+\min\{qR_E,n\log(R_E+1)\})$, where $R_E=1+D_E$ and $D_E$ is the displacement bound implied by $E$. The note also explains verified learned certificates. | [HTML](search-under-a-disorder-budget/search_under_a_disorder_budget.html) | [PDF](search-under-a-disorder-budget/search_under_a_disorder_budget.pdf) | [Source](search-under-a-disorder-budget/search_under_a_disorder_budget.tex) |

The [archived original draft](archived-draft-materials/disorder_potential_search_note.pdf) and its [LaTeX source](archived-draft-materials/disorder_potential_search_note.tex) remain available for historical context.

## Companion note

**Potential Across Random Permutations** puts the first paper's budget in context for uniformly shuffled arrays and connects its limit to the repeated-search bound in paper 2. Read the [HTML](experiments/n9-potential-distribution/potential_across_random_permutations.html), [PDF](experiments/n9-potential-distribution/potential_across_random_permutations.pdf), or [LaTeX source](experiments/n9-potential-distribution/potential_across_random_permutations.tex). The [experiment README](experiments/n9-potential-distribution/README.md) contains the exact $n=9$ counts, plot, and reproduction script.

## Work in progress

**Search Under Disorder and Query Entropy** studies a known distribution over target ranks and gaps. It remains in the repository for further development and is not listed on the website: [HTML](search-under-query-entropy/search_under_query_entropy.html), [PDF](search-under-query-entropy/search_under_query_entropy.pdf), [LaTeX source](search-under-query-entropy/search_under_query_entropy.tex).

## Models

The first paper gives the search algorithm a numerical promise $V(A)\le E$, with no auxiliary index or preprocessing transcript. The second paper allows preprocessing comparisons among array keys and an $O(n)$-word index, charging their cost along with later target comparisons. The companion note uses a random-array model to show when a potential budget can narrow the search window; an individual input still needs a supplied or certified promise. The work-in-progress note introduces a separate distribution over target ranks and gaps.

The website is the root [index.html](index.html), published through GitHub Pages from master. The mobile-friendly HTML editions are generated from the LaTeX sources by [build_paper_html.py](scripts/build_paper_html.py) (requires Pandoc and Beautiful Soup).
