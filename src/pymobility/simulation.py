# coding: utf-8
#
#  Copyright (C) 2008-2010 Istituto per l'Interscambio Scientifico I.S.I.
#  You can contact us by email (isi@isi.it) or write to:
#  ISI Foundation, Viale S. Severo 65, 10133 Torino, Italy. 
#
#  This program was written by André Panisson <panisson@gmail.com>
#
from pymobility.models.mobility import gauss_markov, reference_point_group, tvc
'''
Created on Jan 24, 2012

@author: André Panisson
@contact: panisson@gmail.com
@organization: ISI Foundation, Torino, Italy
'''
import numpy as np
from models import truncated_levy_walk, random_direction, random_waypoint, random_walk
import logging
from scipy.spatial.distance import cdist

logging.basicConfig(format='%(asctime)-15s - %(message)s', level=logging.INFO)
logger = logging.getLogger("simulation")

DRAW = True
CALCULATE_CONTACTS = True
TRACE_CONTACTS = False

nr_nodes = 100
MAX_X, MAX_Y = 100, 100

#MIN_V, MAX_V = 0.003, 0.03
MIN_V, MAX_V = 0.1, 1.

MAX_WT = 100.
RANGE = 1.

STEPS_TO_IGNORE = 10000

if TRACE_CONTACTS:
    trace_file = file("/tmp/trace.txt", 'w')

if DRAW:
    #import matplotlib
    #matplotlib.use('PS')
    import matplotlib.pyplot as plt
    plt.ion()
    ax = plt.subplot(111)
    line, = ax.plot(range(MAX_X), range(MAX_X), linestyle='', marker='.')

contacts = [None]*nr_nodes

def contacts_list():
    l = []
    for i in range(nr_nodes):
        if len(contacts[i])>0:
            for n in contacts[i]:
                l.append((i,n))
    return l

if DRAW and CALCULATE_CONTACTS:
    for l in range(100):
        ax.plot([], [], 'b-')
        
step = 0
np.random.seed(0xffff)

# UNCOMMENT THE MODEL YOU WANT TO USE
#for xy in truncated_levy_walk(nr_nodes, dimensions=(MAX_X, MAX_Y)):
#for xy in random_direction(nr_nodes, dimensions=(MAX_X, MAX_Y)):
#for xy in random_waypoint(nr_nodes, dimensions=(MAX_X, MAX_Y), velocity=(MIN_V, MAX_V), wt_max=MAX_WT):
for xy in random_walk(nr_nodes, dimensions=(MAX_X, MAX_Y)):
#for xy in gauss_markov(nr_nodes, dimensions=(MAX_X, MAX_Y), alpha=0.99):

## Reference Point Group model
#groups = [4 for _ in range(10)]
#nr_nodes = sum(groups)
#for xy in reference_point_group(groups, dimensions=(MAX_X, MAX_Y), aggregation=0.5):

#groups = [4 for _ in range(10)]
#nr_nodes = sum(groups)
#for xy in tvc(groups, dimensions=(MAX_X, MAX_Y), aggregation=[0.5,0.], epoch=[100,100]):
    
    step += 1
    if step%10000==0: logger.info('Step %s'% step)
    if step < STEPS_TO_IGNORE: continue
    
    if CALCULATE_CONTACTS:
        
#        d = np.zeros((nr_nodes, nr_nodes), dtype=np.double)
#        for i in xrange(0, nr_nodes):
#            for j in xrange(0, nr_nodes):
#                d[i,j] = (abs(xy[i]-xy[j])**2.).sum() ** 0.5 # minkowski(XA[i:], XB[j:], p)
        
        d = cdist(xy,xy)
        #print d
        c = zip(*np.where(d<RANGE))
        
#        if step == STEPS_TO_IGNORE*2:
#            assert [(i,j) for (i,j) in c if i!=j] == [(0, 41), (14, 74), (41, 0), (74, 14)]
            
        if TRACE_CONTACTS:
            trace_file.write(str(contacts_list())+"\n")
    
    if DRAW:
        
        if CALCULATE_CONTACTS:
            lnr = 1
            for (i,j) in c:
                    if j > i:
                        ax.lines[lnr].set_data([xy[i,0],xy[j,0]], [xy[i,1],xy[j,1]])
                        lnr += 1
            for i in xrange(lnr, 100):
                ax.lines[i].set_data([],[])
        
        line.set_data(xy[:,0],xy[:,1])
        plt.draw()
    