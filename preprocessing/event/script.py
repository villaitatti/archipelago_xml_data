from xml.dom import minidom as md, getDOMImplementation
import xml.etree.ElementTree as et
import os
import json
import re


def execute(limit):
    t = 'event'

    dir_path = os.path.dirname(os.path.realpath(__file__))
    root_path = os.path.join(dir_path, os.path.pardir, os.path.pardir)
    filename = os.path.join(dir_path, 'Events.xml')
    # Geonames dictionary
    geonames_dict = json.load(
        open(os.path.join(root_path, 'utils', 'geonames', 'geonames.json'), 'r'))
    association_tables = json.load(open(os.path.join(
        root_path, 'utils', 'association_tables', 'association_tables.json'), 'r'))

    def write_file(text):
        output_directory = os.path.join(root_path, 'transformation', t, 'data')
        if not os.path.isdir(output_directory):
            os.mkdir(output_directory)
        output_filename = os.path.join(output_directory, f'{row_id}.xml')
        with open(output_filename, 'w') as f:
            f.write(text)

    def add_clean_field(input_key):
        field = et.SubElement(new_row, input_key)
        field.text = row.find(f'ns:{input_key}', ns).text

    regex_century_id = r'[0-9]{2}-[0-9]{2}'

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
        "day_earliest": "Day_Earliest",

        "people": "People",
        "person": "Person",
        "id_person": "ID_PERSON",
        "role": "Role",

        "bibliographic_items": "Bibliographic_Items",
        "bibliographic_item": "Bibliographic_Item",
        "id_bibliography": "ID_BIBLIOGRAPHY",
        "date": "Date",
        "pages": "Pages",

        "places": "Places",
        "place": "Place",
        "id_place": "ID_PLACE",

        "sources": "Sources",
        "source": "Source",
        "id_source": "ID_SOURCE",
        "event": "Event",

        "fraction_id": "fraction_id",
    }

    custom_keys = {
        "date_earliest": "Date_Earliest"
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

    cnt_total = 0

    # Iterate each ROW
    for row in tags:

        if limit and cnt_total == int(cnt_total):
            break

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

        century_fraction = row.find(f'ns:{keys["fraction_century"]}', ns).text
        if century_fraction is not None and re.search(regex_century_id, str(century_fraction)):
            f_century = et.SubElement(new_row, keys["fraction_century"])
            f_century.text = century_fraction

            r = re.search(regex_century_id, str(century_fraction))[0]
            f_century.attrib[keys['fraction_id']] = r.replace('-', '')

        # Add Custom Fields
        # Date_Earliest
        day_earliest = row.find(f'ns:{keys["day_earliest"]}', ns).text
        if day_earliest is None:
            day_earliest = "01"
        month_earliest = row.find(f'ns:{keys["month_earliest"]}', ns).text
        if month_earliest is None:
            month_earliest = "01"
        year_earliest = row.find(f'ns:{keys["year_earliest"]}', ns).text
        # Date format: YYYY-MM-DDThh:mm:ss (xsd:datetime)
        date_earliest = et.SubElement(new_row, custom_keys["date_earliest"])
        date_earliest.text = f'{year_earliest}-{month_earliest}-{day_earliest}'

        # Island
        island_found = row.find(f'ns:{keys["island"]}', ns).text
        # TODO: better management of exceptions?
        if island_found not in geonames_dict:
            island_found = exceptions[island_found]
        isl_geoname_id = geonames_dict[island_found][0]["geoname_id"]
        island = et.SubElement(new_row, keys["island"])
        island.text = isl_geoname_id

        # ASSOCIATIONS

        # People
        people = et.SubElement(new_row, keys["people"])
        if row_id in association_tables['events']:
            for k, v in association_tables['events'][row_id]['people'].items():
                person = et.SubElement(people, keys["person"])
                person_id = et.SubElement(person, keys["id_person"])
                person_id.text = k
                role = et.SubElement(person, keys["role"])
                role.text = v[keys['role']]

        # Bibliograpic items
        bibliographic_items = et.SubElement(
            new_row, keys["bibliographic_items"])
        if row_id in association_tables['events']:
            for k, v in association_tables['events'][row_id]['bibliography'].items():
                bibliographic_item = et.SubElement(
                    bibliographic_items, keys["bibliographic_item"])
                bibliography_id = et.SubElement(
                    bibliographic_item, keys["id_bibliography"])
                bibliography_id.text = k
                date = et.SubElement(bibliographic_item, keys["date"])
                date.text = v[keys['date']]
                pages = et.SubElement(bibliographic_item, keys["pages"])
                pages.text = v[keys['pages']]

        # Places
        places = et.SubElement(new_row, keys["places"])
        if row_id in association_tables['events']:
            for k, v in association_tables['events'][row_id]['places'].items():
                place = et.SubElement(places, keys["place"])
                place_id = et.SubElement(place, keys["id_place"])
                place_id.text = k

                date = et.SubElement(place, keys["date"])
                date.text = v[keys['date']]

        # Sources
        sources = et.SubElement(new_row, keys["sources"])
        if row_id in association_tables['events']:
            for k, v in association_tables['events'][row_id]['sources'].items():
                source = et.SubElement(sources, keys["source"])
                source_id = et.SubElement(source, keys["id_source"])
                source_id.text = k

                event = et.SubElement(source, keys["event"])
                event.text = v[keys['event']]

        # new_document_root.append(new_row)

        final = md.parseString(et.tostring(
            new_row, method='xml')).toprettyxml()
        write_file(final)
        cnt_total += 1
