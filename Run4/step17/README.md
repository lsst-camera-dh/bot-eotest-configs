The high signal and low signal files are cleaned-up versions of what we used for Run 3.

linearityFlatPairs_hisignal.cfg has 205 pairs that range from 190 to 462000 electrons per pixel.  This
probably is enough to reach full well for all sensors, but should be checked.  The order is scambled and the filter is SDSSi

linearityFlatPairs_losignal.cfg as 44 pairs ranging from 50 to 186 electrons per pixel, in sequential
order.  The 750nm filter is used (to make the exposure times longer than they might have been).  We might consider using the SDSSi filter plus a fairly deep ND filter instead.  Because of the
change in filter, this low-flux sequence needs to be acquired separately from the high-flux
sequence.

Note:  No bias is taken after each flat pair

Note:  Added overlap between flux ranges for the different filters in linearityFlatPairs_hisignal.cfg
Insert overlap at the high and low flux end of each transition, by one flux point
