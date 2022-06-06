#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jun  6 16:28:37 2022

@author: cyrusmatheson
"""

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May 30 15:21:15 2022

@author: cyrusmatheson
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import datetime


# Import Facility Data 

flow = pd.read_csv('/Users/cyrusmatheson/Documents/DHIrrigation.csv')

# Establishe time series dataframe

columns = ['A','B','C','D','E','F','JKL','MNQ','PQ','Consumed']
series = pd.date_range(start = '2022-01-01', end = '2022-01-02',freq= 'T')

res_level = pd.DataFrame(index = series, columns= columns)

# Initialize reservoir sizes

for i in range(len(flow)):
    
    res_level.iloc[0,i] = flow.iloc[i,1]
    
res_level.iloc[0,9] = res_level.iloc[0,0:9].sum()


    
#Assumes system is always on (24/7) run time  


for j in range(1,len(res_level)):
    
   
    for i in range(len(flow)):
    
    
        lr = flow.iloc[i,2]
        ot = flow.iloc[i,4]
        it = flow.iloc[i,5]
        full = flow.iloc[i,3]
        cyctime = flow.iloc[i,10]
        float_max = flow.iloc[i,8]
    
        timeleft = full - cyctime 

        if timeleft > 0:
        
        
            if timeleft - it > 0:
                
            
                res_level.iloc[j,i] = round(res_level.iloc[j-1,i] - (float_max/ot),5)
            
                flow.iloc[i,10] = flow.iloc[i,10] + 1
                
                
            elif timeleft - it == 0:
                
                flow.iloc[i,8] = flow.iloc[i,8]*(1-lr)
                
                res_level.iloc[j,i] = round(res_level.iloc[j-1,i] + (flow.iloc[i,8]/it),5)
                
                flow.iloc[i,10] = flow.iloc[i,10] + 1
                
                
            else:
                
                res_level.iloc[j,i] = round(res_level.iloc[j-1,i] +(flow.iloc[i,8]/it),5)
                
                flow.iloc[i,10] = flow.iloc[i,10] + 1
                
            
        else:
                res_level.iloc[j,i] = round(res_level.iloc[j-1,i] - (float_max/ot),5)
                flow.iloc[i,10] = 1
                flow.iloc[i,11] =  flow.iloc[i,11] + 1
                