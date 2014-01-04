import xml.etree.ElementTree as ET
import urllib
import datetime

states = {
	"AL" : 2 ,
	"AK" : 3 ,
	"AZ" : 4 ,
	"AR" : 5 ,
	"CA" : 6 ,
	"CO" : 7 ,
	"CT" : 8 ,
	"DE" : 9 ,
	"DC" : 10 ,
	"FL" : 11 ,
	"GA" : 12 ,
	"HI" : 13 ,
	"ID" : 14 ,
	"IL" : 15 ,
	"IN" : 16 ,
	"IA" : 17 ,
	"KS" : 18 ,
	"KY" : 19 ,
	"LA" : 20 ,
	"ME" : 21 ,
	"MT" : 22 ,
	"NE" : 23 ,
	"NV" : 24 ,
	"NH" : 25 ,
	"NJ" : 26 ,
	"NM" : 27 ,
	"NY" : 28 ,
	"NC" : 29 ,
	"ND" : 30 ,
	"OH" : 31 ,
	"OK" : 32 ,
	"OR" : 33 ,
	"MD" : 34 ,
	"MA" : 35 ,
	"MI" : 36 ,
	"MN" : 37 ,
	"MS" : 38 ,
	"MO" : 39 ,
	"PA" : 40 ,
	"RI" : 41 ,
	"SC" : 42 ,
	"SD" : 43 ,
	"TN" : 44 ,
	"TX" : 45 ,
	"UT" : 46 ,
	"VT" : 47 ,
	"VA" : 48 ,
	"WA" : 49 ,
	"WV" : 50 ,
	"WI" : 51 ,
	"WY" : 52 ,
	}

def get_house_value(address, csz):
	#This method returns a tuple (currValue, soldValue)
	#Format of address = "14232 Shady Oak Ct"
	#Format of csz = "Saratoga, CA"
	if(address == '' or csz == ''):
		return address, csz, 0
	token = "X1-ZWz1dp4nf26mff_10irx"
	params = urllib.urlencode({'zws-id':token, 'address':address, 'citystatezip':csz})
	url = "http://www.zillow.com/webservice/GetDeepSearchResults.htm?%s"
	zillow_xml = urllib.urlopen(url%params).read()
	root = ET.fromstring(zillow_xml)
	currValue,soldValue,soldDate = '','',''
	years = 0
	for child in root.iter('amount'):
		if(child.text):
			currValue = child.text
	for child in root.iter('lastSoldPrice'):
		if(child.text):
			soldValue = child.text
	for child in root.iter('lastSoldDate'):
		if(child.text):
			soldDate = child.text
	if soldValue and not currValue:
		currValue = soldValue
	elif currValue and not soldValue:
		soldValue = currValue
	if soldDate:
		timeSincePurchase = datetime.datetime.today() - datetime.datetime.strptime(soldDate, '%m/%d/%Y')
		years = timeSincePurchase.days/365
	return currValue, soldValue, years

filenames = ['Data/donor_data.csv', 'Data/donor_data2.csv']
user_id = 0

for filename in filenames:
	f = open(filename, 'r')
	output = open('Data/donor_features.csv', 'w')
	donations = f.readlines()[0].split('\r')
	donations.pop(0)
	output.write("id, city, state, donation, house_price, house_sold_at, years_sold\n")
	for line in donations:
		elements = line.strip().split(',')
		name = elements[1]
		addr = elements[8]
		amount = elements[2]
		city = elements[10]
		state = elements[11]
		csz = "%s,%s"%(city, state)
		if not addr or not city or not state:
			continue
		currVal,soldVal,years = get_house_value(addr, csz)
		out = "%d, %s, %d, %s, %s, %s, %d\n"%(user_id, city, states.get(state, 0), amount, currVal, soldVal, years)
		output.write(out)
		user_id = user_id + 1
	f.close()
output.close()
