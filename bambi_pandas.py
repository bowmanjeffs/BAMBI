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
import numpy as np
import pandas as pd


size = (parent1_bday + parent2_bday) / (due_date / aatc)

df = pd.read_csv('yob2014.txt', names=['name','sex','p'])
# refine based on sex
dfg = df[df.sex==sex]
# refine based on letter
for let in start_letters:
    dfg = dfg[dfg.name.str.startswith(let)]

plog_mean = np.log(dfg.p).mean()
plog_std = np.log(dfg.p).std()

print 'mean name abundance is', np.exp(plog_mean)
print 'the standard deviation of name abundance is', np.exp(plog_std)
print 'most popular names in your subset:'
print dfg.sort('p', ascending=False).head()

# calculate weight factor based on normal distribution
prob = ( (plog_std * np.sqrt(2*np.pi))**-1 *
         np.exp( -(np.log10(dfg.p) - plog_mean)**2 / (2*plog_std**2)))

# get a random sample
print dfg.sample(n=get, weights=prob, replace=False)
