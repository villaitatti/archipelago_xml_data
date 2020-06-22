import pandas as pd
import xml.dom.minidom as md
import xml.etree.ElementTree as et
import os
import re
import json

# TODO pass the file as arg
dir_path = os.path.dirname(os.path.realpath(__file__))
filename = os.path.join(dir_path, 'builtwork.xml')

# Geonames dictionary
geonames_dict = json.load(open(os.path.join(dir_path, '../geonames/', 'geonames.json'), 'r'))

def write_file(row_id, text):

  output_directory = os.path.join(dir_path, '../..', 'transformation/builtwork/' ,'data')

  if not os.path.isdir(output_directory):
    os.mkdir(output_directory)

  output_filename = os.path.join(output_directory, f'{row_id}.xml')

  with open(output_filename, 'w') as f:
    f.write(text)

def base_tag(parent, key, row):
  tmp = et.SubElement(parent, key)
  tmp.text = row.find(key).text 

# Input keys
key_root = 'root'
key_row = 'row'
key_wkt = 'WKT'
key_bw_id = 'BW_ID'
key_islandname = 'IslandName'
key_date = 'Date'
key_start = 'Start_Earliest'
key_end = 'End_Latest'
key_name = 'Name'

key_function = 'Function'
key_function_start = 'Start_Function'
key_function_end = 'End_Function'

key_use = 'Use'
key_use_start = 'Start_Use'
key_use_end = 'End_Use'

key_typology = 'Typology'
key_typology_start = 'Start_Typology'
key_typology_end = 'End_Typology'

key_height = 'Height'
key_material = 'Material'
key_architect = 'Architect'
key_patron = 'Patron'

key_owner = 'Owner'
key_owner_start = 'Start_Owner'
key_owner_end = 'End_Owner'

key_tenant = 'Tenant'
key_tenant_start = 'Start_Tenant'
key_tenant_end = 'End_Tenant'

key_shape_lenght = 'SHP_Lenght'
key_shape_area = 'SHP_Area'

# Custom created keys
key_materials = 'Materials'

tree = et.parse(filename)
root = tree.getroot()

tags = root.findall(key_row)

# Iterate each ROW
for row in tags:

    # Copy the current row
    new_row = et.Element(key_row)
    row_id = row.find(key_bw_id).text 

    # WKT 
    base_tag(new_row, key_wkt, row)

    # BW_ID
    base_tag(new_row, key_bw_id, row)

    # IslandName 
    base_tag(new_row, key_islandname, row)

    # Date 
    base_tag(new_row, key_date, row)

    # Start_Earliest 
    base_tag(new_row, key_start, row)

    # End_Latest 
    base_tag(new_row, key_end, row)

    # Name 
    base_tag(new_row, key_name, row)

    # Function 
    base_tag(new_row, key_function, row)

    # Start_Function 
    base_tag(new_row, key_function_start, row)

    # End_Function
    base_tag(new_row, key_function_end, row)

    # Use
    base_tag(new_row, key_use, row)

    # Start_Use
    base_tag(new_row, key_use_start, row)

    # End_Use
    base_tag(new_row, key_use_end, row)

    # Typology
    base_tag(new_row, key_typology, row)

    # Start_Typology
    base_tag(new_row, key_typology_start, row)

    # End_Typology
    base_tag(new_row, key_typology_end, row)

    # Height
    base_tag(new_row, key_height, row)

    # Material
    text_materials = row.find(key_material).text 

    if text_materials is not None:
      text_materials = text_materials.split(';')

      materials = et.SubElement(new_row, key_materials)

      for text_material in text_materials:
        material = et.SubElement(materials, key_material)
        material.text = text_material.strip()

    # Architect
    base_tag(new_row, key_architect, row)

    # Patron
    base_tag(new_row, key_patron, row)

    # Owner
    base_tag(new_row, key_owner, row)

    # Start_Owner
    base_tag(new_row, key_owner_start, row)

    # End_Owner
    base_tag(new_row, key_owner_end, row)

    # Tenant
    base_tag(new_row, key_tenant, row)

    # Start_Tenant
    base_tag(new_row, key_tenant_start, row)

    # End_Tenant
    base_tag(new_row, key_tenant_end, row)

    # SHP_Lenght
    base_tag(new_row, key_shape_lenght, row)

    # SHP_Area
    base_tag(new_row, key_shape_area, row)

    final = md.parseString(et.tostring(
        new_row, method='xml')).toprettyxml()

    write_file(row_id, final)
