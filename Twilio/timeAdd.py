# -*- coding: utf-8 -*-
"""
Created on Sun Oct 29 01:04:26 2017

@author: Colle
"""
from datetime import datetime, date
import time

def return_new_time(datetimeobj,moreTime):
    #change from datetimeobj to time tuple
    time_tuple = datetimeobj.timetuple()
    
    #change from time tuple timestamp
    timestamp = time.mktime(time_tuple)
    
    #update timestamp
    print(timestamp)
    timestamp += moreTime
    print(timestamp)
    
    #change from timestamp to datetimeobj
    dt_obj = datetime.fromtimestamp(timestamp)
    
    return(dt_obj)
"""
# testing code
date_obj = datetime(2008,11,10,17,53,59) 
print(date_obj)
print(return_new_time(date_obj,300000))
"""