"""
PhyloDeep Analysis: Runs PhyloDeep deep learning model on phylogenetic trees.

Uses the unified batch processor with PhyloDeep library.

Author: Santosh Desai <santoshdesai12@hotmail.com>
"""

import sys
from pathlib import Path
import numpy as np
import pandas as pd

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
from config import PHYLODEEP_OUTPUT_DIR, DEFAULT_SAMPLING_PROBA

from utils.batch_processor import process_trees_batch

# PhyloDeep imports
from phylodeep import BD, FULL
from phylodeep.paramdeep import paramdeep


def phylodeep_estimator(tree_file: str, sampling_prob: float):
    """Estimate parameters using PhyloDeep."""
    try:
        phylodeep_params = paramdeep(
            tree_file,
            sampling_prob,
            model=BD,
            vector_representation=FULL,
            ci_computation=False
        )
        
        # Check if we got valid results
        if phylodeep_params is None or phylodeep_params.empty:
            return {
                'lambda': np.nan,
                'mu': np.nan,
                'R0': np.nan,
                'infectious_period': np.nan,
                'error': 'PhyloDeep returned empty results'
            }
        
        result = {}
        # Map PhyloDeep column names to standard names
        for col in phylodeep_params.columns:
            value = phylodeep_params[col].iloc[0]
            
            # Skip NaN values but keep them if they're the only value
            if pd.isna(value):
                continue
            
            if col == 'R_naught' or col == 'R0':
                result['R0'] = float(value)
            elif col == 'Infectious_period':
                result['infectious_period'] = float(value)
            elif col == 'la' or col == 'lambda':
                result['lambda'] = float(value)
            elif col == 'psi' or col == 'mu':
                result['mu'] = float(value)
            else:
                result[f'phylodeep_{col}'] = float(value)
        
        # Compute lambda and mu from R0 and infectious_period if not
        # directly available
        # R0 = lambda / mu, and infectious_period = 1 / mu
        # Therefore: mu = 1 / infectious_period, and
        # lambda = R0 * mu = R0 / infectious_period
        if 'R0' in result and 'infectious_period' in result:
            r0_val = result['R0']
            ip_val = result['infectious_period']
            
            # Compute mu from infectious_period if not already present
            if 'mu' not in result or pd.isna(result.get('mu')):
                if not pd.isna(ip_val) and ip_val > 0:
                    result['mu'] = float(1.0 / ip_val)
            
            # Compute lambda from R0 and mu if not already present
            if 'lambda' not in result or pd.isna(result.get('lambda')):
                mu_val = result.get('mu')
                if not pd.isna(r0_val) and not pd.isna(mu_val) and mu_val > 0:
                    result['lambda'] = float(r0_val * mu_val)
        elif (not pd.isna(r0_val) and not pd.isna(ip_val) and
              ip_val > 0):
                    # Alternative: lambda = R0 / infectious_period
                    result['lambda'] = float(r0_val / ip_val)
        
        # Ensure standard columns exist (use NaN if missing)
        if 'lambda' not in result:
            result['lambda'] = np.nan
        if 'mu' not in result:
            result['mu'] = np.nan
        if 'R0' not in result:
            result['R0'] = np.nan
        if 'infectious_period' not in result:
            result['infectious_period'] = np.nan
        
        # Mark as successful if we have at least one valid value
        if not all(pd.isna(v) for k, v in result.items() if k in ['lambda',
            'mu', 'R0', 'infectious_period']):
            result['success'] = True
        
        return result
    except Exception as e:
        # PhyloDeep estimation failed - return error info
        error_msg = str(e)
        if len(error_msg) > 200:
            error_msg = error_msg[:200]
        return {
            'lambda': np.nan,
            'mu': np.nan,
            'R0': np.nan,
            'infectious_period': np.nan,
            'error': f'PhyloDeep error: {error_msg}',
            'success': False
        }


if __name__ == "__main__":
    import argparse
    from config import MIN_TIP_SIZE
    
    parser = argparse.ArgumentParser(description="Run PhyloDeep analysis")
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
    
    # PhyloDeep requires tip size >= MIN_TIP_SIZE (default 50)
    # Filter target_tip_sizes to only include >= MIN_TIP_SIZE
    from utils.batch_processor import load_tree_metadata
    df_params, _ = load_tree_metadata(None)
    available_sizes = sorted(df_params['tips'].unique())
    target_tip_sizes = [s for s in available_sizes if s >= MIN_TIP_SIZE]
    
    if not target_tip_sizes:
        print(f"No trees with tip size >= {MIN_TIP_SIZE} found!")
        print(f"PhyloDeep requires minimum {MIN_TIP_SIZE} tips.")
    else:
        process_trees_batch(
            estimator_func=phylodeep_estimator,
            output_dir=PHYLODEEP_OUTPUT_DIR,
            method_name="PhyloDeep",
            target_tip_sizes=target_tip_sizes,
            sampling_prob=DEFAULT_SAMPLING_PROBA,
            n_jobs=args.n_jobs,
            clean_output=args.clean,
        )
