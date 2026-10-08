"""Enumerate the exact disorder-potential distribution for nine distinct keys."""

from collections import Counter
from csv import writer
from itertools import permutations
from math import factorial
from pathlib import Path
from random import Random

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.ticker import StrMethodFormatter


N = 9
SEED = 20261008
OUT = Path(__file__).resolve().parent


def main() -> None:
    values = Random(SEED).sample(range(10, 100), N)
    rank = {value: i for i, value in enumerate(sorted(values), start=1)}
    counts: Counter[int] = Counter()
    examples: dict[int, tuple[int, ...]] = {}

    for ordering in permutations(values):
        twice_potential = sum(
            (rank[value] - i) ** 2 for i, value in enumerate(ordering, start=1)
        )
        assert twice_potential % 2 == 0
        potential = twice_potential // 2
        counts[potential] += 1
        examples.setdefault(potential, ordering)

    maximum = N * (N * N - 1) // 6
    total = factorial(N)
    assert sum(counts.values()) == total
    assert counts[0] == counts[maximum] == 1
    assert all(counts[v] == counts[maximum - v] for v in range(maximum + 1))

    potentials = list(range(maximum + 1))
    frequencies = [counts[v] for v in potentials]
    peak = max(frequencies)
    modes = [v for v in potentials if counts[v] == peak]
    mean = sum(v * counts[v] for v in potentials) / total

    with (OUT / "potential_counts.csv").open("w", newline="", encoding="utf-8") as file:
        rows = writer(file)
        rows.writerow(("potential", "count", "fraction", "example_permutation"))
        for v in potentials:
            rows.writerow(
                (v, counts[v], f"{counts[v] / total:.8f}", " ".join(map(str, examples[v])))
            )

    fig, ax = plt.subplots(figsize=(11.6, 5.6), dpi=200)
    colors = ["#9b3d35" if v in modes else "#343b45" for v in potentials]
    ax.bar(potentials, frequencies, width=0.88, color=colors, linewidth=0)
    ax.axvline(mean, color="#8e959c", linestyle=(0, (4, 4)), linewidth=1.2,
               label=f"mean = {mean:g}")
    ax.set_xlim(-1, maximum + 1)
    ax.set_ylim(0, peak * 1.17)
    ax.set_xticks(range(0, maximum + 1, 10))
    ax.yaxis.set_major_formatter(StrMethodFormatter("{x:,.0f}"))
    ax.grid(axis="y", color="#d9dde1", linewidth=0.7)
    ax.set_axisbelow(True)
    ax.spines[["top", "right"]].set_visible(False)
    ax.set_title("Exact disorder-potential distribution for n = 9",
                 loc="left", fontsize=17, fontweight="semibold", pad=17)
    ax.set_xlabel(
        r"potential $V(A)=\frac{1}{2}\sum_{i=1}^{9}(x_i-i)^2$",
        fontsize=11,
        labelpad=10,
    )
    ax.set_ylabel("number of permutations", fontsize=11, labelpad=10)
    ax.text(
        0.02, 0.96,
        f"modes: V = {modes[0]} and {modes[1]}  ({peak:,} each)",
        transform=ax.transAxes,
        va="top",
        fontsize=10,
        color="#9b3d35",
    )
    ax.legend(loc="upper right", frameon=False, fontsize=10)
    fig.text(
        0.105, 0.015,
        f"all {total:,} permutations of {values}; the frequencies depend only on ranks, not the sampled integers.",
        color="#555b61",
        fontsize=9,
    )
    fig.subplots_adjust(left=0.105, right=0.98, top=0.88, bottom=0.19)
    fig.savefig(OUT / "potential_histogram.png", dpi=220, facecolor="white")
    fig.savefig(OUT / "potential_histogram.pdf", facecolor="white")
    plt.close(fig)

    print(f"seeded list: {values}")
    print(f"permutations: {total:,}; potential values: {len(counts)} (0 through {maximum})")
    print(f"mean: {mean:g}; modes: {modes} ({peak:,} permutations each)")
    for v in modes:
        print(f"example with V={v}: {examples[v]}")


if __name__ == "__main__":
    main()