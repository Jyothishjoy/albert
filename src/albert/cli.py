import argparse
from pathlib import Path

from albert.extract import run_extract


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(prog="albert")
    subparsers = parser.add_subparsers(dest="command", required=True)

    p_extract = subparsers.add_parser("extract", help="Extract features from many job subfolders.")
    p_extract.add_argument("jobs_dir", type=Path, help="Directory containing job subfolders.")
    p_extract.add_argument("--out", default="albert_features.csv", help="Output CSV path.")
    p_extract.add_argument("--nprocs", type=int, default=1, help="Number of worker processes.")
    p_extract.set_defaults(func=lambda args: run_extract(args.jobs_dir, Path(args.out), args.nprocs))

    args = parser.parse_args(argv)
    return int(args.func(args))


if __name__ == "__main__":
    raise SystemExit(main())

