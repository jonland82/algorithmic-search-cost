# Disorder Potential and the Cost of Search

**Jonathan R. Landers** · October 2026

This note studies comparison search in an array whose squared rank-displacement potential is bounded. It proves a tight worst-case search bound, then shows why the location of disorder matters beyond its total amount.

For an array with rank word \(x=(x_1,\ldots,x_n)\), the potential is

\[
V(A)=\frac12\sum_{i=1}^{n}(x_i-i)^2.
\]

Given only the promise \(V(A)\leq E\), the optimal worst-case number of search queries is

\[
\Theta\!\left(\log n+\min\{n,\sqrt E\}\right).
\]

The note also constructs two known input families with the same maximum potential but different optimal search costs: \(\Theta(\log n+\sqrt E)\) and \(\Theta(\log n)\). A potential balance law accounts for disorder removed during preprocessing; a useful search guarantee also depends on what structural information preprocessing supplies.

## Read the note

| Version | PDF | LaTeX |
| --- | --- | --- |
| Historical context and expanded references | [Version 2 PDF](disorder_potential_search_note_v2.pdf) | [Version 2 source](disorder_potential_search_note_v2.tex) |
| Original note | [Original PDF](archived-draft-materials/disorder_potential_search_note.pdf) | [Original source](archived-draft-materials/disorder_potential_search_note.tex) |

Version 2 preserves the original results and proofs while weaving in the history of rank distances, comparison sorting, adaptive search, and related work through 2026. The LaTeX source is self-contained and uses a `thebibliography` environment.

## Scope

The search model uses deterministic index queries that compare a target with one array entry and allows the target to be absent. The search algorithm receives a numerical potential promise, with no auxiliary index or preprocessing transcript. Preprocessing cost is accounted for separately.
