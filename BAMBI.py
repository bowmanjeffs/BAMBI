# -*- coding: utf-8 -*-
"""
Created on Sun Sep 13 17:18:16 2015

@author: jeff

download the last few years and see which are trending. add that as an
additional value to dictionary

"""

### user setable variables ###

get = 100 # how many names do you want returned?

parent1_bday = 999999
parent2_bday = 999999
due_date = 999999
aatc = 999999 # address at time of conception
start_letters = [] # restrict names to those that start with these letters
sex = 'F' # F or M

### end user setable variables ###

import matplotlib
#matplotlib.use('PS')
import numpy as np
import matplotlib.pyplot as py
import math
import scipy.stats as sps

size = (parent1_bday + parent2_bday) / (due_date / aatc)
            
p = []
names = []
            
with open('yob2014.txt', 'r') as names_in:
    for line in names_in:
        line = line.rstrip()
        line = line.split(',')
        if line[1] == sex:
            if len(start_letters) > 0:
                if line[0][0] in start_letters:
                    n = float(line[2])
                    p.append(float(n))       
                    names.append(line[0])
            else:
                n = float(line[2])
                p.append(float(n))       
                names.append(line[0])                
        
### transform the abundance values ###

geo_mean = sps.mstats.gmean(p)
print 'mean name abundance is', geo_mean

def calc_geo_sd(geo_mean, p):
    p2 = []

    for i in p:
        p2.append(math.log(i / geo_mean) ** 2)
    
    sum_p2 = sum(p2)
    geo_sd = math.exp(math.sqrt(sum_p2 / len(p)))
    return(geo_sd)
    
geo_sd = calc_geo_sd(geo_mean, p)
print 'the standard deviation of name abundance is', geo_sd

## get a gaussion distribution of mean = geo_mean and sd = geo_sd
## of length len(p)

dist_param = sps.norm(loc = geo_mean, scale = geo_sd)
dist = dist_param.rvs(size = sum(p))

## now get the probability of these values

print 'wait for it, generating name probabilities...'
temp_hist = py.hist(dist, bins = len(p))
probs = temp_hist[0]
probs = probs / sum(probs) # potentially max(probs)

### generate a pool of possible names ###

possible_names = np.random.choice(names, size = size, p = probs, replace = True)
final_names = np.random.choice(possible_names, size = get, replace = False)

with open('pick_your_kids_name.txt', 'w') as output:
    for name in final_names:
        print name
        print >> output, name
