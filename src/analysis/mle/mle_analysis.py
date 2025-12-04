"""
MLE Analysis: Runs Maximum Likelihood Estimation on phylogenetic trees.

Uses the unified batch processor with the MLE estimator class.

Author: Santosh Desai <santoshdesai12@hotmail.com>
"""

import sys
from pathlib import Path

# Setup paths before any imports
# Get the analysis directory (parent of this file's parent)
_script_file = Path(__file__).resolve()
_analysis_dir = _script_file.parent.parent
_project_root = _analysis_dir.parent.parent

# Add to Python path if not already there
if str(_analysis_dir) not in sys.path:
    sys.path.insert(0, str(_analysis_dir))
if str(_project_root) not in sys.path:
    sys.path.insert(0, str(_project_root))

# Now we can import
from utils.common import setup_analysis_environment
setup_analysis_environment(__file__)

# Now we can import from config and other modules
from config import MLE_OUTPUT_DIR, DEFAULT_SAMPLING_PROBA
from utils.batch_processor import process_trees_batch
from mle.mle_birth_death import BirthDeathMLE


def mle_estimator(tree_file: str, sampling_prob: float):
    """Estimate parameters using MLE."""
    estimator = BirthDeathMLE(tree_file, sampling_prob=sampling_prob)
    result = estimator.estimate_bd()
    
    if result['success']:
        return {
            'lambda': result['lambda'],
            'mu': result['mu'],
            'R0': result['R_naught'],
            'infectious_period': result['Infectious_period'],
            'log_likelihood': result['log_likelihood'],
            'n_iterations': result['n_iterations'],
        }
    else:
        return {
            'lambda': None,
            'mu': None,
            'R0': None,
            'infectious_period': None,
            'log_likelihood': None,
            'n_iterations': None,
        }


if __name__ == "__main__":
    import argparse
    import multiprocessing
    
    parser = argparse.ArgumentParser(description="Run MLE analysis")
    parser.add_argument(
        "--n-jobs",
        type=int,
        default=1,
        help=(
            "Number of parallel jobs (1 = sequential, "
            "N > 1 = parallel with N workers)"
        )
    )
    parser.add_argument(
        "--clean",
        action="store_true",
        help="Delete existing results before running (default: preserve and only run missing)"
    )
    args = parser.parse_args()
    
    print("Note: MLE works on all tip sizes (no minimum requirement)")
    
    process_trees_batch(
        estimator_func=mle_estimator,
        output_dir=MLE_OUTPUT_DIR,
        method_name="MLE",
        sampling_prob=DEFAULT_SAMPLING_PROBA,
        n_jobs=args.n_jobs,
        clean_output=args.clean,
    )
