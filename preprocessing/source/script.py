from xml.dom import minidom as md, getDOMImplementation
import xml.etree.ElementTree as et
import os
import csv
import json
import dateutil.parser
import pandas as pd
from datetime import datetime

def execute(limit):

  dir_path = os.path.dirname(os.path.realpath(__file__))
  filename = os.path.join(dir_path, os.pardir, os.pardir, 'extraction/transformed/Sources.xml')
  
  # Geonames dictionary
  #geonames_dict = json.load(open(os.path.join(dir_path, '../geonames/', 'geonames.json'), 'r'))
  association_tables = json.load(open(os.path.join(dir_path, os.pardir, os.pardir, 'utils', 'association_tables', 'association_tables.json'), 'r'))


  def write_file(text):
      output_directory = os.path.join(dir_path, os.pardir, os.pardir, 'transformation/source/' ,'data')
      if not os.path.isdir(output_directory):
          os.mkdir(output_directory)
      output_filename = os.path.join(output_directory, f'{row_id}.xml')
      with open(output_filename, 'w') as f:
          f.write(text)


  def add_clean_field(input_key, tag=None):
    if tag is None:
      field = et.SubElement(new_row, input_key)
    else:
      field = et.SubElement(new_row, tag)

    field.text = row.find(f'ns:{input_key}', ns).text

  KEY_PARENT = 'parents'

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

  #new_document_root = et.Element('FMPDSORESULT', ns)

  archival_units = set()

  def add_archival_unit(unit, type, parent):
    if unit is not None:
      archival_units.add((unit, parent, type))
    

  cnt = 0

  # Iterate each ROW
  for row in tags:

    if limit and cnt == int(limit):
      break

    # Copy the current row
    new_row = et.Element(keys["row"])

    # ROW ID
    row_id = row.find(f'ns:{keys["id_source"]}', ns).text
    id_source = et.SubElement(new_row, keys["id_source"])
    id_source.text = row_id

    # Add clean fields
    add_clean_field(keys["title"], 'attributed_title')
    #add_clean_field(keys["island"])
    #add_clean_field(keys["typology"])
    add_clean_field(keys["format"], 'typology')

    #add_clean_field(keys["author_surname_name"])
    add_clean_field(keys["role_author"])

    add_clean_field(keys["original_title"])
    add_clean_field(keys["language"])

    #add_clean_field(keys["century"])
    #add_clean_field(keys["fraction_century"])
    #add_clean_field(keys["collection"])
    #add_clean_field(keys["acronym"])
    #add_clean_field(keys["fondo"])
    #add_clean_field(keys["busta"])
    #add_clean_field(keys["filza"])
    #add_clean_field(keys["title_filza"])
    #add_clean_field(keys["folio"])
    #add_clean_field(keys["drawing"])
    #add_clean_field(keys["location"])
    #add_clean_field(keys["medium"])
    #add_clean_field(keys["dimensions"])
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

    archival_path = ''

    # Archives
    archive = row.find(f'ns:{keys["collection"]}', ns).text
    if archive is not None:
      archival_path += archive
    
    # Fonds
    fond = row.find(f'ns:{keys["fondo"]}', ns).text 
    if fond is not None:
      archival_path += f' > {fond}'

    # Folder
    folder = row.find(f'ns:{keys["busta"]}', ns).text
    if folder is not None:
      archival_path += f' > {folder}'

    # Filza
    file = row.find(f'ns:{keys["filza"]}', ns).text
    if file is not None:
      archival_path += f' > {file}'
    
    # Folio
    folio = row.find(f'ns:{keys["folio"]}', ns).text
    if folio is not None:
      archival_path += f' > {folio}'

    # Drawing
    drawing = row.find(f'ns:{keys["drawing"]}', ns).text
    if drawing is not None:
      archival_path += f' > {drawing}'

    name = row.find(f'ns:{keys["title"]}', ns).text
    archival_units.add((row_id, archival_path, name))


    

    """
    # Archives
    archive = row.find(f'ns:{keys["collection"]}', ns).text
    parent = None
    add_archival_unit(archive, 'https://archipelago.itatti.harvard.edu/resource/vocab/archive', parent)

    # Fonds
    fond = row.find(f'ns:{keys["fondo"]}', ns).text
    parent = archive
    add_archival_unit(fond, 'https://archipelago.itatti.harvard.edu/resource/vocab/fond', parent)

    # Folder
    folder = row.find(f'ns:{keys["busta"]}', ns).text
    if fond is not None:
      parent = fond
    add_archival_unit(folder, 'https://archipelago.itatti.harvard.edu/resource/vocab/folder', parent)

    # Filza
    file = row.find(f'ns:{keys["filza"]}', ns).text
    if folder is not None:
      parent = folder
    add_archival_unit(file, 'https://archipelago.itatti.harvard.edu/resource/vocab/archival_unit', parent)

    # Folio and Drawing
    if file is not None:
      parent = file 

    folio = row.find(f'ns:{keys["folio"]}', ns).text
    add_archival_unit(folio, 'https://archipelago.itatti.harvard.edu/resource/vocab/folio', parent)

    drawing = row.find(f'ns:{keys["drawing"]}', ns).text
    add_archival_unit(drawing, 'https://archipelago.itatti.harvard.edu/resource/vocab/drawing', parent)
    """

    """
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
    """

    #ASSOCIATIONS

    #Events
    events = et.SubElement(new_row, "EVENTS")
    if row_id in association_tables['sources']:
        for k,v in association_tables['sources'][row_id]['events'].items():
            event = et.SubElement(events, "EVENT")
            event_id = et.SubElement(event, "ID_EVENT")
            event_id.text = k
            event_description = et.SubElement(event, "Event")
            event_description.text = v["Event"]

    #People
    people = et.SubElement(new_row, "PEOPLE")
    if row_id in association_tables['sources']:
        for k,v in association_tables['sources'][row_id]['people'].items():
            person = et.SubElement(people, "PERSON")
            person_id = et.SubElement(person, "ID_PERSON")
            person_id.text = k
            name = et.SubElement(person, "Name")
            name.text = v["Name"]
            surname = et.SubElement(person, "Surname")
            surname.text = v["Surname"]

    #new_document_root.append(new_row)
    final = md.parseString(et.tostring(new_row, method='xml')).toprettyxml()
    write_file(final)

    cnt += 1

  df = pd.DataFrame(list(archival_units), columns=['id', 'path', 'name'])
  df = df.set_index('id')
  df = df.sort_values('path')
  df.to_csv(os.path.join(dir_path, 'archival_units.csv'), quoting=csv.QUOTE_NONNUMERIC)