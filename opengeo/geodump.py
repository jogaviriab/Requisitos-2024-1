import sqlite3
import json
import codecs

conn = sqlite3.connect('opengeo/opengeo.sqlite')
cur = conn.cursor()

cur.execute('SELECT * FROM Locations')
fhand = codecs.open('opengeo/where.js', 'w', "utf-8")
fhand.write("myData = [\n")
count = 0
add = "Universidad Nacional de Colombia 6.26297285 -75.57720175218195"
for row in cur :
    data = str(row[1].decode())
    try: js = json.loads(str(data))
    except: continue

    if len(js['features']) == 0: continue

    try:
        lat = js['features'][0]['geometry']['coordinates'][1]
        lng = js['features'][0]['geometry']['coordinates'][0]
        where = js['features'][0]['properties']['display_name']
        where = where.replace("'", "")
    except:
        print('Unexpected format')
        print(js)

    try :
        print(where, lat, lng)
        count = count + 1
        if count > 1 : fhand.write(",\n")
        output = "["+str(lat)+","+str(lng)+", '"+where+"']"
        fhand.write(output)
    except:
        continue

fhand.write("\n];\n")
cur.close()
fhand.close()
print(add)
print(count, "records written to where.js")
print("Open where.html to view the data in a browser")

