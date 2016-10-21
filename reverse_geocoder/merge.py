import csv


final = csv.writer(open("all_countries_with_postal_code_final.csv", "w"))

original = csv.reader(open("all_countries_with_postal_code_orig.csv"))

all_countries = csv.reader(open("all_countries_with_postal_code.csv"))


countries = set()

for row in all_countries:
	countries.add(row[5])

print "all_countries_with_postal_code.csv contains %s countries." % len(countries)

orig_countries = set()
missing_rows = list()

for row in original:
	if row[5] not in countries:
		orig_countries.add(row[5])
		row.append("")
		missing_rows.append(row)

print "Extracted %s new countries corresponding to %s rows." % (len(orig_countries), len(missing_rows))

for country in countries:
	print country

for country in orig_countries:
	print country

for row in missing_rows:
	final.writerow(row)



