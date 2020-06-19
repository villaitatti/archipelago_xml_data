from xml.dom import minidom as md, getDOMImplementation
import xml.etree.ElementTree as et
import os
import json

dir_path = os.path.dirname(os.path.realpath(__file__))
filename = os.path.join(dir_path, 'Events.xml')
# Geonames dictionary
geonames_dict = json.load(open(os.path.join(dir_path, 'archipelago_geonames.json'), 'r'))


def write_file(text):
    output_directory = os.path.join(dir_path)
    if not os.path.isdir(output_directory):
        os.mkdir(output_directory)
    output_filename = os.path.join(output_directory, 'Events_processed.xml')
    with open(output_filename, 'w') as f:
        f.write(text)


def add_clean_field(input_key):
    field = et.SubElement(new_row, input_key)
    field.text = row.find(f'ns:{input_key}', ns).text


keys = {
    "row": "ROW",
    "id_event": "ID_EVENT",
    "name_event": "Name_Event",
    "typology": "Typology",
    "subtypology": "Subtypology",
    "island": "Island",
    "synopsis": "Synopsis",
    "century": "Century",
    "fraction_century": "Fraction_century",
    "year_earliest": "Year_Earliest",
    "month_earliest": "Month_Earliest",
    "day_earliest": "Day_Earliest"
}

custom_keys = {
    "date_earliest": "Date_Earliest"
}

exceptions = {
    "Lagoon": "Lagoon of Venice, bassi fondali",
    "San Giorgio Maggiore": "Isola di San Giorgio Maggiore"
 }

tree = et.parse(filename)
root = tree.getroot()
ns = {'ns': 'http://www.filemaker.com/fmpdsoresult'}

tags = root.findall(f'ns:{keys["row"]}', ns)

doc = md.Document()

new_document_root = et.Element('FMPDSORESULT', ns)

# Iterate each ROW
for row in tags:
    # Copy the current row
    new_row = et.Element(keys["row"])

    # ROW ID
    row_id = row.find(f'ns:{keys["id_event"]}', ns).text
    id_event = et.SubElement(new_row, keys["id_event"])
    id_event.text = row_id

    # Add clean fields
    add_clean_field(keys["name_event"])
    add_clean_field(keys["typology"])
    add_clean_field(keys["subtypology"])
    add_clean_field(keys["synopsis"])
    add_clean_field(keys["century"])
    add_clean_field(keys["fraction_century"])

    # Add Custom Fields
    # Date_Earliest
    day_earliest = row.find(f'ns:{keys["day_earliest"]}', ns).text
    if day_earliest is None:
        day_earliest = "01"
    month_earliest = row.find(f'ns:{keys["month_earliest"]}', ns).text
    if month_earliest is None:
        month_earliest = "01"
    year_earliest = row.find(f'ns:{keys["year_earliest"]}', ns).text
    # TODO: decide date format
    date_earliest = et.SubElement(new_row, custom_keys["date_earliest"])
    date_earliest.text = f'{day_earliest}-{month_earliest}-{year_earliest}'

    # Island
    island_found = row.find(f'ns:{keys["island"]}', ns).text
    # TODO: better management of exceptions?
    if island_found not in geonames_dict:
        island_found = exceptions[island_found]
    isl_geoname_id = geonames_dict[island_found][0]["geoname_id"]
    island = et.SubElement(new_row, keys["island"])
    island.text = isl_geoname_id

    new_document_root.append(new_row)


final = md.parseString(et.tostring(new_document_root, method='xml')).toprettyxml()
write_file(final)
