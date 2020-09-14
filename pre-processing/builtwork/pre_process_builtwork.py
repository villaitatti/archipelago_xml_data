import pandas as pd
import numpy as np
import xml.dom.minidom as md
import xml.etree.ElementTree as et
import os
import re
import json

# TODO pass the file as arg
dir_path = os.path.dirname(os.path.realpath(__file__))
filename = os.path.join(dir_path, 'buildings.csv')

bw_typologies_filename = os.path.join(dir_path, 'dict', 'bw_typologies.tsv')
bw_uses_filename = os.path.join(dir_path, 'dict', 'bw_uses.tsv')
bw_materials_filename = os.path.join(dir_path, 'dict', 'bw_materials.tsv')
bw_islands_filename = os.path.join(dir_path, 'dict', 'bw_islands.tsv')

# Geonames dictionary
geonames_dict = json.load(open(os.path.join(dir_path, os.path.pardir, 'geonames', 'geonames.json'), 'r'))
people_dict = json.load(open(os.path.join(dir_path, os.path.pardir, 'people', 'people.json'), 'r'))

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

def get_person(name):
  for person in people_dict:
    current_name = re.sub(r'{.*}','',person.get(key_surname)).strip()
    if name.lower() == current_name.lower():
      return person

  return None

def add_person(parent, key):
  current_person = get_person(key)
  if current_person is not None:
    base_tag(parent, key_person_id, current_person.get(key_person_id))

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
key_architects = 'Architects'
key_patrons = 'Patrons'
key_eng = 'eng'
key_ita = 'ita'
key_aat = 'aat'
key_geo = 'geo'
key_person_id = 'ID_PERSON'

# JSON keys
key_json_aat = 'AAT ID'
key_json_name = 'NAME'
key_json_url = 'URL'
key_json_ita = 'ITA'
key_json_geonames = 'Geonames ID'
key_surname = 'Surname'

df = pd.read_csv(filename, sep='\t')

builtworks = {}

def clear(val):
  if val is np.nan or val == 'nan': 
    val = ""
  return val

# Create a dict with an array containing every bw as json object
for i in range(len(df)) :
  row_id = df.loc[i, key_bw_id]

  if row_id not in builtworks:
    builtworks[row_id] = {}

  for y in range(1, len(df.columns)):
    val = clear(df.iloc[i, y])
    col = df.columns[y]

    # Append material as list
    if col == key_patron:

      if builtworks[row_id].get(key_patron) is None:
        builtworks[row_id][key_patron] = set()
      
      builtworks[row_id][key_patron].add(val)

    else:
      builtworks[row_id][col] = val

for bw_id, bw in builtworks.items():

  # Create the current row
  xml_row = et.Element(key_row)

  row_date = bw.get(key_date)

  # Shared elements

  # bw id
  base_tag(xml_row, key_bw_id, bw_id)

  # IslandName
  island = et.SubElement(xml_row, key_islandname)

  current_island = get_bw_island(bw.get(key_islandname))

  base_tag(island, key_ita,  current_island.get(key_json_name))
  base_tag(island, key_geo,  current_island.get(key_json_geonames))

  # Start_Earliest 
  base_tag(xml_row, key_start,  bw.get(key_start))

  # End_Latest 
  base_tag(xml_row, key_end,  bw.get(key_end))

  # Name 
  base_tag(xml_row, key_name,  bw.get(key_name))

  # Height
  base_tag(xml_row, key_height,  bw.get(key_height))

  # Material
  text_materials = bw.get(key_material)

  if text_materials is not None:
    text_materials = text_materials.split(';')

    materials = et.SubElement(xml_row, key_materials)

    for text_material in text_materials:
      material = et.SubElement(materials, key_material)

      current_material = get_bw_material(text_material)

      try:
        base_tag(material, key_eng, current_material.get(key_json_name))
      except AttributeError as err:
        pass
      
      try:
        base_tag(material, key_ita, current_material.get(key_json_ita))
      except AttributeError as err:
        pass

      try:
        base_tag(material, key_aat, current_material.get(key_json_aat))
      except AttributeError as err:
        pass

  # SHP_Lenght
  # base_tag(xml_row, key_shape_lenght,  bw[key_shape_lenght])

  # SHP_Area
  # base_tag(xml_row, key_shape_area,  bw[key_shape_area])

  set_uses = dict()
  set_patrons = dict()
  set_architects = dict()
  set_typologies = dict()
  set_owners = dict()
  set_tenants = dict()
  set_functions = dict()

  # Function
  if bw.get(key_function) not in set_functions:
    set_functions[bw.get(key_function)] = {key_function_start: bw.get(key_function_start), key_function_end: bw.get(key_function_end)}

  # Use
  if bw.get(key_use) not in set_uses and bw.get(key_use):
    set_uses[bw.get(key_use)] = {key_use_start: bw.get(key_use_start), key_use_end: bw.get(key_use_end)}

  # Typologies
  if bw.get(key_typology) not in set_typologies and bw.get(key_typology):
    set_typologies[bw.get(key_typology)] = {key_typology_start: bw.get(key_typology_start), key_typology_end: bw.get(key_typology_end)}

  # Owners
  if bw.get(key_owner) not in set_owners and bw.get(key_owner):
    set_owners[bw.get(key_owner)] = {key_owner_start: bw.get(key_owner_start), key_owner_end: bw.get(key_owner_end)}

  # Tenants
  if type(bw.get(key_tenant)) is str and bw.get(key_tenant) not in set_tenants:
    set_tenants[bw.get(key_tenant)] = {key_tenant_start: bw.get(key_tenant_start), key_tenant_end: bw.get(key_tenant_end)}

  # Architect
  if type(bw.get(key_architect)) is str and bw.get(key_architect) not in set_architects:
    set_architects[bw.get(key_architect)] = bw.get(key_architect)

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
    #base_tag(typology_tag, key_aat, str(int(current_typology.get(key_json_aat))))

    base_tag(typology_tag, key_typology_start, typology[key_typology_start])
    base_tag(typology_tag, key_typology_end, typology[key_typology_end])

  # Owners
  owners = et.SubElement(xml_row, key_owners)
  for key, owner in set_owners.items():

    owner_tag = et.SubElement(owners, key_owner)

    add_person(owner_tag, key)

    base_tag(owner_tag, key_name, key)
    base_tag(owner_tag, key_owner_start, owner[key_owner_start])
    base_tag(owner_tag, key_owner_end, owner[key_owner_end])

  # Tenants
  tenants = et.SubElement(xml_row, key_tenants)
  for key, tenant in set_tenants.items():

    tenant_tag = et.SubElement(tenants, key_tenant)

    add_person(tenant_tag, key)

    base_tag(tenant_tag, key_name, key)
    base_tag(tenant_tag, key_tenant_start, tenant[key_tenant_start])
    base_tag(tenant_tag, key_tenant_end, tenant[key_tenant_end])

  # Architects
  architects = et.SubElement(xml_row, key_architects)
  for key, architect in set_architects.items():
    architect = et.SubElement(architects, key_architect)

    add_person(architect, key)
    base_tag(architect, key_name, key)

  # Patrons
  patrons = et.SubElement(xml_row, key_patrons)
  for key in bw.get(key_patron):
    patron = et.SubElement(patrons, key_patron)

    add_person(patron, key)
    base_tag(patron, key_name, key)

  final = md.parseString(et.tostring(xml_row, method='xml')).toprettyxml()

  write_file(bw_id, final)