# ptc_fluxes.py  19 May 2023
# Tabulates PTC config file fluxes with log spacing from 100-20k e/pix and linear spacing to 250k

import numpy as np

f1 = 100.
f2 = 20e3
f3 = 250e3

num1 = 100
num2 = 250

# Range from f1 to f2 is logarithmic in num1 steps
factor = (f2/f1)**(1./num1)

fluxes = []

flux = f1
for i in np.arange(num1):
    fluxes.append(flux)
    flux *= factor

# Range from f2 to f3 is linear in num2 steps

step_size = (f3 - f2)/(num2-1)

flux = f2
for i in np.arange(num2):
    fluxes.append(flux)
    flux += step_size

# randomize
flux_array = np.array(fluxes)
np.random.shuffle(flux_array)

#FLAT=15     296,  # number of electrons/pixel, ND filter
#     15     239,

print('FLAT=15   %6i,' % flux_array[0])
for elt in flux_array[1:-1]:
    print('     15   %6i,' % elt)
print('     15   %6i' % flux_array[-1])
