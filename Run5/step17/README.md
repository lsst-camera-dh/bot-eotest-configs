linearityFlatPairs has 300 pairs logarithmically spaced from 100 e/pixel to 200k e/pixel
in the SDSSi filter.  The order of the fluxes is randomized (grouped by filter).  Only the
ND_OD1.0 and empty filter settings are used.  At the transition flux, four flux points are
measured in both ND_OD1.0 and empty filters, so the effects of spectral differences can be scaled out.
With this overlap, this configuration file actually acquires 302 pairs.

Note:  No one bias frame is taken after each flat pair. (Use linearityFlatPairs_0bias.cfg for 0 bias frames
between images.  linearityFlatPairs_160.cfg has 160 flat pairs (with overlap around the filter change) and
one bias frame per flat pair.

Note:  An [ANALYSIS_RUNS] entry for gains should be specified in the file

