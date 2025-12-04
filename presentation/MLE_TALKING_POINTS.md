# MLE Talking Points (5 Minutes)

## Slide 1: Title Slide (30 seconds)
- **Introduction**: "Today I'll present our Maximum Likelihood Estimation approach for birth-death tree parameter estimation"
- **Context**: "We're comparing MLE with PhyloDeep to assess statistical efficiency"
- **Key Question**: "Can a classical statistical method compete with deep learning on this task?"

---

## Slide 2: Background - The PhyloDeep Package (45 seconds)
- **Problem**: Parameter estimation from phylogenetic trees is computationally challenging
- **PhyloDeep Solution**: Uses pre-trained neural networks on 3.9 million trees
- **Our Goal**: Evaluate if MLE, a classical method, can provide competitive results
- **Key Insight**: MLE works with tree data only - no nucleotide sequences needed

---

## Slide 3: MLE Overview (1 minute)
- **What is MLE?**: Maximum Likelihood Estimation - a classical statistical method
- **Goal**: Estimate birth rate (λ) and death rate (μ) from tree topology and branch lengths
- **Key Advantage**: Works on trees of ANY size - no minimum tip requirement
- **Implementation**: Uses numerical optimization (scipy.optimize) with L-BFGS-B algorithm
- **Why This Matters**: PhyloDeep requires at least 50 tips, but MLE works on smaller trees

---

## Slide 4: Stadler (2010) Likelihood Formulation (1.5 minutes)
- **Theoretical Foundation**: Based on Stadler's 2010 paper on "Sampling-through-time in birth-death trees"
- **Likelihood Components**:
  - Branching events term: (n-1) × log(λ) - counts speciation events
  - Branch length term: -(λ + μ) × T_total - accounts for waiting times
  - Sampling term: n × log(ρ) - probability of observing n tips
  - **Survival probability term**: -r × T - THIS IS KEY for identifying μ separately
- **Why the Survival Term Matters**: Without it, μ and λ are confounded. The survival term breaks this degeneracy by modeling the probability that the process survives to produce n tips.

---

## Slide 5: MLE Implementation - Tree Statistics (45 seconds)
- **What We Extract**:
  - Number of tips (n)
  - Total branch length (sum of all edge lengths)
  - Tree height (time from root to present)
  - Branching times (ages of all internal nodes)
- **Smart Initialization**: Method-of-moments estimates
  - Net diversification: r̂ = log(n)/T
  - Birth rate: λ̂ = (n-1)/T_total
  - Death rate: μ̂ = λ̂ - r̂
- **Why This Matters**: Good starting values ensure fast convergence and avoid local minima

---

## Slide 6: MLE Implementation - Optimization (1 minute)
- **Algorithm**: L-BFGS-B (bounded optimization with analytical gradients)
- **Constraints**: 
  - λ ∈ [0.01, 10.0]
  - μ ∈ [0.01, 10.0]
  - μ < λ (enforced via penalty)
- **Key Innovation**: Regularization term prevents μ from collapsing to lower bound
  - When μ < 0.1 and n > 10: penalty = -0.1 × log(μ)
  - This encourages realistic death rates for large trees
- **Gradient**: Analytical gradient provided for faster convergence

---

## Slide 7: MLE Key Features (45 seconds)
- **Feature 1**: Survival probability term (-r × T) - critical for μ identification
- **Feature 2**: Regularization prevents μ from getting stuck at 0.01
- **Feature 3**: Robust error handling for edge cases
- **Feature 4**: Method-of-moments initialization for fast convergence
- **Takeaway**: These features make MLE work reliably across tree sizes

---

## Slide 8: Advantages and Limitations (45 seconds)
- **Advantages**:
  - ✓ Statistically principled (maximum likelihood)
  - ✓ No minimum tree size (works on n < 50)
  - ✓ Fast computation
  - ✓ Based on established theory
- **Limitations**:
  - ✗ Higher RMSE than PhyloDeep on large trees
  - ✗ Point estimates only (no uncertainty)
  - ✗ Can struggle with very large trees (n > 500)
- **Best Use Case**: Small to medium trees where statistical rigor matters

---

## Slide 9: Results - RMSE Comparison (1 minute)
- **Key Finding 1**: RMSE decreases with tree size for both methods
- **Key Finding 2**: MLE can be used on smaller trees (n < 50) where PhyloDeep fails
- **Key Finding 3**: PhyloDeep has lower RMSE on large trees (n ≥ 50), likely due to training on 3.9M trees
- **Interpretation**: MLE provides a baseline for small trees and remains competitive on medium trees

---

## Slide 10: Main Takeaways (30 seconds)
- **MLE fills a gap**: Works on small trees where PhyloDeep cannot
- **Statistical rigor**: Based on well-established Stadler (2010) theory
- **Practical value**: Fast, reliable, and provides optimization diagnostics
- **Future work**: Could extend to include uncertainty quantification (bootstrap or profile likelihood)

---

## Total Time: ~5 minutes

### Tips for Delivery:
1. **Emphasize the survival probability term** - this is the key innovation that makes MLE work
2. **Highlight the small tree advantage** - this is MLE's unique strength
3. **Acknowledge PhyloDeep's advantage on large trees** - be fair in comparison
4. **Use the formula slide** to show mathematical rigor
5. **Connect theory to practice** - explain why each component matters

### Potential Questions:
- **Q**: "Why does MLE struggle on very large trees?"
  - **A**: "The likelihood surface becomes flatter with more data, making optimization more challenging. PhyloDeep's neural network can learn complex patterns from millions of trees."

- **Q**: "Can you add uncertainty quantification to MLE?"
  - **A**: "Yes, we could use parametric bootstrap or profile likelihood to get confidence intervals. This is a natural extension."

- **Q**: "How does the survival probability term work?"
  - **A**: "It models the probability that the birth-death process survives to produce n tips. This probability depends on both λ and μ, allowing us to separate them in the likelihood."

