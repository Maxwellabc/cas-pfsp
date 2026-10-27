# Carbon-aware permutation flow-shop scheduling: reproducibility artifact

Anonymous research artifact, release **v232** (27 October 2026). This repository contains algorithm source, the 30 exposed benchmark instances, and retained numerical data and plotting code. Research author names, affiliations, contact details and local home-directory paths are omitted. Third-party licensing and provenance are retained.

## Files and quick start

Download or clone this repository, then use Python 3.11 or later:

```sh
python3 reproduce.py --check
python3 reproduce.py --summary
```

These commands verify and extract the three archives into a new `work/cas/` directory, check every frozen source/input hash, and independently recompute the reported cohort C mean gains with exact rational arithmetic. They need only the Python standard library and perform **no optimizer runs**. Existing extracted files must match the published bytes.

- `cas_source_v232.zip`: all 96 frozen Python source modules, supporting scripts, original protocol, environment record and constructed interface fixtures. Directory paths inside the archive are preserved.
- `cas_instances_v232.zip`: exactly the 30 exposed indices 1 to 5 across six families. The other 270 input contents are excluded. The pinned upstream input manifest includes direct download URLs and SHA256 values.
- `cas_analysis_v232.zip`: 720 audited cohort C outcome records, exact comparisons, separate-cohort summaries, all 50,000 bootstrap draws and plotting code. Individual optimizer transcripts containing millions of registrations are not included in this compact release. Hash/summary checking does not replay those full physical audits.

The archives are immutable versioned snapshots so that browser publication does not change any frozen file. Changes are published as new named archives and repository commits. The local research archive tracks paper, code and instances as ordinary files with separate Git tags.

## Figures

Use a separate environment with NumPy 2.3.5 and Matplotlib 3.10.7:

```sh
python3 reproduce.py --figures
```

This redraws six statistical figures from frozen data, including a family profile and grouped signed ablation bars. There are no heatmaps. It does not regenerate or tune optimizer results. The remaining historical plots are available in the paper source delivery.

## Running an algorithm

Use an experiment environment with NumPy 2.2.6 and OR-Tools 9.15.6755 (the retained Linux ARM64 runs used Python 3.10.19). Import all dependencies before the paid root. For example:

```sh
python3 reproduce.py --run-one serial_rows CAS-PFSP-M5T1_1.cas --seed 2026102903 --budget 5
```

Supported methods are `serial_rows`, `no_serial`, `no_pair`, `lexicographic`, `fast_wait`, `local_wait_raw`, `adaptive_cp_alns` and `lg_ucb26`. Re-execution results go to a new file in `work/`; they never replace frozen data. Wall-clock stopping and a nonexclusive host make bit-identical optimizer outcomes inappropriate to promise. Use the frozen protocol for worker quotas, concurrency, call order, timing and eligibility rules. This entry point is a single-run convenience tool, not a reconstruction of the historical three-worker experiment launcher.

## Interpretation and provenance

The optimizer is unchanged v197r1. Cohorts A, B and C remain separate; all 30 inputs are exposed development instances. Published-mechanism comparators are explicit adaptations, not complete reproductions of their original algorithms. Mixed paired-response and priority results are retained. No unseen-instance or universal superiority claim is made.

Instances originate from `ugent-isye/MA-DRL-CAS-PFSP`, commit `c8fc905f4cbe5f38189fedf8d0c52f1442dc0c9e`; their original GPL version 3 license is included verbatim. No project-author identity is added, no third-party license is removed, and no new blanket license is assigned to this collection. See `RIGHTS.md` for the distinction between original source and upstream data.
