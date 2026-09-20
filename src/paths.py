"""Single source of truth for every path in this repository.

Nothing here is machine-specific. ``REPO_ROOT`` is derived from the location of
this file, so a fresh clone works with no edits by anyone -- that is the entire
point of the module. Do not hardcode an absolute path anywhere else in the repo.

Environment variables are an escape hatch, not the normal path. Set one only
when a tree genuinely lives outside the repo (results on an external drive, data
on cluster scratch):

    MPC_ROOT           repo root           default: the parent of src/
    MPC_DATA_ROOT      the data/ tree      default: $MPC_ROOT/data
    MPC_RESULTS_ROOT   the results/ tree   default: $MPC_ROOT/results
    MPC_FIGS_ROOT      the figs/ tree      default: $MPC_ROOT/figs

Every constant and helper returns ``str``, never ``pathlib.Path``, so they drop
straight into the f-string and ``+`` path building used throughout the codebase.

From a script in experiments/::

    import os, sys
    sys.path.insert(0, os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "src"))
    from paths import i24_data, fig

From a notebook in experiments/::

    import sys; sys.path.append("../src")
    from paths import i24_data, fig

Run ``python src/paths.py`` to print every resolved path and whether it exists.
"""

import os
from pathlib import Path

__all__ = [
    "REPO_ROOT", "DATA_ROOT", "RESULTS_ROOT", "FIGS_ROOT", "SRC_ROOT",
    "I24_DATA", "I24_RESULTS", "SYNTHETIC_RESULTS", "DEFAULT_CALIBRATION",
    "synthetic_results",
    "fig", "ensure_dir", "i24_dates", "describe",
]


def _resolve(env_var, default):
    """Absolute path from ``$env_var`` if it is set and non-empty, else default."""
    return os.path.abspath(os.environ.get(env_var) or default)


# ── Roots ────────────────────────────────────────────────────────────────────

REPO_ROOT = Path(_resolve(
    "MPC_ROOT", os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
))
DATA_ROOT    = Path(_resolve("MPC_DATA_ROOT",    REPO_ROOT / "data"))
RESULTS_ROOT = Path(_resolve("MPC_RESULTS_ROOT", REPO_ROOT / "results"))
FIGS_ROOT    = Path(_resolve("MPC_FIGS_ROOT",    REPO_ROOT / "figs"))
SRC_ROOT     = REPO_ROOT / "src"

I24_DATA          = DATA_ROOT / "i24"
I24_RESULTS       = RESULTS_ROOT / "i24"
SYNTHETIC_RESULTS = RESULTS_ROOT / "synthetic_10km"

#: The calibration every figure in the paper is built from.
DEFAULT_CALIBRATION = "calibration_static/fixed_ramping"


# ── Helpers ──────────────────────────────────────────────────────────────────

def ensure_dir(path):
    """Create ``path`` if missing and return it, so it can be used inline."""
    os.makedirs(path, exist_ok=True)
    return path

def synthetic_results(*parts):
    """Solved policies for the synthetic 10 km bottleneck.

        synthetic_results("demand")              -> <results>/synthetic_10km/demand
        synthetic_results("holdlength", "x.csv") -> <results>/synthetic_10km/holdlength/x.csv
    """
    return os.path.join(SYNTHETIC_RESULTS, *parts)


def fig(name):
    """Absolute path for a figure, creating ``figs/`` if it does not exist.

    The directory is created here so ``plt.savefig(fig("x.png"))`` cannot fail on
    a fresh clone that has no ``figs/`` yet.
    """
    ensure_dir(FIGS_ROOT)
    return os.path.join(FIGS_ROOT, name)


def i24_dates():
    """Sorted ``["11_21", ...]`` for every date directory actually present."""
    if not os.path.isdir(I24_DATA):
        return []
    return sorted(
        d[len("i24_"):] for d in os.listdir(I24_DATA)
        if d.startswith("i24_") and os.path.isdir(os.path.join(I24_DATA, d))
    )


def describe():
    """Print every resolved root and whether it exists. Run this first when
    something cannot find its data."""
    overrides = {v: os.environ[v] for v in
                 ("MPC_ROOT", "MPC_DATA_ROOT", "MPC_RESULTS_ROOT", "MPC_FIGS_ROOT")
                 if os.environ.get(v)}
    print("Resolved paths\n" + "-" * 62)
    for name in ("REPO_ROOT", "DATA_ROOT", "RESULTS_ROOT", "FIGS_ROOT",
                 "I24_DATA", "I24_RESULTS", "SYNTHETIC_RESULTS"):
        path = globals()[name]
        print(f"  {'OK ' if os.path.exists(path) else 'MISSING'}  {name:<18} {path}")
    print("-" * 62)
    print(f"  environment overrides: {overrides or 'none (all derived from this file)'}")
    dates = i24_dates()
    print(f"  I-24 dates available:  {', '.join(dates) if dates else 'none'}")


if __name__ == "__main__":
    describe()
