# 2011 Sprout StreetBump Team

import filters
from google.appengine.ext import db
from google.appengine.ext import webapp
from google.appengine.ext.webapp import util
import os
import sys
from google.appengine.ext.webapp import template
import csv
import StringIO
from django.utils import simplejson  
import constants as c

class MainHandler(webapp.RequestHandler):
    def get(self):
		path = os.path.join(os.path.dirname(__file__), 'index.html')
		
		# retrieve all previously uploaded tracks IMPLEMENT IN FUTURE
		'''
		results = db.GqlQuery("SELECT * FROM csv_files")
		for csv_file in results:
			print csv_file.csv_name
		'''
		
		
		self.response.out.write(template.render(path, {}))
		
# this handles uploaded track files
class FileUploadHandler(webapp.RequestHandler):
	def post(self):
		csv_file_contents = self.request.get("csv_file")
		self.response.out.write(self.request.params["csv_file"].filename)
		# save the uploaded csv to csv_files table in db to have for future
		csv_file = csv_files()
		csv_file.csv_contents = csv_file_contents
		csv_file.csv_name = self.request.params["csv_file"].filename;
		csv_file.put()
		

# use alg to filter and return json object
class FilterHandler(webapp.RequestHandler):
	def get(self):
		# csv_file_name = self.request.get('csv_file_name')
		# self.response.out.write(csv_file_name)
		csv_row = db.GqlQuery('SELECT * FROM csv_files WHERE csv_name = :csv_file_name LIMIT 1', csv_file_name = self.request.get('csv_file_name')).get()
		if csv_row:
			f = StringIO.StringIO(csv_row.csv_contents)
			# reader = csv.reader(f, delimiter=',')
			reader = list(csv.reader(f)) 
		
			headers = reader[0]
			
			# move past headers
			reader.pop(0)
			
			# remove last couple points as tend to be empty
			reader.pop()
			reader.pop()
			
			sorted(reader, key=lambda reader_item: reader_item[0]) 
			
			filtered_points = []
			
			for row_idx, row in enumerate(reader):
				# discards rows with the wrong number of columns
				if len(row) != len(headers):
					reader.remove(row_idx)
					
				# convert each column to float 
				for element_idx, element in enumerate(row):
					reader[row_idx][element_idx] = float(element)
			
			filtered_points = reader
			
			if self.request.get('z_accel_enabled'):		
				# implementation of zaccel filter
				filtered_points = filters.general_std_peaks(reader, 5, float(self.request.get('threshold')), 'both')
			
			if self.request.get('z_x_ratio_enabled'):	
				# implementation of z/x ratio 
				filtered_points = filters.ratio(filtered_points, c.accelz,c.accelx, float(self.request.get('z_x_ratio_threshold')))
			
			if self.request.get('min_speed_enabled'):	
				# implementation of min speed filter 
				filtered_points = filters.min_speed(filtered_points, float(self.request.get('min_speed_threshold_value')))
			
			if self.request.get('z_vs_speed_enabled'):	
				# implementation of min speed filter 
				filtered_points = filters.ratio(filtered_points, c.accelz, c.speed, float(self.request.get('z_vs_speed_threshold_value')))
			
			
			# determine severity
			# get filtered set of points on lowered std spike threshold. this will give us more points clustered around our estimated locations. the greater the number of spikes around our location will help score the severity
			# zaccel_spike_points = filters.general_std_peaks(reader, 5, 1, 'both')
			mean, std = filters.running_window(reader,5)
			for filtered_point_idx, filtered_point in enumerate(filtered_points):
				std_diffs = []
				point_score = 0
				'''
				filtered_point_reader_index = reader.index( filtered_point )
				for point_around_filterered_point in reader[filtered_point_reader_index-5:filtered_point_reader_index+5]:
					std_diffs.append(abs(point_around_filterered_point[5]-std))
				
				if len(std_diffs) > 0:
					std_diff_mean = filters.mean(std_diffs)
					filtered_points[filtered_point_idx].append(std_diff_mean)
				else:
					filtered_points[filtered_point_idx].append(0)
				#### filtered_points[filtered_point_idx].append(abs(filtered_point[5]-mean))
				#filtered_points[filtered_point_idx].append(std_diff_mean)
				'''
				#filtered_points[filtered_point_idx].append(abs(filtered_point[5])-abs(mean)*10)
				#filtered_points[filtered_point_idx].append(abs((filtered_point[5]-mean)/std)*10)
				filtered_points[filtered_point_idx].append(abs(filtered_point[5]-mean)*10)
				
				#mean - (devs * std)
				#filtered_point[5]*devs = std =  mean - (x * std)
			# convert filtered points list to json object
			json_object = '{"pothole": ['
			for filtered_point in filtered_points:
				json_object += '{"longitude": "'+str(filtered_point[c.longitude])+'", "latitude": "'+str(filtered_point[c.latitude])+'", "severity":"'+str(filtered_point[16])+'"}'
				if filtered_point != filtered_points[-1]:
					json_object += ','
			json_object += ']}'
			self.response.out.write( json_object )
		else:
			# that particular one not found, return 404
			self.error(404)
		#for csv_file in results:

def main():
    application = webapp.WSGIApplication([('/', MainHandler), 
										('/file_upload', FileUploadHandler),
										('/filter', FilterHandler)],
                                         debug=True)
    util.run_wsgi_app(application)

# database model csv_files instantiating 
class csv_files(db.Model):
	csv_contents = db.BlobProperty()
	csv_name = db.StringProperty(multiline=False)

if __name__ == '__main__':
    main()