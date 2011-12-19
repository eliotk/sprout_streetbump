import constants as c
# derived from original filters.py
def general_std_peaks(data, target_column = 5, devs=3.45, mode="both"):
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

def mean(values):
    return sum(values, 0.0) / len(values)

def meanstdv(x): 
	from math import sqrt 
	n, mean, std = len(x), 0, 0 
	for a in x: 
		mean = mean + float(a) 
	mean = mean / float(n) 
	for a in x: 
		std = std + (float(a) - mean)**2
	std = sqrt(std / float(n-1)) 
	return mean, std
	
def running_window(data, target_column = 5):
	column_array=[]
	for entry in data:
		column_array.append(float(entry[target_column]))
	return meanstdv(column_array)
	
def ratio(data, numeratorConstant, denominatorConstant, threshold):
	'''
	this was the xzRatio function, but I generalized it so that now it's also
	the zspeed ration function, and applicable to any time we want a ratio. The 
	numeratorConstant should be c.accelz in the xz ratio, and the denominatorConstant
	should be c.accelx. For zspeed, c.speed should be the numeratorConstant and
	c.accelz should be the denominatorConstant. The threshold variable is the 'we
	are not interested in ratios higher than this' variable.
	'''
	table = []
	for row in data:
		if row[denominatorConstant] == 0:
			row[denominatorConstant] = .0000000001
		if ( abs(row[numeratorConstant] / row[denominatorConstant]) < threshold):
			table.append(row)
	return table
	
def milesPerHourToMetersPerSecond(mph):
	return mph * 0.44704;
		
def min_speed(data, min_speed):
	filtered_speed = []
	for row in data:
		# compare speed against min_speed
		if row[c.speed] > milesPerHourToMetersPerSecond(min_speed):
			# add this row to a new table
			filtered_speed.append(row)
	return filtered_speed