import csv
import json

jason = {}
accepted_feature_codes = ["PPLA", "PPLA2", "PPLA3"]

with open('geonames_it.tsv') as f:
    for row in csv.DictReader(f, delimiter='\t'):
        geoname_id = row["geoname_id"]
        name = row["name"]
        feature_code = row["feature_code"]
        admin2_code = row["admin2_code"]
        latitude = row["latitude"]
        longitude = row["longitude"]

        #Get only geonames for:
            #1: Islands or Lagoon in VE (Provincia di venezia)
            #2: Cities in italy = PPLA (città capoluoghi), PPLA2 (città capoluogo di provincia), PPLA3(città comune)
        if ((feature_code == "ISL" or feature_code == "LGN") and admin2_code == "VE") or feature_code in accepted_feature_codes:
            if not name in jason:
                jason[name] = []
            place_object = {}
            place_object["geoname_id"] = geoname_id
            place_object["feature_code"] = feature_code
            place_object["latitude"] = latitude
            place_object["longitude"] = longitude
            jason[name].append(place_object)

with open('geonames.json', 'w') as fp:
    json.dump(jason, fp)