#!/usr/bin/python

'''
Created on Jul 12, 2011

@author: Ben

csvToList('filename.csv') will open the csv file
filename.csv and convert it to a list of lists of floats
this format can be directly pumped into numpy.array

csvToNPArray converts to a numpy array. this data is zipped
(x<->y) so that numpy can easily calculate means and stds

csvToBoth returns both a List and a numpy array


The input csv files have these fields:

	Time
	Longitude
	Latitude
	AccelX
	AccelY
	AccelZ
	OrientX
	OrientY
	OrientZ
	MagneticX
	MagneticY
	MagneticZ
	Bearing
	Speed
	gpsAccuracy
	Entropy

see constants.py for how to access them
'''

import csv
import numpy as np
import constants as c

standard_path = "../datain/"


def csvToBoth(filename, path=standard_path):
	data = csvHelper(path + filename)
	ndata = np.array(data)
	return (data, ndata)

def csvToNPArray(filename, path=standard_path):
	data = csvHelper(path + filename)
	ndata = np.array(data)
	return ndata

def csvToList(filename, path=standard_path, raw=False):
	return csvHelper(path + filename, raw)

def csvHelper(filepath, raw=False):
	dataReader = csv.reader(open(filepath, 'rb'))
	i = 1
	num_headers = 1
	dataa = []

	# read (remove) the header line, and save the number of fields it contains
	num_headers = len(dataReader.next())

	# read all the rows. convert to floats unless @raw
	for row in dataReader:
		if raw:
			dataa.append(row)
		else:
			datar = []
			# convert each element to a float
			for element in row:
				datar.append(float(element))
			# discards rows with the wrong number of columns
			if len(datar) == num_headers:
				dataa.append(datar)

	# sorts by time
	data2 = sorted(dataa, key=lambda data: data[c.time])

	return data2
