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
series = pd.date_range(start = '2022-01-01', end = '2022-02-01 00:01:00',freq= 'T')

res_level = pd.DataFrame(index = series, columns= columns)

# Initialize reservoir sizes

for i in range(len(flow)):
    
    res_level.iloc[0,i] = flow.iloc[i,1]
    

# Establishing base consumption as the sum of each reservoirs gallon size 
    
res_level.iloc[0,9] = res_level.iloc[0,0:9].sum()


# # Defining function to calculate i'th reservoir level at the j'th minute


def calc_level(
        lr,
        ot,
        it,
        full,
        cyctime,
        float_max,
        j,
        i
        ):
    
    # Calculates the time left remaining in teh current reservoir cycle
    
    timeleft = full - cyctime
    
    # Checks for the daily refill and one hour stop which occurs at 11:00PM
    
    stop_count = (j+60) % 1440
    
    # While top_up is engaged reservoir levels wont change
    
    top_up = flow.iloc[i,13]
    
    # top_timer runs for 60 minutes and then allows the cycles to resume
    
    top_timer = flow.iloc[i,14]
    
    # Reservoirs are flushed every two weeks. This initiates the flush cycle.
    
    flush_count = j % 20160
    
    
    
    # Hitting zero initiates a flush run
    
    if flush_count == 0:
        
    
        # Smaller reservoirs are cycled completely
        
        if i < 6:
            
            res_level.iloc[j,i] = flow.iloc[i,1]
            
            flow.iloc[i,10] = flow.iloc[i,10] + 1
            
            res_level.iloc[j,9] = res_level.iloc[j,9] + flow.iloc[i,1]
            
        #Larger reservoirs only have 250 gallons cycled    
            
        else:
            
     
            res_level.iloc[j,i] = flow.iloc[i,1]
            
            flow.iloc[i,10] = flow.iloc[i,10] + 1
            
            
            res_level.iloc[j,9] = res_level.iloc[j,9] + 250

    
    # At 11:00PM this pauses cycle and refills reservoirs and restarts cycles
        
    elif  stop_count == 0:
    
        
        # This sets water level immediately back to full reservoir level
        
        res_level.iloc[j,i] = flow.iloc[i,1]
        
        # Sets float_max back to full
        
        flow.iloc[i,8] = flow.iloc[i,1]
        
        # Restarts cycle

        flow.iloc[i,10] = full
        
        
        # This turns on the stall and begins the top_up timer
        
        flow.iloc[i,13] = 1
        
        flow.iloc[i,14] = flow.iloc[i,14] + 1
        
    
    
    # While top_up is engaged levels don't change
    
    elif top_up == 1 and top_timer < 60:
        
        res_level.iloc[j,i] = res_level.iloc[j-1,i] 
        
        flow.iloc[i,10] = flow.iloc[i,10] + 1
        
        flow.iloc[i,14] = flow.iloc[i,14] + 1
        
        
    # Once timer maxes, the reservoir cycles restart    
     
    elif top_timer == 60:
        
        res_level.iloc[j,i] = res_level.iloc[j-1,i] 
        
        flow.iloc[i,14] = 0 
        
        flow.iloc[i,13] = 0
        
    

    # If a flush/top up cycle isn't initiated and there is time left in the cycle this process is started
    
    elif timeleft > 0:
        
        
        # If time remaining - fill time remains a positive integer, the reservoir should still be emptying
    
        if timeleft - it > 0:
            
            res_level.iloc[j,i] = res_level.iloc[j-1,i] - (float_max/ot)
            
            flow.iloc[i,10] = flow.iloc[i,10] + 1
            
        
        # At zero the emptying cycle has ended and the reservoir is refilling 
        # Need to establish a new float_max, which is the max level of the reservoir for each respective cycle
        # Also calculate the loss delta (constant value specific to each reservoir)
            
        elif timeleft - it == 0:
            
            flow.iloc[i,12] = flow.iloc[i,1]*lr
            
            flow.iloc[i,8] = flow.iloc[i,8] - flow.iloc[i,1]*(lr)
            
            res_level.iloc[j,i] = (flow.iloc[i,8]/it)
            
            flow.iloc[i,10] = flow.iloc[i,10] + 1
            
         
        # After zero reservoir continues refilling at a constant rate   
            
            
        else:
            
            res_level.iloc[j,i] = res_level.iloc[j-1,i] + (flow.iloc[i,8]/it)
            
            flow.iloc[i,10] = flow.iloc[i,10] + 1
            
    
    # If no time is left in the cycle calculate consumption for the cycle  and increase the cycle counter
        
        
    else:
            res_level.iloc[j,i] = res_level.iloc[j-1,i] - (float_max/ot)
            
            flow.iloc[i,10] = 1
            
            flow.iloc[i,11] =  flow.iloc[i,11] + 1
            
            res_level.iloc[j,9] = res_level.iloc[j,9] + flow.iloc[i,12]
    
   
    return(res_level.iloc[j,i])
 
 
 
 


# Running function to perform calculation

