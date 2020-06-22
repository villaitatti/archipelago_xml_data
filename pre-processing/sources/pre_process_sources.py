from xml.dom import minidom as md, getDOMImplementation
import xml.etree.ElementTree as et
import os
import json
import dateutil.parser
from datetime import datetime


dir_path = os.path.dirname(os.path.realpath(__file__))
filename = os.path.join(dir_path, '../../export/transformed/Sources.xml')
# Geonames dictionary
geonames_dict = json.load(open(os.path.join(dir_path, '../geonames/', 'geonames.json'), 'r'))


def write_file(text):
    output_directory = os.path.join(dir_path)
    if not os.path.isdir(output_directory):
        os.mkdir(output_directory)
    output_filename = os.path.join(output_directory, 'Sources_processed.xml')
    with open(output_filename, 'w') as f:
        f.write(text)


def add_clean_field(input_key):
    field = et.SubElement(new_row, input_key)
    field.text = row.find(f'ns:{input_key}', ns).text


keys = {
    "row": "ROW",
    "id_source": "ID_SOURCE",
    "title": "Title",
    "island": "Island",
    "typology": "Typology",
    "format": "Format",
    "language": "Language",
    "author_surname_name": "Author_Surname_Name",
    "role_author": "Role_Author",
    "original_title": "Original_Title",
    "century": "Century",
    "fraction_century": "Fraction_Century",
    "collection": "Collection",
    "acronym": "Acronym",
    "fondo": "Fondo",
    "busta": "Busta",
    "filza": "Filza",
    "title_filza": "Title_Filza",
    "folio": "Folio",
    "drawing": "Drawing",
    "location": "Location",
    "medium": "Medium",
    "dimensions": "Dimensions",
    "synopsis": "Synopsis",
    "trascription": "Trascription",
    "image_container": "Image_Container",
    "year_earliest": "Year_Earliest",
    "month_earliest": "Month_Earliest",
    "day_earliest": "Day_Earliest",
    "year_latest": "Year_Latest",
    "month_latest": "Month_Latest",
    "day_latest": "Day_Latest"
}

custom_keys = {
    "date_earliest": "Date_Earliest",
    "date_latest": "Date_Latest",
}

exceptions = {
    "Lagoon": "Venetian Lagoon",
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
    row_id = row.find(f'ns:{keys["id_source"]}', ns).text
    id_source = et.SubElement(new_row, keys["id_source"])
    id_source.text = row_id

    # Add clean fields
    add_clean_field(keys["title"])
    add_clean_field(keys["island"])
    add_clean_field(keys["typology"])
    add_clean_field(keys["format"])
    add_clean_field(keys["language"])
    add_clean_field(keys["author_surname_name"])
    add_clean_field(keys["role_author"])
    add_clean_field(keys["original_title"])
    add_clean_field(keys["century"])
    add_clean_field(keys["fraction_century"])
    add_clean_field(keys["collection"])
    add_clean_field(keys["acronym"])
    add_clean_field(keys["fondo"])
    add_clean_field(keys["busta"])
    add_clean_field(keys["filza"])
    add_clean_field(keys["title_filza"])
    add_clean_field(keys["folio"])
    add_clean_field(keys["drawing"])
    add_clean_field(keys["location"])
    add_clean_field(keys["medium"])
    add_clean_field(keys["dimensions"])
    add_clean_field(keys["synopsis"])
    add_clean_field(keys["trascription"])

    # Add Custom Fields
    # Date_Earliest
    day_earliest = row.find(f'ns:{keys["day_earliest"]}', ns).text
    if day_earliest is None:
        day_earliest = "01"
    month_earliest = row.find(f'ns:{keys["month_earliest"]}', ns).text
    if month_earliest is None:
        month_earliest = "01"
    year_earliest = row.find(f'ns:{keys["year_earliest"]}', ns).text
    date_earliest_pretty = f'{year_earliest}-{month_earliest}-{day_earliest}T00:00:00'
    if year_earliest is None:
        date_earliest_pretty = ""
    # Date format: YYYY-MM-DDThh:mm:ss (xsd:datetime)
    date_earliest = et.SubElement(new_row, custom_keys["date_earliest"])
    date_earliest.text = date_earliest_pretty

    # Date_Latest
    day_latest = row.find(f'ns:{keys["day_latest"]}', ns).text
    if day_latest is None:
        day_latest = "01"
    month_latest = row.find(f'ns:{keys["month_latest"]}', ns).text
    if month_latest is None:
        month_latest = "01"
    year_latest = row.find(f'ns:{keys["year_latest"]}', ns).text
    date_latest_pretty = f'{year_latest}-{month_latest}-{day_latest}T00:00:00'
    if year_latest is None:
        date_latest_pretty = ""
    # Date format: YYYY-MM-DDThh:mm:ss (xsd:datetime)
    date_latest = et.SubElement(new_row, custom_keys["date_latest"])
    date_latest.text = date_latest_pretty

    # Island
    island_found = row.find(f'ns:{keys["island"]}', ns).text
    if island_found is None:
            isl_geoname_id = ""
    else:
        if island_found not in geonames_dict:
            island_found = exceptions[island_found]
        isl_geoname_id = geonames_dict[island_found][0]["geoname_id"]
    island = et.SubElement(new_row, keys["island"])
    island.text = isl_geoname_id

    new_document_root.append(new_row)


final = md.parseString(et.tostring(new_document_root, method='xml')).toprettyxml()
write_file(final)
print("Done.")