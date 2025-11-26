# Project 2 - Stats 607

Submission repository for Project 2 - *Simulation study*, and Project 3 - *High-Performance simulation study*, of the course Stats 607 - *Programming and Numerical method in Statistics*.

The repository implements the experiment in the paper *Controlling the False Discovery Rate: a Practical and Powerful
Approach to Multiple Testing*, published in JRSSB 1995 by Benjamini and Hochberg (that introduces BH correction).

### Running the experiment

The parameters are saved and can be adjusted in the file `params.json`. Use `make test` to run the test suite, and `make all` to run the experiment. With`"num_reps"` equal 2000 the full experiment should take about 5 seconds to run; when equal 20000 (as in the paper) it should take less than a minute.

### Reproducibility of paper's result

The original results was partially reproduced in this experiment. The results of power of correction methods for high number of hypotheses is reproduced, but differ for low number of hypotheses (such as 4 and 8), especially when there is more null hypotheses (50% or 75% of the number of hypotheses). We believe this is mainly due to possible miss-intepretation of the following part, which is unclear technicality-wise in the paper:

> The non-zero expectations were
divided into four groups and placed at L/4, LI2, 3L/4 and L in the following three
ways:
>  (a) linearly decreasing (D) number of hypotheses away from 0 in each group;
> (b) equal (E) number of hypotheses in each group; and
> (c) linearly increasing (I) number of hypotheses away from 0 in each group.

This gives us no information about how the two "linear" assignment schemes work, as well as what to do when dividing equally into the 4 groups leaves a remainder. These problems are significant when the number of hypotheses is low or the ratio of nulls is high, making the number of alternative hypotheses low.

### Simulation design

Other than the afore-mentioned part that has to be re-intepreded, as far as we are aware, the design of the experiment reflects that of the one in the paper. The setting is a unit-variance z-test for normal hypotheses.

### Additional features implemented for Project 3:

* Bug fixes and code clean-ups from Project 2
* Vectorized implementation of Hochberg and BH methods, and corresponding correctness checks.
* Simple embarassingly paralelization of the experiment script, running multiple values of `L` at the same time (e.g., the values `L=5.0` and `L=10.0` could be ran in parallel instead of sequentially).
* Scripts to benchmark and analyze complexity.
* Additional make targets.
