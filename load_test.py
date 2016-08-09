from reverse_geocoder import geo_hash
import reverse_geocoder as rg
import time
import sys
from random import random
from LatLon import LatLon



chunk_size = 500000




start = time.time()



# '\u0001' character as delimter. It contains: street address, city, state, postal code, country code, and categories (comma separated)

DISTANCE_THRESHOLD = 1
MAX_DISTANCE = 50
sampling_rate = -1

def compare(points, should_filter=False, max_distance=DISTANCE_THRESHOLD):
	ret_val = rg.search([p[0] for p in points], max_distance=max_distance)

	counts = {
		"country_mismatch": 0
		, "postal_code_mismatch": 0
		, "country_new": 0
		, "postal_code_new": 0
		, "filtered": 0
		, "postal_code_match": 0
		, "internal_filtered": 0
		, "country_match": 0
	}
	
	for i, point in enumerate(points):
		if chr(0001) in point[1] and "|" in point[1]:
			expected = point[1].split(chr(0001))[0].split("|")
		elif chr(0001) in point[1]:
			expected = point[1].split(chr(0001))
		else:
			expected = point[1].split('|')

		expected_postal_code = expected[3].upper()
		expected_country = expected[4].upper()
		

		if len(expected_country) > 2:
			temp = expected_country
			expected_country = expected_postal_code
			expected_postal_code = temp

		if not ret_val[i]:
			counts["filtered"] += 1
		elif should_filter and LatLon(point[0][0], point[0][1]).distance(LatLon(ret_val[i]["lat"], ret_val[i]["lon"])) > MAX_DISTANCE:
			counts["internal_filtered"] += 1
		else:
			
			result_postal_code = ret_val[i].get("pc", "").upper()
			result_country = ret_val[i].get("cc", "").upper()
			result_point = LatLon(ret_val[i]["lat"], ret_val[i]["lon"])
			
			def print_mismatch(mismatch_type=""):
				if random() <= sampling_rate:
					print ",".join([str(k) for k in [mismatch_type, expected_country, result_country, expected_postal_code, result_postal_code, point[0][0], point[0][1], ret_val[i]["lat"], ret_val[i]["lon"], LatLon(point[0][0], point[0][1]).distance(LatLon(ret_val[i]["lat"], ret_val[i]["lon"])), point[1]]])
					sys.stdout.flush()

			if not expected_country and result_country:
				counts["country_new"] += 1
			elif result_country != expected_country:
				print_mismatch("c")
				counts["country_mismatch"] += 1
			elif result_country == expected_country:
				counts["country_match"] += 1


			if not expected_postal_code and result_postal_code:
				counts["postal_code_new"] += 1
			elif result_postal_code != expected_postal_code:
				# print result_postal_code, expected_postal_code, expected_country
				counts["postal_code_mismatch"] += 1
				print_mismatch("p")
			elif result_postal_code == expected_postal_code:
				counts["postal_code_match"] += 1

		# else:
			# counts["filtered"] += 1


	counts["total"] = i+1
	return counts


for thresh in xrange(1, 5):

	thresh = thresh * 0.2
	# print thresh
	total_counts = dict()
	fin = open("../dumps/geo/poi/aggregate")
	points = list()
	results = list()
	start = time.time()
	for i, row in enumerate(fin):
		row = row.strip().split("\t")
		_hash = int(row[0])
		points.append((geo_hash.from_ord(_hash), row[1]))

		if len(points) >= chunk_size:
			results = compare(points, False, thresh)
			# print i, count, delta
			for key in set(results.keys() + total_counts.keys()):
				total_counts[key] = total_counts.get(key, 0) + results.get(key, 0)
			points = list()
			# print results

	if points:
		results = compare(points, False, thresh)
		# print i, count, delta
		for key in set(results.keys() + total_counts.keys()):
			total_counts[key] = total_counts.get(key, 0) + results.get(key, 0)
		points = list()
		# if i % 100000 == 0:
			# print i, total_counts

	end = time.time()
	# print "Total: %s %s" %(i, end - start)
	print thresh, end - start,total_counts