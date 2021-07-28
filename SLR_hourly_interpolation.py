# -*- coding: utf-8 -*-
"""
Created on Wed May 19 08:06:19 2021

@author: catherinef
"""

#This may be clunky, but it's my first python code. Also did SLR interpolation
#in Matlab. I will try to upload that one as well.

pip install pandas
import pandas as pd #import pandas now includes entire library to use
#as pd uses pd as shortcut when calling functions, so instead of pands.(function_name)...
#we use pd.(function_name)

#to get current directory (optional):
import os
#navigating to desired working directory
os.chdir('Documents')
os.chdir('Scenarios')

#so now we need to get data
slr = pd.read_csv(r'C:\Users\catherinef\Documents\Scenarios\SLR_to_be_interpolated_05192021.csv')
#don't know yet how to set the folder, so I just included the whole pathway


#getting started
import numpy as np
time = pd.date_range('2020-12-31 23:00', periods=6, freq='10Y')
#above command rewrites time intervals to interval compatible for interpolating
#slr['Time'] = time #this works but it puts the time column at the end
#this solution is better
slr.insert(0, 'Time', time, True) #0 indicates the position of insertion
#the magic
slr2 = slr.set_index('Time').resample('h').mean().interpolate('linear')
del slr2['Scenario/RCP']

#adding the early dates before interpolation
time2 = pd.date_range('2019-01-01 0:00', periods=1)

time_combine = time2.union(time) #adding the dates together to include 2019 for spin up

#follow this
#creating a row of zeros
row1 = pd.DataFrame([[0]*len(slr.columns)], columns=slr.columns)
slr2 = row1.append(slr, ignore_index=True)
del slr2['Scenario/RCP'] #cleanup
del slr2['Time'] #this is so I don't have 2 columns named 'Time' later - that will
#complicate the resample/interpolation
#alright so now we have a blank row of zeros at the top of the slr values
#that means that the number of rows in time_combine and slr2 line up
slr2.insert(0, 'Time', time_combine, True)

#the above command combines time and slr values, now we interpolate beginning from 2019
slr_spinup = slr2.set_index('Time').resample('h').mean().interpolate('linear')

slr_spinup.to_csv(r'C:/Users/catherinef/Documents/Scenarios/slr_all_interpolated.csv')