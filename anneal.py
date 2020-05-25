import numpy as np
import matplotlib.pyplot as pl

#Inputs
N = 3
fill = 5

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
print(lat)

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

#Create adjacency list
def checkAdjacents(i,j,lat):
    adj = np.array([])
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

#Sorta-canonical partition function, for adjacent microstates possible for a site
def partitionFunc(adjE,T):
    terms = np.array([])
    for E in adjE:
        np.append(terms, np.exp(-(E/T)) )
    return np.sum(terms)

#Main
T = 1.0
for i in range(N):
    for j in range(N):
        #Now specific to an i,j
        if lat[i,j] == 1:
            #Adjacency list
            adj = checkAdjacents(i,j,lat)
            #Determine probabilities of empty adjacent sites
            for a in range(5):
                if adj[a] == 0:
