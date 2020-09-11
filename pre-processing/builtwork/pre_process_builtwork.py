import pandas as pd
import numpy as np
import xml.dom.minidom as md
import xml.etree.ElementTree as et
import os
import re
import json

# TODO pass the file as arg
dir_path = os.path.dirname(os.path.realpath(__file__))
filename = os.path.join(dir_path, 'SS_BLDG_01.csv')

bw_typologies_filename = os.path.join(dir_path, 'dict', 'bw_typologies.tsv')
bw_uses_filename = os.path.join(dir_path, 'dict', 'bw_uses.tsv')
bw_materials_filename = os.path.join(dir_path, 'dict', 'bw_materials.tsv')
bw_islands_filename = os.path.join(dir_path, 'dict', 'bw_islands.tsv')

# Geonames dictionary
geonames_dict = json.load(open(os.path.join(dir_path, '../geonames/', 'geonames.json'), 'r'))

bw_typologies = pd.read_csv(bw_typologies_filename, sep='\t').reset_index().to_json(orient='records')
bw_uses = pd.read_csv(bw_uses_filename, sep='\t').reset_index().to_json(orient='records')
bw_materials = pd.read_csv(bw_materials_filename, sep='\t').reset_index().to_json(orient='records')
bw_islands = pd.read_csv(bw_islands_filename, sep='\t').reset_index().to_json(orient='records')

def write_file(name, text, ext='xml'):

  output_directory = os.path.join(dir_path, '../..', 'transformation/builtwork/' ,'data')

  if not os.path.isdir(output_directory):
    os.mkdir(output_directory)

  output_filename = os.path.join(output_directory, f'{name}.{ext}')

  with open(output_filename, 'w') as f:
    f.write(text)

def base_tag(parent, key, text):
  text = str(text)
  tmp = et.SubElement(parent, key)
  if not re.match(r'^2019-12-31$', text):
    tmp.text = text

def get_bw_use(name):
  for bw_use in json.loads(bw_uses):
    if name == bw_use.get(key_json_name):
      return bw_use

  return None

def get_bw_typology(name):

  for bw_typology in json.loads(bw_typologies):
    if name == bw_typology.get(key_json_name):
      return bw_typology

  return None

def get_bw_material(name):
  for bw_material in json.loads(bw_materials):
    if name == bw_material.get(key_json_name):
      return bw_material

  return None

def get_bw_island(name):
  for bw_island in json.loads(bw_islands):
    if name == bw_island.get(key_json_name):
      return bw_island

  return None

# Input keys
key_root = 'root'
key_row = 'row'
key_wkt = 'WKT'
key_bw_id = 'BW_ID'
key_islandname = 'IslandName'
key_date = 'Date'
key_start = 'Start'
key_end = 'End'
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
key_functions = 'Functions'
key_uses = 'Uses'
key_typologies = 'Typologies'
key_owners = 'Owners'
key_tenants = 'Tenants'
key_eng = 'eng'
key_ita = 'ita'
key_aat = 'aat'
key_geo = 'geo'

# JSON keys
key_json_aat = 'AAT ID'
key_json_name = 'NAME'
key_json_url = 'URL'
key_json_ita = 'ITA'
key_json_geonames = 'Geonames ID'

