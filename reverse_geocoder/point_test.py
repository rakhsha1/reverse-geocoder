

from geo_hash import from_ord 
from reverse_geocoder import search

points = [1028940903367840592, 1028940741691456133, 1028940714896802299, 1028937300827959104, 1028936919208416560, 1028936496796163181, 1028936321951596184]

for point in points:
	coords = from_ord(point)
	print point, coords
	result = search(coords, max_distance=1)

	print coords, result



coords = (43.646964, -79.455647)
result = search(coords, max_distance=1)

print coords, result

coords = (43.6469, -79.4521)
result = search(coords, max_distance=1)

print coords, result
