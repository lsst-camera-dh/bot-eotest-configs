#!/usr/bin/env/python
# Generates a README directory of the contents of the step subdirectories
# The links are correct only for the master branch

import glob

outfile = '../Run6/README.md'
link_root = 'https://github.com/lsst-camera-dh/bot-eotest-configs/blob/master/Run6/'

files = glob.glob('../Run6/*/*.cfg') + glob.glob('../Run6/*/*/*.cfg')
files.sort()

f = open(outfile,'w')

f.write('# Index of Run6 configuration files\n')
print('# Index of configuration files')
for file in files:
    entry = file.split('Run6/')[1]
    entry_esc = entry.replace('_', '\_')
    f.write('* [' + entry_esc + '](' + link_root + entry + ')\n')
    print('* [' + entry_esc + '](' + link_root + entry + ')')

f.close()
