#!/usr/bin/env/python
# Generates a README directory of the contents of the step subdirectories
# The links are correct only for the master branch

import glob

outfile = '../Run5/README.md'
link_root = 'https://github.com/lsst-camera-dh/bot-eotest-configs/blob/master/Run5/'

files = glob.glob('../Run5/*/*.cfg') + glob.glob('../Run5/*/*/*.cfg')
files.sort()

f = open(outfile,'w')

f.write('# Index of Run5 configuration files\n')
print('# Index of configuration files')
for file in files:
    entry = file.split('Run5/')[1]
    entry_esc = entry.replace('_', '\_')
    f.write('* [' + entry_esc + '](' + link_root + entry + ')\n')
    print('* [' + entry_esc + '](' + link_root + entry + ')')

f.close()