df = pd.read_csv(filename, sep='\t')

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
  island = et.SubElement(xml_row, key_islandname)

  current_island = get_bw_island(first[key_islandname])

  base_tag(island, key_ita,  current_island.get(key_json_name))
  base_tag(island, key_geo,  current_island.get(key_json_geonames))

  # Start_Earliest 
  base_tag(xml_row, key_start,  first[key_start])

  # End_Latest 
  base_tag(xml_row, key_end,  first[key_end])

  # Name 
  base_tag(xml_row, key_name,  first[key_name])

  """
  # Function 
  base_tag(xml_row, key_function,  first[key_function])

  # Start_Function 
  base_tag(xml_row, key_function_start,  first[key_function_start])

  # End_Function
  base_tag(xml_row, key_function_end,  first[key_function_end])
  """

  # Height
  base_tag(xml_row, key_height,  first[key_height])

  # Material
  text_materials = first[key_material] 

  if text_materials is not None:
    text_materials = text_materials.split(';')

    materials = et.SubElement(xml_row, key_materials)

    for text_material in text_materials:
      material = et.SubElement(materials, key_material)

      current_material = get_bw_material(text_material)

      base_tag(material, key_eng, current_material.get(key_json_name))
      base_tag(material, key_ita, current_material.get(key_json_ita))
      base_tag(material, key_aat, current_material.get(key_json_aat))

  # Architect
  base_tag(xml_row, key_architect,  first[key_architect])

  # Patron
  base_tag(xml_row, key_patron,  first[key_patron])

  # SHP_Lenght
  # base_tag(xml_row, key_shape_lenght,  first[key_shape_lenght])

  # SHP_Area
  # base_tag(xml_row, key_shape_area,  first[key_shape_area])

  set_uses = dict()
  set_typologies = dict()
  set_owners = dict()
  set_tenants = dict()
  set_functions = dict()

  # Not shared elements
  for current_bw in builtworks[bw_id]:

    # Function
    if current_bw[key_function] not in set_functions:
      set_functions[current_bw[key_function]] = {key_function_start: current_bw[key_function_start], key_function_end: current_bw[key_function_end]}

    # Use
    if current_bw[key_use] not in set_uses and current_bw[key_use]:
      set_uses[current_bw[key_use]] = {key_use_start: current_bw[key_use_start], key_use_end: current_bw[key_use_end]}

    # Typologies
    if current_bw[key_typology] not in set_typologies and current_bw[key_typology]:
      set_typologies[current_bw[key_typology]] = {key_typology_start: current_bw[key_typology_start], key_typology_end: current_bw[key_typology_end]}

    # Owners
    if current_bw[key_owner] not in set_owners and current_bw[key_owner]:
      set_owners[current_bw[key_owner]] = {key_owner_start: current_bw[key_owner_start], key_owner_end: current_bw[key_owner_end]}

    # Tenants
    if current_bw[key_tenant] not in set_tenants and current_bw[key_tenant]:
      set_tenants[current_bw[key_tenant]] = {key_tenant_start: current_bw[key_tenant_start], key_tenant_end: current_bw[key_tenant_end]}

  # Function
  functions = et.SubElement(xml_row, key_functions)
  for key, function in set_functions.items():

    function_tag = et.SubElement(functions, key_function)

    base_tag(function_tag, key_name, key)
    base_tag(function_tag, key_function_start, function[key_function_start])
    base_tag(function_tag, key_function_end, function[key_function_end])


  # Use
  uses = et.SubElement(xml_row, key_uses)
  for key, use in set_uses.items():

    use_tag = et.SubElement(uses, key_use)

    current_use = get_bw_use(key)

    base_tag(use_tag, key_eng, current_use.get(key_json_name))
    base_tag(use_tag, key_ita, current_use.get(key_json_ita))
    base_tag(use_tag, key_aat, current_use.get(key_json_aat))

    base_tag(use_tag, key_use_start, use[key_use_start])
    base_tag(use_tag, key_use_end, use[key_use_end])

  # Typologies
  typologies = et.SubElement(xml_row, key_typologies)
  for key, typology in set_typologies.items():

    typology_tag = et.SubElement(typologies, key_typology)

    current_typology = get_bw_typology(key)

    base_tag(typology_tag, key_eng, current_typology.get(key_json_name))
    base_tag(typology_tag, key_ita, current_typology.get(key_json_ita))
    base_tag(typology_tag, key_aat, str(int(current_typology.get(key_json_aat))))

    base_tag(typology_tag, key_typology_start, typology[key_typology_start])
    base_tag(typology_tag, key_typology_end, typology[key_typology_end])

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