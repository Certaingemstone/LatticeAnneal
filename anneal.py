import numpy as np
import matplotlib.pyplot as pl

#Inputs
N = 5
fill = 7

N2 = N**2
frac = fill/N2
if frac > 1.0:
    print("lattice overfill")
    quit()
if frac < 0.333: x = 3
elif frac < 0.5: x = 2
else: x = 1

#Initial Lattice Condition
lat = np.zeros(N2, dtype=int)
for i in range(fill):
    lat[N2-1-x*i] = 1
lat = lat.reshape((N,N))

#Adjust
T = 1.0
print(lat[3,3])