for j in range(1,len(res_level)):
    
    res_level.iloc[j,9] = res_level.iloc[j-1,9]
    
   
    for i in range(len(flow)):
        
        lr = flow.iloc[i,2]
        ot = flow.iloc[i,4]
        it = flow.iloc[i,5]
        full = flow.iloc[i,3]
        cyctime = flow.iloc[i,10]
        float_max = flow.iloc[i,8]
        
        
        res_level.iloc[j,i] = calc_level(lr,ot,it,full,cyctime,float_max,j,i)
        
        
                
total_consumed = res_level.iloc[-1,9]



## Raw function logic


# for j in range(1,len(res_level)):
    
#     res_level.iloc[j,9] = res_level.iloc[j-1,9]
    
   
#     for i in range(len(flow)):
        
#         # Reestablishing variables for the j'th minute on reservoir i
        
#         lr = flow.iloc[i,2]
        
#         ot = flow.iloc[i,4]
        
#         it = flow.iloc[i,5]
        
#         full = flow.iloc[i,3]
        
#         cyctime = flow.iloc[i,10]
        
#         float_max = flow.iloc[i,8]
        
#         # Caculates the time remaining in reservoir cycle
        
#         timeleft = full - cyctime
        
#         # Stop/refill occurs at 11:00PM daily for an hour
        
#         stop_count = (j+60) % 1440
        
#         # While top_up is engaged reservoir levels wont change
        
#         top_up = flow.iloc[i,13]
        
#         # top_timer runs for 60 minutes and then allows the cycles to resume
        
#         top_timer = flow.iloc[i,14]
        
#         # Flush timer 
        
#         flush_count = j % 20160
        
        
#         if flush_count == 0:
            
        
            
#             if i < 6:
                
#                 res_level.iloc[j,i] = flow.iloc[i,1]
                
#                 flow.iloc[i,10] = flow.iloc[i,10] + 1
                
#                 res_level.iloc[j,9] = res_level.iloc[j,9] + flow.iloc[i,1]
                
#             else:
                
         
#                 res_level.iloc[j,i] = flow.iloc[i,1]
                
#                 flow.iloc[i,10] = flow.iloc[i,10] + 1
                
                
#                 res_level.iloc[j,9] = res_level.iloc[j,9] + 250
    
        
#         # At 11:00PM pauses cycle and refills reservoirs and restarts cycles
            
#         elif  stop_count == 0:
        
            
#             # This sets water level immediately back to full reservoir level
            
#             res_level.iloc[j,i] = flow.iloc[i,1]
            
#             # Sets float_max back to full
            
#             flow.iloc[i,8] = flow.iloc[i,1]
            
#             # 
    
#             flow.iloc[i,10] = full
            
            
#             # This turns on the stall and begins the top_up timer
            
#             flow.iloc[i,13] = 1
            
#             flow.iloc[i,14] = flow.iloc[i,14] + 1
            
        
        
#         # While top_up is engaged 
        
#         elif top_up == 1 and top_timer < 60:
            
#             res_level.iloc[j,i] = res_level.iloc[j-1,i] 
            
#             flow.iloc[i,10] = flow.iloc[i,10] + 1
            
#             flow.iloc[i,14] = flow.iloc[i,14] + 1
            
         
#         elif top_timer == 60:
            
#             res_level.iloc[j,i] = res_level.iloc[j-1,i] 
            
#             flow.iloc[i,14] = 0 
            
#             flow.iloc[i,13] = 0
        
        
#         elif timeleft > 0:
        
        
#             if timeleft - it > 0:
                
#                 res_level.iloc[j,i] = res_level.iloc[j-1,i] - (float_max/ot)
                
#                 flow.iloc[i,10] = flow.iloc[i,10] + 1
                
                
                
#             elif timeleft - it == 0:
                
#                 flow.iloc[i,12] = flow.iloc[i,1]*lr
                
#                 flow.iloc[i,8] = flow.iloc[i,8] - flow.iloc[i,1]*(lr)
                
#                 res_level.iloc[j,i] = (flow.iloc[i,8]/it)
                
#                 flow.iloc[i,10] = flow.iloc[i,10] + 1
                
                
#             else:
                
#                 res_level.iloc[j,i] = res_level.iloc[j-1,i] + (flow.iloc[i,8]/it)
                
#                 flow.iloc[i,10] = flow.iloc[i,10] + 1
            
            
#         else:
#                 res_level.iloc[j,i] = res_level.iloc[j-1,i] - (float_max/ot)
                
#                 flow.iloc[i,10] = 1
                
#                 flow.iloc[i,11] =  flow.iloc[i,11] + 1
                
#                 res_level.iloc[j,9] = res_level.iloc[j,9] + flow.iloc[i,12]
            
                
# total_consumed = res_level.iloc[-1,9]

# print(total_consumed)


# res_level.plot(kind ='line', y = 'A' )
# res_level.plot(kind ='line', y = 'PQ' )
# res_level.plot(kind ='line', y = 'Consumed' )
# plt.show()

        



                