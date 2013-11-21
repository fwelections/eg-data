
#getting the GeoJSON data from original stupid files , badly encoded with wrong formats 

import io, json
import urllib2
import pprint
import csv
from collections import namedtuple
# given and url where the original files are and a district name we download the data , extract what we need and recreate the geojson files 
def create_geojson(url,filename,mode):
	if mode == "g":
		root="governorate"
	else:
		root="district"
	json_data=urllib2.urlopen(url).read()
	# file contents start with a javascript function loadGeoJSON(DATA) , we need to get DATA so we strip the first 12 chars and the last one 
	json_data = json_data[12:]
	json_data = json_data[:-1]
	data = json.loads(json_data)
	crs=str(data[root]['crs'])
	egypt_json='{"type": "FeatureCollection", "crs": {"type": "name", "properties": {"name": "urn:ogc:def:crs:EPSG::3857"}}, "features": ['
	features = data[root]['features']
	for feature in features:
		geo=feature['geometry']
		geostr='{"type":"MultiPolygon","coordinates":' + str(geo["coordinates"]) + '}'
		temp='{"type": "Feature","properties": { "iso": "EGY", "gov_id":"'+ feature["id"] +'", "gov_name":"'+ feature["name"] + '"}, "id":"' + feature["id"] + '", "name":"' + feature["name"] + '", "geometry":' + geostr + '},'
		egypt_json = egypt_json +  temp
	egypt_json = egypt_json [:-1] + "]}"

	file_name= filename + ".geojson"
	with io.open(file_name, 'w') as f:
	  f.write(unicode(egypt_json))

# open a csv file ( from previous work ) that contains the id and name of the governorates 
with io.open('../referendum2012/districts.csv', 'r', encoding='utf-8') as csvfile:
	lines = csvfile.readlines()
        csvfile.close()
for line in lines:
	encoded_line=line
        columns= encoded_line.split(',', 1 )
	#base_url ="http://egelections-2011.appspot.com/Presidential2012/voters-map/shapes/json/egypt-" + DISTRICT_ID +"-goog_geom70.js"
	source_url="http://egelections-2011.appspot.com/Presidential2012/voters-map/shapes/json/egypt-" + columns[0] +"-goog_geom70.js"
	print source_url
	#create_geojson(source_url,columns[1].encode('utf-8'))
	#file formats are different so we create the mode variable to process differently for each case 
	create_geojson(source_url,columns[0],"d")
#create the full map 
egy_url="http://egelections-2011.appspot.com/Presidential2012/voters-map/shapes/json/egypt-EG-goog_geom95.js"
create_geojson(egy_url,"egypt","g")
