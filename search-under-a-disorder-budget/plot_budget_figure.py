"""Plot the n=9 potential distribution against the search saturation budget."""

from csv import DictReader
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter


HERE = Path(__file__).resolve().parent
COUNTS = HERE.parent / "experiments" / "n9-potential-distribution" / "potential_counts.csv"
N = 9
SATURATION = N * (N - 1) // 2


def main() -> None:
    with COUNTS.open(newline="", encoding="utf-8") as source:
        rows = list(DictReader(source))
    potentials = [int(row["potential"]) for row in rows]
    counts = [int(row["count"]) for row in rows]
    total = sum(counts)
    tail = sum(count for potential, count in zip(potentials, counts) if potential < SATURATION)
    mean = sum(potential * count for potential, count in zip(potentials, counts)) / total
    assert len(rows) == 121 and total == 362_880
    assert SATURATION == 36 and tail == 48_913 and mean == 60

    fig, ax = plt.subplots(figsize=(6.45, 2.35), dpi=180)
    colors = ["#38647a" if potential < SATURATION else "#c0c5cb" for potential in potentials]
    ax.bar(potentials, counts, width=0.9, color=colors, linewidth=0)
    ax.axvline(SATURATION - 0.5, color="#18465d", linewidth=1.3)
    ax.axvline(mean, color="#6b747d", linewidth=1.1, linestyle=(0, (3, 3)))
    ax.text(4, 7150, f"{tail / total:.1%} have V < {SATURATION}",
            color="#18465d", fontsize=8.8, weight="semibold", va="top")
    ax.text(38, 6250, r"$E_{\mathrm{sat}}=36$", color="#18465d", fontsize=8.5, va="top")
    ax.text(62, 7150, "mean = 60", color="#555d65", fontsize=8.5, va="top")
    ax.set_xlim(-1, 121)
    ax.set_ylim(0, 7600)
    ax.set_xticks([0, 20, 36, 60, 80, 100, 120])
    ax.set_xlabel(r"potential $V(A)$", fontsize=9)
    ax.set_ylabel("permutations", fontsize=9)
    ax.yaxis.set_major_formatter(FuncFormatter(lambda value, _: f"{value / 1000:g}k" if value else "0"))
    ax.tick_params(labelsize=8, length=3)
    ax.grid(axis="y", color="#e2e5e8", linewidth=0.6)
    ax.set_axisbelow(True)
    ax.spines[["top", "right"]].set_visible(False)
    fig.tight_layout(pad=0.45)
    fig.savefig(HERE / "potential_budget_n9.png", dpi=300, facecolor="white")
    plt.close(fig)
    print(f"wrote potential_budget_n9.png; V<{SATURATION}: {tail}/{total} ({tail / total:.3%})")


if __name__ == "__main__":
    main()
