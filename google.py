import sys, requests, earth


def detour(driver_a, driver_b, unit="mi", quick=True):
	origin_a, dest_a = (driver_a.get("origin"), driver_a.get("dest"))
	origin_b, dest_b = (driver_b.get("origin"), driver_b.get("dest"))
	a_drives_dist = earth.multi_dist(origin_a, origin_b, dest_b, dest_a)
	b_drives_dist = earth.multi_dist(origin_b, origin_a, dest_a, dest_b)
	return a_drives_dist - b_drives_dist

def call_google_api(points):
	'''Use the Google Maps Distance Matrix API to return a json with the relative driving times and road distances between points.'''
	u = "https://maps.googleapis.com/maps/api/distancematrix/json"
	p = {"origins": '|'.join(points), "destinations": '|'.join(points)}
	return requests.get(u, params=p)

def main(args):
	'''
	Function to compute the detour distance each of two drivers would have to make to pick up and drop off the other.
	'''
# 	args[0] is the script name
	o1 = args[1] if len(args) >= 2 else None
	d1 = args[2] if len(args) >= 3 else None
	o2 = args[3] if len(args) >= 4 else None
	d2 = args[4] if len(args) >= 5 else None
	if not (o1 and o2 and d1 and d1):
		print('You may enter locations as anything that Google can parse. \n'
			'Valid examples include:\n'
			'32.85938175,-110.85930157\n'
			'Concord, CA\n' +
			'308 Madison Ave, New York, NY\n')
		if o1: print('Person A starting from: ' + o1)
		else: o1 = raw_input('Starting point of person A')
		if d1: print('Person A going to: ' + d1)
		else: d1 = raw_input('Destination point of person A')
		if o2: print('Person B starting from: ' + o2)
		else: o2 = raw_input('Starting point of person B')
		if d2: print('Person B going to: ' + o1)
		else: d2 = raw_input('Destination point of person B')
	points = [o1, d1, o2, d2]
	distances = call_google_api(points)
# 	print distances.text
# 	response is a 4x4 matrix in dict form, with each row corresponding to a single origin,
# 	and each column (called elements) corresponding to a single destination.
	rows = distances.json().get('rows')
	o1o2 = rows[0].get('elements')[2]
	o2d2 = rows[2].get('elements')[3]
	d2d1 = rows[3].get('elements')[1]
	o2o1 = rows[2].get('elements')[0]
	o1d1 = rows[0].get('elements')[1]
	d1d2 = rows[1].get('elements')[3]

	a_drives_dist = int(o1o2.get('distance').get('value')) + \
					int(o2d2.get('distance').get('value')) + \
					int(d2d1.get('distance').get('value'))
	a_drives_time = int(o1o2.get('duration').get('value')) + \
					int(o2d2.get('duration').get('value')) + \
					int(d2d1.get('duration').get('value'))
	b_drives_dist = int(o2o1.get('distance').get('value')) + \
					int(o1d1.get('distance').get('value')) + \
					int(d1d2.get('distance').get('value'))
	b_drives_time = int(o2o1.get('duration').get('value')) + \
					int(o1d1.get('duration').get('value')) + \
					int(d1d2.get('duration').get('value'))
	print("If A drives, he will drive a total of " + m_2_miles(a_drives_dist) + " and take " + sec_2_hms(a_drives_time))
	print("If B drives, he will drive a total of " + m_2_miles(b_drives_dist) + " and take " + sec_2_hms(b_drives_time))

	show_comparison(a_drives_dist, a_drives_time, b_drives_dist, b_drives_time)
	return a_drives_time - b_drives_time

def show_comparison(ad, at, bd, bt):
	'''Print the results of who should drive and how much time/distance will be saved.'''
	if (ad < bd and at <= bt) or (ad <= bd and at < bt):
		print("A should drive. It will save " + sec_2_hms(bt - at) + " and be " + m_2_miles(bd - ad) + " shorter.")
	elif (ad > bd and at >= bt) or (ad >= bd and at > bt):
		print("B should drive. It will save " + sec_2_hms(at - bt) + \
			 " and be " + m_2_miles(ad - bd) + " shorter.")
	elif ad == bd and at == bt:
		print("It doesn't matter who drives. It will take the same time and distance either way.")
	else:
		print("Split decision.")
		print(\
				("If A drives it will save " + sec_2_hms(bt - at) + ".\n"\
				) if at < bt else \
				("If B drives it will save " + sec_2_hms(at - bt) + ".\n"\
				) + ("If A drives it will be " + m_2_miles(bd - ad) + " shorter."\
				) if ad < bd else \
				("If B drives it will be " + m_2_miles(ad - bd) + " shorter."\
				)
			)


def sec_2_hms(sec):
	'''
	Convert an integer number of seconds into a string representation in seconds, minutes and seconds, minutes, or hours and minutes, as appropriate
	'''
	h = sec / 3600
	m = (sec % 3600) / 60
	s = sec % 60
	if h == 0:
		if m == 0:
			return str(s) + ' sec'
		elif m <= 5:
			return str(m) + ' min ' + str(s) + ' sec'
		else:
			return str(m) + ' min'
	else:
		return str(h) + ' hr ' + str(m) + ' min'

def m_2_miles(meters):
	'''
	Convert an integer number of meters into a string representation in miles.
	'''
	m = float(meters)
	mi = m / 1609.34  # meters in a mile
	return "{0:.1f}".format(mi) + " miles"

if __name__ == "__main__":
	main(sys.argv)
