#download the 2012 egypt referendum results from the official website 
# http://referendum2012.elections.eg/results/referendum-results has the results in both csv and xls formats but it doesn't show 
#	the total registred voters and other information we might need , another thing is that to get the breakdown by district you need to go #	through every option in the select field to get individual files  .

#  sudo apt-get install python-setuptools
#  easy_install beautifulsoup4

import urllib2
from bs4 import BeautifulSoup
import csv
import os #for the se of wget command to download the files 
source_url = "http://egelections-2011.appspot.com/Referendum2012/results/index.html"
# using urllib2 to read the remote html page
html = urllib2.urlopen(source_url).read()
#using BeautifulSoup library for pulling data out of HTML
soup = BeautifulSoup(html)
#gettting all the disticts
districts_html =soup.find('select', id="cities")
#print districts_html
districts = districts_html.find_all('option')
f = open('districts.csv', 'wb')
writer = csv.writer(f,delimiter=',')
#saving districts names and codes for possible use in joins or even to match file names with district names .
for option in districts :
	print option.text
        print option.get('value')
        writer.writerow([option.get('value'),option.text.encode('utf-8').strip()])
	#linux command
	csv_command="wget -P csv http://egelections-2011.appspot.com/Referendum2012/results/csv/"+ option.get('value') + ".csv" 
        excel_command="wget -P xls http://egelections-2011.appspot.com/Referendum2012/results/excels/"+ option.get('value') + ".xls" 
        os.system(csv_command)
	os.system(excel_command)
