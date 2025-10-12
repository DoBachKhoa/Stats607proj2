## ADEMP framework documentation

### ADEMP framework
* Aims: To verify the experiment of Benjamini and Hochberg in their paper: *Controlling the False Discovery Rate: a Practical and Powerful
Approach to Multiple Testing*. The experiment compares the power of BH correction method that controls for FDR and other FWER control method such as Bonferoni correction and modified Hochberg correction.
* Data-generating mechanism (DGMs): Gaussian mean hypothesis, variance 1, z-test. Number of hypotheses: $m\in\{4, 8, 16, 32, 64\}$. Proportion of true hypotheses: 0%, 25%, 50% and 75%. The non-null hypotheses has expectation $\frac14L,\frac12L,\frac34L$ and $L$, with $L\in\{5,10\}$. Distribution of non-null means in these groups are a) linear Decreasing (D) away from 0, b) Equal (E) number of hypotheses, and c) linear Increasing (I) away from 0 in each group. (this is unclear but is re-interpreted as well as possible in my experiment).
* Estimand / Target: The power of the three method, plotted against each other in various settings for comparision
* Methods: Bonferoni correction, Hochberg (1988) correction, and BH correction.
* Performance measure: Power (i.e., the proportion of rejected hypotheses that are not true).