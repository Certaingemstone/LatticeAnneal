import numpy as np
import matplotlib.pyplot as pl
import random

#Inputs
N = 100
fill = 6666
#Higher gives more steps, nonlinear
steps = 20
#low (-1) or high (1) Energy
lohi = -1
T = 10
stopT = 0.01

N2 = N**2
if fill > N2:
    print("lattice overfill")
    quit()

#Initial Lattice Condition
lat = np.zeros(N2, dtype=int)
for i in range(fill):
    lat[i] = 1
np.random.shuffle(lat)
lat = lat.reshape((N,N))

#Functions - Need to add a way to switch to square lattice

#Possible adjacents
def top(i,j,lat):
    return lat[i-1,j]
def toprht(i,j,lat):
    return lat[i-1,j+1]
def lft(i,j,lat):
    return lat[i,j-1]
def rht(i,j,lat):
    return lat[i,j+1]
def botlft(i,j,lat):
    return lat[i+1,j-1]
def bot(i,j,lat):
    return lat[i+1,j]

""" sites and indices
  0 1
2 X 3
4 5
"""

#Create adjacency list
def checkAdjacents(i,j,lat):
    adj = np.array([None, None, None, None, None, None])
    try:
        #Bottom Left
        if i == N-1 and j == 0:
            adj = np.array([top(i,j,lat) , toprht(i,j,lat) , None , rht(i,j,lat) , None , None])
        #Bottom Right
        elif i == N-1 and j == N-1:
            adj = np.array([top(i,j,lat) , None , lft(i,j,lat) , None , None , None])
        #Top Right
        elif i == 0 and j == N-1:
            adj = np.array([None , None , lft(i,j,lat) , None , botlft(i,j,lat) , bot(i,j,lat)])
        #Top Left
        elif i == 0 and j == 0:
            adj = np.array([None , None , None , rht(i,j,lat) , None , bot(i,j,lat)])
        #Top edge
        elif i == 0:
            adj = np.array([None , None , lft(i,j,lat) , rht(i,j,lat) , botlft(i,j,lat) , bot(i,j,lat)])
        #Left edge
        elif j == 0:
            adj = np.array([top(i,j,lat) , toprht(i,j,lat) , None , rht(i,j,lat) , None , bot(i,j,lat)])
        #Bottom edge
        elif i == N-1:
            adj = np.array([top(i,j,lat) , toprht(i,j,lat) , lft(i,j,lat) , rht(i,j,lat) , None , None])
        #Right edge
        elif j == N-1:
            adj = np.array([top(i,j,lat) , None , lft(i,j,lat) , None , botlft(i,j,lat) , bot(i,j,lat)])
        else:
        #Check all adjacents
            adj = np.array([top(i,j,lat) , toprht(i,j,lat) , lft(i,j,lat) , rht(i,j,lat) , botlft(i,j,lat) , bot(i,j,lat)])
    except IndexError:
        print("Something went wrong at i"+str(i)+", j"+str(j))
    return adj

#Potential of bonds
def getEnergy(adj):
    filter = adj != None
    cleanadj = adj[filter]
    return np.sum(cleanadj)

#Take adjacent energies, give probabilities. Last term is probability of staying in same position.
def EtoP(adjE,T):
    terms = []
    for E in adjE:
        if E != None:
            terms.append(np.exp(lohi*(E/T)) )
        else:
            terms.append(0)
    Z = np.sum(terms)
    return np.divide(terms, Z)

#Main
#adj: adjacency list (1 if occupied, 0 if empty, None if wall), adjP: probabilities of adjacent sites, and lastly the current site (0 to 1, None if adjacent site full)
while T > stopT:
    excluded = []
    for i in range(N):
        for j in range(N):
            #Now specific to an i,j
            adjCoords = {0:[i-1,j], 1:[i-1,j+1], 2:[i,j-1], 3:[i,j+1], 4:[i+1,j-1], 5:[i+1,j], 6:[i,j]}
            if lat[i,j] == 1 and (i,j) not in excluded:
                #Adjacency list
                adj = checkAdjacents(i,j,lat)
                adjE = []
                #Determine probabilities of empty adjacent sites
                for a in range(6):
                    if adj[a] == 0:
                        adjE.append(getEnergy(checkAdjacents(adjCoords[a][0], adjCoords[a][1], lat)) - 1)
                    else:
                        adjE.append(None)
                adjE.append(getEnergy(adj))
                adjP = EtoP(adjE, T)
                #Decide which site to move to, or whether to stay
                #cdf: cumulative distribution starting from site 0, a: index of site chosen to move to SEEMS TO BIAS TOWARDS TOP LEFT
                rand = random.random()
                cdf = 0
                a = -1
                while cdf < rand:
                    cdf += adjP[a+1]
                    a += 1
                #Move or don't move the particle
                lat[i,j] = 0
                lat[adjCoords[a][0], adjCoords[a][1]] = 1
                #Avoid moving particles just moved
                excluded.append((adjCoords[a][0], adjCoords[a][1]))
    T -= T/steps
    print("Temperature: ", T)
pl.imshow(lat, cmap='hot')
pl.show()
