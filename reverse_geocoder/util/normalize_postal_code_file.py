import sys
import csv


def process(output_file):
    raise Exception("Not implemented.")


def process_file(input_file, output_file):
    """
        output schema:
            lat,lon,name,admin1,admin2,cc,pc
            9,10,2,4,6,0,1

        input schema:
            0,country code      : iso country code, 2 characters [cc]
            1,postal code       : varchar(20) [pc]
            2,place name        : varchar(180) [name]
            3,admin name1       : 1. order subdivision (state) varchar(100) [admin1]
            4,admin code1       : 1. order subdivision (state) varchar(20) [admin2]
            5,admin name2       : 2. order subdivision (county/province) varchar(100)
            6,admin code2       : 2. order subdivision (county/province) varchar(20)
            7,admin name3       : 3. order subdivision (community) varchar(100)
            8,admin code3       : 3. order subdivision (community) varchar(20)
            9,latitude          : estimated latitude (wgs84)
            10,longitude         : estimated longitude (wgs84)
            11,accuracy          : accuracy of lat/lng from 1=estimated to 6=centroid
        sample input:
        AD  AD100   Canillo                         42.5833 1.6667  6
        AD  AD200   Encamp                          42.5333 1.6333  6
        AD  AD300   Ordino                          42.6    1.55    6
        AD  AD400   La Massana                          42.5667 1.4833  6
        AD  AD500   Andorra la Vella                            42.5    1.5 6
    """
    print "Processing postal code file: %s" % input_file
    print "Writing to: %s" % output_file

    fin = csv.reader(open(input_file), delimiter="\t")
    fout = csv.writer(open(output_file, "w"))

    fout.writerow("lat,lon,name,admin1,admin2,cc,pc".split(","))
    for i, row in enumerate(fin):
        fout.writerow([row[9],row[10],row[2],row[4],row[6],row[0],row[1]])
        if i % 10000 == 0:
            print "Processed %s rows of data." % i

    print "Total rows processed: %s" % i

if __name__ == "__main__":
    if len(sys.argv) == 3:
        process_file(sys.argv[1], sys.argv[2])
    elif len(sys.argv) == 2:
        process(sys.argv[1])
    else:
        print """Usage:
                    offline -> <input_file> <output_file>
                    online  -> <output_file>"""