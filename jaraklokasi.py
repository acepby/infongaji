from math import radians, sin,asin,cos,acos,pi

jariBumi = 6371.01

def rad2deg(radians):
	degrees = 180 * radians/pi
	return degrees

def deg2rad(degrees):
	radians = pi * degrees/180
	return radians

def jarak(lokasi0,lokasi1,lat,lon): #(lokasi,tujuan):
	slat = radians(lokasi0)
	slon = radians(lokasi1)
	elat = radians(lat) #radians(tujuan[0])
	elon = radians(lon) #radians(tujuan[1])
	#jari-jari bumi dalam kilometer
	#jariBumi = 6371.01
	res = jariBumi*acos(sin(slat)*sin(elat) + cos(slat)*cos(elat)*cos(slon - elon))
	#print(res)
	return round(res,2) #jariBumi *acos(sin(slat)*sin(elat) + cos(slat)*cos(elat)*cos(slon - elon))

def bounding(lokasi,area):
	maxLat = lokasi[0] + rad2deg(area/jariBumi)
	minLat = lokasi[0] - rad2deg(area/jariBumi)
	maxLon = lokasi[1] + rad2deg(asin(area/jariBumi)/cos(deg2rad(lokasi[0])))
	minLon = lokasi[1] - rad2deg(asin(area/jariBumi)/cos(deg2rad(lokasi[0])))
	#maxLatLon = (maxLat,maxLon)
	#minLatLon = (minLat,minLon)
	bound = [maxLat,minLat,maxLon,minLon]
	return bound
