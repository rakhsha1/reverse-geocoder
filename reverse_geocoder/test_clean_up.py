from reverse_geocoder import search
import boto3
from geo_hash import from_ord
import os
import sys
from collections import defaultdict

mappings = {
    "GRAND CAYMAN, CAYMAN ISLANDS": "ky",
    "ECUADOR": "ec", 
    "UAE": "ae"
}

# base_dir = "/data/geo"
base_dir = "/Users/ali/icode/dumps"
raw = "raw"
out = "mod"

raw_dir = "%s/%s" %(base_dir, raw)
out_dir = "%s/%s" %(base_dir, out)

update = 0
counts = defaultdict(int)

for file_name in os.listdir(raw_dir):

    fin = open("%s/%s" %(raw_dir, file_name))
    rows = []
    points = []

    for row in fin:
        row = row.strip()
        if not row: 
            continue
        try:
            first = row.split("\t")
            _hash = int(first[0])
            rows.append(row)
            points.append(from_ord(_hash))
        except IndexError, e:
            print "IndexError: %s" % row
            sys.sdout.flush()

    if rows:
        ret_vals = search(points, max_distance=1)
        file_name = "%s/%s" %(out_dir, file_name)
        fout = open(file_name, "w")
        for i, row in enumerate(rows):
            ret_val = ret_vals[i] or {}
            first = row.split("\t")
            _hash = first[0]
            content = first[1].split(chr(0001))
            postal_code = ret_val.get("pc", "") or content[3] 
            country_code = ret_val.get("cc", "").upper() or content[4]
            if len(country_code) > 2:
                cc = mappings.get(country_code)
                if cc: 
                    country_code = cc 
                    
            content[3] = postal_code
            
            if content[4] != country_code.upper():
                print "%s -> %s" %(content[4], country_code.upper())
                update += 1
                counts[content[4]] += 1

            content[4] = country_code.upper()

            fout.write("%s\t%s\n" %(_hash, chr(0001).join(content)))

        fout.close()


print "Mismatch counts %s" % update
for k, v in counts.iteritems():
    print "%s: %s" % (k, v)
