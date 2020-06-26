#Operates on a 2D array, with elements representing the sites of a triangular lattice
#Attempts to either minimize or maximize the local number of "bonds" between adjacent sites
#Employs a version of simulated annealing for optimization.
#Created by Jade Chongsathapornpong, for MIT 8.044 Statistical Physics final assignment, Spring 2020

import numpy as np
import matplotlib.pyplot as pl
import random

#Inputs
#Side dimension of the square array representing a triangular lattice
N = 100
#Number of sites filled
fill = 6666
#Higher gives more steps, nonlinear, recommend <4
steps = 3
#low (-1) or high (1) Energy; low -> particles repel; high -> particles attract
lohi = -1
#Initial and final "temperature," recommend not changing
T = 10
stopT = 0.01

#Check if valid fill
N2 = N**2
if fill > N2:
    print("lattice overfill")
    quit()

#Initialize Lattice; value of 1 represents filled site
lat = np.zeros(N2, dtype=int)
for i in range(fill):
    lat[i] = 1
np.random.shuffle(lat)
lat = lat.reshape((N,N))


#Functions - Will someday add a flag to simulate square lattice

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

""" site indices for triangular (relative positions in the 2D array)
  0 1
2 X 3
4 5
"""

""" site indices for square (TO BE ADDED)
  0
2 X 3
  5
"""

#Create adjacency list; should change to switch but this works okay
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

#Take adjacent energies, give probabilities (assuming canonical ensemble). Last element is probability of staying in same position.
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
            #check if site occupied and if not previously moved to during this turn
            if lat[i,j] == 1 and (i,j) not in excluded:
                #Adjacency list
                adj = checkAdjacents(i,j,lat)
                adjE = []
                #Determine probabilities of empty adjacent sites
                for a in range(6):
                    if adj[a] == 0:
                        adjE.append(getEnergy(checkAdjacents(adjCoords[a][0], adjCoords[a][1], lat)) - 1)
                        #-1 to avoid counting energy of currently occupied site
                    else:
                        adjE.append(None)
                #Determine probability of current site
                adjE.append(getEnergy(adj))
                adjP = EtoP(adjE, T)
                #Decide which site to move to, or whether to stay
                #cdf: cumulative distribution decreasing starting from site 0, a: index of site chosen to move to
                rand = random.random()
                cdf = 1
                a = -1
                while cdf > rand:
                    cdf -= adjP[a+1]
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
