linearityFlatPairs has 330 pairs logarithmically spaced from 100 e/pixel to 250k e/pixel
in the SDSSi filter.  The order of the fluxes is randomized (grouped by filter).  Only the
ND_OD0.5 and empty filter settings are used.  At the transition flux, four flux points are
measured in both ND_OD0.5 and empty filters, so the effects of spectral differences can be scaled out.
With this overlap, this configuration file actually acquires 334 pairs.

Note:  No one bias frame is taken after each flat pair. (Use linearityFlatPairs_0bias.cfg for 0 bias frames
between images.  linearityFlatPairs_165.cfg has 165 flat pairs (plus overlap around the filter change) and
one bias frame per flat pair.

Note:  An [ANALYSIS_RUNS] entry for gains should be specified in the file

