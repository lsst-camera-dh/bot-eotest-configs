C_protocol.cfg will need update in [ANALYSIS_RUNS] section to point to Fe55 run number.  Also
for the flat pair acquisition, the number of pairs may need
revisiting.  Initially the pairs are specified as 6 per decade from 450 to 450k electrons/pixel
(for the central raft).  This range should reach full well even for sensors at the edge of the
focal plane.

D_protocol.cfg will also need an update in [ANALYSIS_RUNS] to point to Fe55 run number, and possibly
also a reduction in the number of flat pairs acquired.

C_protocol and D_protocol configurations include 2-point overlaps in the flat pairs when the ND
filter is changed.

bias10.cfg acquires 10 bias frames and runs associated analyses

bias_ptc.cfg makes just the bias frame and flat pair acquisitions of a D_protocol.cfg run.  It may need a gain entry under [ANALYSIS_RUNS]

sflat.cfg acquires bias and sequences of flats at 10k and 50k electrons/pixel, and runs associated
analyses.  The configuration file may need to have a gain entry under [ANALYSIS_RUNS]
