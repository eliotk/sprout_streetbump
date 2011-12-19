'''
	@author: Sprout StreetBump Team
	
	Functions for filtering dataset points to zoom in on pothole/damage locations
'''

import constants as c
import math

def general_std_peaks(data, target_column = 5, devs=3.4, mode="both"):
	zs=[]
	for entry in data:
		zs.append(float(entry[target_column]))
	mean, std = meanstdv(zs)
	zbot = mean - (devs * std)
	ztop = mean + (devs * std)
	keep = []
	for i in range(len(data)):
		if (zs[i] > ztop and (mode == "both" or mode == "high") or zs[i] < zbot and (mode == "both" or mode == "low")):
			keep.append(data[i])
	return keep
 
def meanstdv(x): 
	n, mean, std = len(x), 0, 0 
	for a in x: 
		mean = mean + float(a) 
	mean = mean / float(n) 
	for a in x: 
		std = std + (float(a) - mean)**2
	std = math.sqrt(std / float(n-1)) 
	return mean, std
	
def score_algorithm(data):
	score = 0
	newArray = []
	for entry in data:
		score = abs(float(entry[c.speed])/math.sqrt((float(entry[c.accelx])**2)+(float(entry[c.accely])**2)+(float(entry[c.accelz])**2)))
		print score
		newEntry = list(entry)
		newEntry.append(score)
		newArray.append(newEntry)
	return newArray

def running_window(data, target_column = 5):
	column_array=[]
	for entry in data:
		column_array.append(float(entry[target_column]))
	return meanstdv(column_array)