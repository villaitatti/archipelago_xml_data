import pandas as pd
import numpy as np
import xml.dom.minidom as md
import xml.etree.ElementTree as et
import os
import re
import json

# TODO pass the file as arg
dir_path = os.path.dirname(os.path.realpath(__file__))
filename = os.path.join(dir_path, 'BuiltWork_Buildings.csv')

# Geonames dictionary
geonames_dict = json.load(open(os.path.join(dir_path, '../geonames/', 'geonames.json'), 'r'))

def write_file(name, text, ext='xml'):

  output_directory = os.path.join(dir_path, '../..', 'transformation/builtwork/' ,'data')

  if not os.path.isdir(output_directory):
    os.mkdir(output_directory)

  output_filename = os.path.join(output_directory, f'{name}.{ext}')

  with open(output_filename, 'w') as f:
    f.write(text)

def base_tag(parent, key, text):
  tmp = et.SubElement(parent, key)
  tmp.text = text

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
key_uses = 'Uses'
key_typologies = 'Typologies'
key_owners = 'Owners'
key_tenants = 'Tenants'

df = pd.read_csv(filename, sep=';')

builtworks = {}

# Create a dict with an array containing every bw as json object
for i in range(len(df)) :
  row_id = df.loc[i, key_bw_id]
  new_row = {}

  if row_id not in builtworks:
    builtworks[row_id] = []

  for y in range(1, len(df.columns)):
    val = df.iloc[i, y]
    col = df.columns[y]
    
    if val is np.nan or val == 'nan' or col == key_height: 
      val = ""
      
    new_row[col] = val
  
  builtworks.get(row_id).append(new_row)

#print(builtworks)
#write_file('output', json.dumps(builtworks), ext='json')

cnt_id = 1
bw_id = f'SS_BLDG_{cnt_id:03d}'

while bw_id in builtworks:

  first = builtworks.get(bw_id)[0]

  # Create the current row
  xml_row = et.Element(key_row)

  row_date = first[key_date]

  # Shared elements

  # bw id
  base_tag(xml_row, key_bw_id, bw_id)

  # IslandName 
  base_tag(xml_row, key_islandname,  first[key_islandname])

  # Start_Earliest 
  base_tag(xml_row, key_start,  first[key_start])

  # End_Latest 
  base_tag(xml_row, key_end,  first[key_end])

  # Name 
  base_tag(xml_row, key_name,  first[key_name])

  # Function 
  base_tag(xml_row, key_function,  first[key_function])

  # Start_Function 
  base_tag(xml_row, key_function_start,  first[key_function_start])

  # End_Function
  base_tag(xml_row, key_function_end,  first[key_function_end])

  # Height
  base_tag(xml_row, key_height,  first[key_height])

  # Material
  text_materials = first[key_material] 

  if text_materials is not None:
    text_materials = text_materials.split(';')

    materials = et.SubElement(xml_row, key_materials)

    for text_material in text_materials:
      base_tag(materials, key_material, text_material.strip())

  # Architect
  base_tag(xml_row, key_architect,  first[key_architect])

  # Patron
  base_tag(xml_row, key_patron,  first[key_patron])

  # SHP_Lenght
  base_tag(xml_row, key_shape_lenght,  first[key_shape_lenght])

  # SHP_Area
  base_tag(xml_row, key_shape_area,  first[key_shape_area])

  set_uses = dict()
  set_typologies = dict()
  set_owners = dict()
  set_tenants = dict()

  # Not shared elements
  for current_bw in builtworks[bw_id]:

    # Use
    if current_bw[key_use] not in set_uses:
      set_uses[current_bw[key_use]] = {key_use_start: current_bw[key_use_start], key_use_end: current_bw[key_use_end]}

    # Typologies
    if current_bw[key_typology] not in set_typologies:
      set_typologies[current_bw[key_typology]] = {key_typology_start: current_bw[key_typology_start], key_typology_end: current_bw[key_typology_end]}

    # Owners
    if current_bw[key_owner] not in set_owners:
      set_owners[current_bw[key_owner]] = {key_owner_start: current_bw[key_owner_start], key_owner_end: current_bw[key_owner_end]}

    # Tenants
    if current_bw[key_tenant] not in set_tenants:
      set_tenants[current_bw[key_tenant]] = {key_tenant_start: current_bw[key_tenant_start], key_tenant_end: current_bw[key_tenant_end]}

  # Use
  uses = et.SubElement(xml_row, key_uses)
  for key, use in set_uses.items():

    use_tag = et.SubElement(uses, key_use)

    base_tag(use_tag, key_name, key)
    base_tag(use_tag, key_use_start, use[key_use_start])
    base_tag(use_tag, key_use_end, use[key_use_end])

  # Typologies
  typologies = et.SubElement(xml_row, key_typologies)
  for key, typology in set_typologies.items():

    typology_tag = et.SubElement(typologies, key_typology)

    base_tag(typology_tag, key_name, key)
    base_tag(typology_tag, key_use_start, typology[key_typology_start])
    base_tag(typology_tag, key_use_end, typology[key_typology_end])

  # Owners
  owners = et.SubElement(xml_row, key_owners)
  for key, owner in set_owners.items():

    owner_tag = et.SubElement(owners, key_owner)

    base_tag(owner_tag, key_name, key)
    base_tag(owner_tag, key_owner_start, owner[key_owner_start])
    base_tag(owner_tag, key_owner_end, owner[key_owner_end])

  # Tenants
  tenants = et.SubElement(xml_row, key_tenants)
  for key, tenant in set_tenants.items():

    tenant_tag = et.SubElement(tenants, key_tenant)

    base_tag(tenant_tag, key_name, key)
    base_tag(tenant_tag, key_tenant_start, tenant[key_tenant_start])
    base_tag(tenant_tag, key_tenant_end, tenant[key_tenant_end])

  final = md.parseString(et.tostring(xml_row, method='xml')).toprettyxml()

  write_file(bw_id, final)

  break

  cnt_id += 1
  bw_id = f'SS_BLDG_{cnt_id:03d}'