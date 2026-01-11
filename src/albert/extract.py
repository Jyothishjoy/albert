from __future__ import annotations

import os
import csv
import multiprocessing as mp
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Optional

from tqdm import tqdm

# Import your existing extractors (same ones you use today)
from albert.bde_calculator import (
    calculate_frozen_scfbde_from_directory,
    calculate_relaxed_scfbde_from_directory,
    calculate_relaxred_ZPEbde_from_directory,
    calculate_frag_relax_energy,
)
from albert.gaussian_extractor import (
    extract_bndlgth_freq_frc_const,
    extract_Radical_Attch_Energy,
    somo_lumo_spin_Mulliken_dipole,
)
from albert.nbo_pop_charge import extract_NBO
from albert.conceptual_dft import extract_conceptual_dft
from albert.fukui_functions import extract_Fukui_Fun
from albert.orbital_data import extract_complex_orbital_data
from albert.Aaron_features import (
    get_lig_atom_indicies,
    get_sterimol,
    get_buried_volume,
    get_cone_angle,
    get_ligand_solid_angle,
)
from albert.MORFEUS_features import get_sasa, get_dispersion_int, get_local_force_constant


@dataclass(frozen=True)
class JobResult:
    job_name: str
    features: dict[str, Any]


def _immediate_subdirs(jobs_dir: Path) -> list[Path]:
    return sorted([p for p in jobs_dir.iterdir() if p.is_dir()])


def _warn(msg: str) -> None:
    print(f"WARNING: {msg}")  # stdout, as requested


def _extract_one(job_dir: Path) -> Optional[JobResult]:
    try:
        # Put *your* minimal file checks here based on albert.file_names
        # If missing: _warn(...); return None

        subdir = str(job_dir)

        row: dict[str, Any] = {"job_dir": subdir, "job_name": job_dir.name}

        # --- Example: call your existing feature functions (keep same logic as current script) ---
        row.update(extract_bndlgth_freq_frc_const(subdir) or {})
        row.update(extract_Radical_Attch_Energy(subdir) or {})
        row.update(somo_lumo_spin_Mulliken_dipole(subdir) or {})

        row.update(extract_NBO(subdir) or {})
        row.update(extract_conceptual_dft(subdir) or {})
        row.update(extract_Fukui_Fun(subdir) or {})
        row.update(extract_complex_orbital_data(subdir) or {})

        # AaronTools-based
        lig_atoms = get_lig_atom_indicies(subdir)
        row.update(get_sterimol(subdir, lig_atoms) or {})
        row.update(get_buried_volume(subdir, lig_atoms) or {})
        row.update(get_cone_angle(subdir, lig_atoms) or {})
        row.update(get_ligand_solid_angle(subdir, lig_atoms) or {})

        # MORFEUS-based
        row.update(get_sasa(subdir) or {})
        row.update(get_dispersion_int(subdir) or {})
        row.update(get_local_force_constant(subdir) or {})

        # BDE-related (adjust to your current row schema)
        row.update(calculate_frozen_scfbde_from_directory(subdir) or {})
        row.update(calculate_relaxed_scfbde_from_directory(subdir) or {})
        row.update(calculate_relaxred_ZPEbde_from_directory(subdir) or {})
        row.update(calculate_frag_relax_energy(subdir) or {})

        return JobResult(job_dir.name, row)

    except Exception as e:
        _warn(f"{job_dir.name}: {type(e).__name__}: {e}; skipped")
        return None


def _write_csv(rows: list[dict[str, Any]], out_path: Path) -> None:
    out_path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        _warn(f"No jobs produced output; CSV not written: {out_path}")
        return

    # stable header union across rows
    fieldnames = sorted({k for r in rows for k in r.keys()})

    with out_path.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames)
        w.writeheader()
        w.writerows(rows)


def run_extract(jobs_dir: Path, out_csv: Path, nprocs: int) -> int:
    jobs_dir = jobs_dir.expanduser().resolve()
    subdirs = _immediate_subdirs(jobs_dir)

    if not subdirs:
        _warn(f"No subfolders found in {jobs_dir}")
        return 2

    if nprocs <= 1:
        results = []
        for d in tqdm(subdirs, desc="ALBERT extract"):
            r = _extract_one(d)
            if r is not None:
                results.append(r.features)
    else:
        with mp.Pool(processes=nprocs) as pool:
            it = pool.imap_unordered(_extract_one, subdirs)
            results = [r.features for r in tqdm(it, total=len(subdirs), desc="ALBERT extract") if r is not None]

    _write_csv(results, out_csv)
    return 0

