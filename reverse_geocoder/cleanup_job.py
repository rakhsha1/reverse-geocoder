from reverse_geocoder import search
import boto3
from geo_hash import from_ord
import os
import sys


S3_CONFIG = dict(
    AWS_ACCESS_KEY_ID = sys.argv[1]
    , AWS_SECRET_ACCESS_KEY = sys.argv[2]
    , SOURCE_BUCKET="geoinfo"
    , SOURCE_PATH="geoindex-data/latest"
    , SINK_BUCKET="geoinfo"
    , SINK_PATH="complete"
)


client = boto3.client(
    's3',
    aws_access_key_id=S3_CONFIG["AWS_ACCESS_KEY_ID"],
    aws_secret_access_key=S3_CONFIG["AWS_SECRET_ACCESS_KEY"]
)

paginator = client.get_paginator('list_objects')
page_iterator = paginator.paginate(Bucket=S3_CONFIG["SOURCE_BUCKET"], Prefix=S3_CONFIG["SOURCE_PATH"])
existing =  paginator.paginate(Bucket=S3_CONFIG["SINK_BUCKET"], Prefix=S3_CONFIG["SINK_PATH"])

base_dir = "/tmp"

keys = set()
for page in page_iterator:
    print page
    # import sys. 
    for content in page["Contents"]:
        keys.add(content["Key"].strip())


existing_keys = set()

for page in existing:
    for content in page.get("Contents", []):
        existing_keys.add(content["Key"].strip().split("/")[-1])

print existing_keys

mappings = {
    "GRAND CAYMAN, CAYMAN ISLANDS": "ky",
    "ECUADOR": "ec", 
    "UAE": "ae"
}

def get_content(key):
    client = boto3.client(
        's3',
        aws_access_key_id=S3_CONFIG["AWS_ACCESS_KEY_ID"],
        aws_secret_access_key=S3_CONFIG["AWS_SECRET_ACCESS_KEY"]
    )
    return client.get_object(Bucket=S3_CONFIG["SOURCE_BUCKET"], Key=key)["Body"]

for j, key in enumerate(keys):

    try:
        rows = []
        points = []
        okey = "%s %s %s" % (j, int(float(j) / len(keys) * 100), key)
        print "Processing -> %s" % okey 
        sys.stdout.flush()

        if key.split("/")[-1] in existing_keys:
            print "Skipping -> %s" % okey 
            sys.stdout.flush()
            continue

        for row in get_content(key).read().split("\n"):
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
                sys.stdout.flush()

        if rows:
            print "Searching %s" % okey
            sys.stdout.flush()
            ret_vals = search(points, max_distance=4)
            file_name = "%s/%s" %(base_dir, key.split("/")[-1])
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
                content[4] = country_code.upper()
                fout.write("%s\t%s\n" %(_hash, chr(0001).join(content)))

            fout.close()
            print "Uploading %s" % okey
            sys.stdout.flush()
            # client.put_object(Bucket=S3_CONFIG["SINK_BUCKET"], Key="%s/%s" %(S3_CONFIG["SINK_PATH"], key.split("/")[-1]), Body=open(file_name, 'rb'))
            os.remove(file_name)
    except Exception, e:
        print "Error %s" % key
        print e
        sys.stdout.flush()
