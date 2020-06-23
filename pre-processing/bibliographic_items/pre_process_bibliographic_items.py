from xml.dom import minidom as md, getDOMImplementation
import xml.etree.ElementTree as et
import os
import json
import dateutil.parser
from datetime import datetime


dir_path = os.path.dirname(os.path.realpath(__file__))
filename = os.path.join(dir_path, '../../export/transformed/Bibliographic_Items.xml')
# Geonames dictionary
geonames_dict = json.load(open(os.path.join(dir_path, '../geonames/', 'geonames.json'), 'r'))


def write_file(text):
    output_directory = os.path.join(dir_path, '../..', 'transformation/bibliographic_items/' ,'data')
    if not os.path.isdir(output_directory):
        os.mkdir(output_directory)
    output_filename = os.path.join(output_directory, f'{row_id}.xml')
    with open(output_filename, 'w') as f:
        f.write(text)


def add_clean_field(input_key):
    field = et.SubElement(new_row, input_key)
    field.text = row.find(f'ns:{input_key}', ns).text


keys = {
    "row": "ROW",
    "id_event": "ID_BIBLIOGRAPHY",
    "typology": "Typology",
    "author": "Author",
    "title": "Title",
    "language": "Language",
    "curator": "Curator",
    "publisher": "Publisher",
    "city": "City",
    "date": "Date",
    "book_or_journal_title": "Book_or_Journal_Title",
    "series": "Series",
    "journals_number": "Journal_Number",
    "n_volume": "N_Volume",
    "volume_title": "Volume_Title",
    "pages": "Pages",
    "subject": "Subject",
}

custom_keys = {
    "date_earliest": "Date_Earliest"
}

exceptions = {}

tree = et.parse(filename)
root = tree.getroot()
ns = {'ns': 'http://www.filemaker.com/fmpdsoresult'}

tags = root.findall(f'ns:{keys["row"]}', ns)

doc = md.Document()

#new_document_root = et.Element('FMPDSORESULT', ns)

# Iterate each ROW
for row in tags:
    # Copy the current row
    new_row = et.Element(keys["row"])

    # ROW ID
    row_id = row.find(f'ns:{keys["id_event"]}', ns).text
    id_event = et.SubElement(new_row, keys["id_event"])
    id_event.text = row_id

    # Add clean fields
    add_clean_field(keys["id_event"])
    add_clean_field(keys["typology"])
    add_clean_field(keys["author"])
    add_clean_field(keys["title"])
    add_clean_field(keys["language"])
    add_clean_field(keys["curator"])
    add_clean_field(keys["publisher"])
    add_clean_field(keys["book_or_journal_title"])
    add_clean_field(keys["series"])
    add_clean_field(keys["journals_number"])
    add_clean_field(keys["n_volume"])
    add_clean_field(keys["volume_title"])
    add_clean_field(keys["pages"])
    add_clean_field(keys["subject"])

    # Add Custom Fields
    # Date
    # Date format: YYYY-MM-DDThh:mm:ss (xsd:datetime)
    date = et.SubElement(new_row, keys["date"])
    date_raw = row.find(f'ns:{keys["date"]}', ns).text
    #print(f"Raw: {date_raw}")
    date_clean = dateutil.parser.parse(date_raw).strftime("%m-%d-%YT%H:%M:%S")
    #print(f"Clean: {date_clean}")
    date.text = date_clean

    # City
    city_found = row.find(f'ns:{keys["city"]}', ns).text
    if city_found is None:
        city_geoname_id = ""
    else:
        if city_found not in geonames_dict:
            city_found = exceptions[city_found]
        city_geoname_id = geonames_dict[city_found][0]["geoname_id"]
    city = et.SubElement(new_row, keys["city"])
    city.text = city_geoname_id


    #new_document_root.append(new_row)
    final = md.parseString(et.tostring(new_row, method='xml')).toprettyxml()
    write_file(final)
print("Done.")