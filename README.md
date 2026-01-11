# albert
Feature extraction from QM outputs for ML workflows

`pip install git+https://github.com/jyothishjoy/albert.git`

`albert extract /path/to/JOBS_DIR --out albert_features.csv --nprocs 16`

If a job folder is missing required files or cannot be parsed, ALBERT will skip that folder and continue processing the remaining jobs. 

If a job folder fails (missing inputs or parsing error), ALBERT prints a WARNING: ...; skipped message to stdout and continues with the next folder
