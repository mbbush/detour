from math import sin, cos, asin, sqrt
import math

# support various units. Currently only miles is used.
earth_radius = {
	"mi": 3959,
	"ft": 20903520,
	"km": 6371,
}

# shortcut to iterate math.radians
def radians(*args):
	return [math.radians(arg) for arg in args]

def distance(point1, point2, unit="mi", quick=False):
	'''
	Calculate the distance between two lat/long pairs, given as arrays. Assumes a spherical earth.
	'''
	lat1, lon1, lat2, lon2 = radians(point1[0], point1[1], point2[0], point2[1])
	if not quick:
# use the haversine formula for accurate results anywhere on the spherical earth
		a = sin((lat2 - lat1) / 2)
		b = sin((lon2 - lon1) / 2)
		a = a * a + cos(lat1) * cos(lat2) * b * b
# 	a can sometimes equal 1 + roundoff error
		return 2 * asin(min(1, sqrt(a))) * earth_radius.get(unit)
	else:
# use a rectangular approximation that is very good with distances within a city. Do further testing before using with latitudes > 60 degrees
		x = (lon2 - lon1) * cos(lat1)
		y = lat2 - lat1
		return sqrt(x * x + y * y) * earth_radius.get(unit)

def multi_dist(*points):
	out = 0
	for o, d in zip(points, points[1:]):
		out += distance(o, d)
	return out

def detour(driver_a, driver_b, unit="mi", quick=True):
	origin_a, dest_a = (driver_a.get("origin"), driver_a.get("dest"))
	origin_b, dest_b = (driver_b.get("origin"), driver_b.get("dest"))
	a_drives_dist = multi_dist(origin_a, origin_b, dest_b, dest_a)
	b_drives_dist = multi_dist(origin_b, origin_a, dest_a, dest_b)
	return a_drives_dist - b_drives_dist

