# Density Regression for Phylogenetic Parameters

This project compares density regression methods with PhyloDeep's existing point estimation approach for phylogenetic parameter inference.

## Overview

**Goal**: Evaluate how effectively density regression can learn and reproduce results compared to PhyloDeep's existing methods (point estimates + bootstrap CIs).

**Methods**:
- **Mixture Density Networks (MDN)** - Python/TensorFlow
- **Gaussian Process Regression** - Python/scikit-learn  
- **Kernel Density Estimation** - Python/scipy
- **BART (Bayesian Additive Regression Trees)** - R

## Quick Start

### Jupyter Notebook (Recommended)

```bash
# Open the interactive notebook
jupyter notebook density_regression_analysis.ipynb

# Or use JupyterLab
jupyter lab density_regression_analysis.ipynb
```

The notebook includes:
- Table of contents with section navigation
- PhyloDeep sample data integration
- Nextstrain data loading (optional)
- Interactive visualization
- Step-by-step analysis

### Python Script

```bash
# Run main comparison script
python3 main.py

# This will:
# 1. Generate or load phylogenetic data
# 2. Apply density regression methods
# 3. Compare with PhyloDeep (if available)
# 4. Evaluate using proper scoring rules (CRPS)
```

## Installation

### Quick Setup

```bash
# Run setup script
./setup_env.sh

# Or manually:
python3 -m venv venv_phylodeep
source venv_phylodeep/bin/activate
pip install numpy scipy scikit-learn pandas matplotlib seaborn
```

### PhyloDeep Installation

**⚠ Important**: PhyloDeep requires Python 3.8-3.11 (Python 3.13 has compatibility issues)

**Option 1: Conda (Recommended)**
```bash
conda create -n phylodeep_env python=3.11
conda activate phylodeep_env
conda install -c bioconda phylodeep
```

**Option 2: Python 3.11 Virtual Environment**
```bash
# Install Python 3.11 (macOS)
brew install python@3.11

# Create venv with Python 3.11
python3.11 -m venv venv_phylodeep
source venv_phylodeep/bin/activate
pip install phylodeep
```

**Note**: The notebook works with synthetic data even if PhyloDeep is not installed.

### Current Installation Status

✅ **Installed**:
- numpy, scipy, scikit-learn
- pandas, matplotlib, seaborn

⚠️ **Requires Python 3.8-3.11**:
- phylodeep
- ete3 (dependency of phylodeep)

See installation section above for detailed options.

## What It Does

1. **Data**: Uses PhyloDeep sample data (HIV Zurich tree) or generates synthetic data
2. **Feature Extraction**: Uses PhyloDeep's encoding (summary statistics or full tree representation)
3. **Density Regression**: Fits models that output full probability distributions
4. **Evaluation**: Uses Continuous Ranked Probability Score (CRPS) - a proper scoring rule
5. **Comparison**: Compares with PhyloDeep's point estimates and bootstrap CIs

## Key Advantages of Density Regression

- ✓ **Full Distributions**: Provides complete posterior distributions, not just point estimates
- ✓ **Uncertainty Quantification**: Properly quantifies epistemic and aleatoric uncertainty
- ✓ **Parameter Correlations**: Can model dependencies between parameters
- ✓ **Proper Evaluation**: Uses proper scoring rules (CRPS) instead of just MAE/RMSE

## Files

- `density_regression_analysis.ipynb` - **Main Jupyter notebook** with table of contents and full analysis
- `main.py` - Python script version (same functionality)
- `density_regression_R.R` - R implementation with GP and BART
- `requirements.txt` - Python dependencies

## Results

The script outputs:
- CRPS (Continuous Ranked Probability Score) per parameter
- MAE (Mean Absolute Error) comparison
- Visualization of predicted distributions (if matplotlib available)

## Next Steps

1. Install PhyloDeep: `pip install phylodeep`
2. Use real phylogenetic data (HIV Zurich tree or other datasets)
3. Compare with PhyloDeep's bootstrap CI method
4. Evaluate on multiple disease datasets
