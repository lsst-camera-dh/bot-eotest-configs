The high signal and low signal files are cleaned-up versions of what we used for Run 3.

linearityFlatPairs has 300 pairs logarithmically spaced from 150 e/pixel to 450k e/pixel
in the SDSSi filter.  The order of the fluxes is randomized.  Only the ND_OD1.0 and empty
filter settings are used.  At the transition flux, two flux points are measured in both
ND_OD1.0 and empty filters, so the effects of spectral differences can be scaled out.
With this overlap, this configuration file actually acquires 302 pairs.

Note:  No bias is taken after each flat pair

Note:  An [ANALYSIS_RUNS] entry for gains should be specified in the file

