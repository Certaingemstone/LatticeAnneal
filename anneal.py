import numpy as np
import matplotlib.pyplot as pl

#Inputs
N = 5
fill = 14

N2 = N**2
frac = fill/N2
if frac > 1.0:
    print("lattice overfill")
    quit()
if frac < 0.333: a = 3
elif frac < 0.5: a = 2
else: a = 1

#Initial Lattice Condition
lat = np.zeros(N2, dtype=int)
for i in range(fill):
    lat[N2-1-a*i] = 1
lat = lat.reshape((N,N))
print(lat)

#Functions
def checkAdjacents(i,j,lat):
    adj = np.array([])
    try: #Need to deal with corners: (4,4) and ()
        #Top edge
        if i == 0:
            adj = np.array(None , None , [lat[i,j-1] , lat[i,j+1] , lat[i+1,j-1] , lat[i+1,j]])
        #Left edge
        elif j == 0:
            adj = np.array([lat[i-1,j] , lat[i-1,j+1] , None , lat[i,j+1] , None , lat[i+1,j]])
        #Bottom edge
        elif i == N-1:
            adj = np.array([lat[i-1,j] , lat[i-1,j+1] , lat[i,j-1] , lat[i,j+1] , None , None])
        #Right edge
        elif j == N-1:
            adj = np.array([lat[i-1,j] , None , lat[i,j-1] , None , lat[i+1,j-1] , lat[i+1,j]])
        else:
        #Check all adjacents
            adj = np.array([lat[i-1,j] , lat[i-1,j+1] , lat[i,j-1] , lat[i,j+1] , lat[i+1,j-1] , lat[i+1,j]])
    except IndexError:
        print("Corner i"+str(i)+", j"+str(j))
        adj = np.array([])
    return adj

#Main
T = 1.0
for i in range(N):
    for j in range(N):
        if lat[i,j] == 1:
            adj = checkAdjacents(i,j,lat)
            print(adj)
            print("\n")

                    #do something here to checkadjacents for the i,j of the corresponding adjacent
