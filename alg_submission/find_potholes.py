#!/usr/bin/python

'''
	@author: Sprout StreetBump Team	
	
	Main file that returns JSON object of pothole and road damage locations from a StreetBump track 	
	CSV file
'''

import constants as c
import csv
import filters

# filename of csv data to use that is located in datain directory
dataset_file = 'SelfTest_newdata.csv';

# use csv library to create a list of csv rows
reader = list(csv.reader(open('datain/'+dataset_file, 'rb'))) 

headers = reader[0]

# remove csv headers
reader.pop(0)

for row_idx, row in enumerate(reader):
	# discards rows with the wrong number of columns
	if len(row) != len(headers):
		reader.remove(row_idx)
		
	# convert each column to float 
	for element_idx, element in enumerate(row):
		reader[row_idx][element_idx] = float(element)


# execute zaccel std filter
filtered_points = filters.general_std_peaks(reader, 5)

# determine severity
# 
mean, std = filters.running_window(reader,5)
for filtered_point_idx, filtered_point in enumerate(filtered_points):
	filtered_points[filtered_point_idx].append(abs(filtered_point[5]-mean)*10)


# convert filtered points list to json object
json_object = '{"pothole": ['
for filtered_point in filtered_points:
	json_object += '{"longitude": "'+str(filtered_point[c.longitude])+'", "latitude": "'+str(filtered_point[c.latitude])+'", "severity":"'+str(filtered_point[16])+'"}'
	if filtered_point != filtered_points[-1]:
		json_object += ','
json_object += ']}'


print json_object