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
  # Block empty and wrong end
  text = str(text)

  if not text or re.match(r'^2019-12-31$', text):
    return
  tag = et.SubElement(parent, key)
  tag.text = text

def get_bw_use(current_use):
  
  if current_use.get(key_use) is not None:
    name = current_use.get(key_use) 
  
  for bw_use in json.loads(bw_uses):
    if name == bw_use.get(key_json_name):

      try:
          current_use[key_json_aat] = str(int(bw_use.get(key_json_aat)))
      except AttributeError:
        pass
      except TypeError:
        pass
      
      try:
        current_use[key_json_ita] = bw_use.get(key_json_ita)
      except AttributeError:
        pass

  return current_use

def get_bw_typology(current_typology):

  if current_typology.get(key_typology) is not None:

    name = current_typology.get(key_typology)

    for bw_typology in json.loads(bw_typologies):
      if name == bw_typology.get(key_json_name):

        try:
          current_typology[key_json_aat] = str(int(bw_typology.get(key_json_aat)))
        except AttributeError:
          pass
        except TypeError:
          pass
        
        try:
          current_typology[key_json_ita] = bw_typology.get(key_json_ita)
        except AttributeError:
          pass

  return current_typology

def get_bw_material(current_material):

  name =  current_material
  current_material = {key_material: current_material}

  for bw_material in json.loads(bw_materials):

    if name.lower() == bw_material.get(key_json_name).lower():
      
      try:
        current_material[key_json_aat] = str(int(bw_material.get(key_json_aat)))
      except AttributeError:
        pass
      except TypeError:
        pass
      
      try:
        current_material[key_json_ita] = bw_material.get(key_json_ita)
      except AttributeError:
        pass 

  return current_material

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
  # Clear nan words
  if (type(val) is np.int64 or type(val) is np.float64) and np.isnan(val): 
    return ''
    
  return val

def add_to_set(key, bw_dict, id, val):
  if bw_dict[id].get(key) is None:
    bw_dict[id][key] = set()
    
  bw_dict[id][key].add(val)

def insert_in_list(l, to_insert):

  if len(l) == 0:
    return l.append(to_insert)

  for row in l:
    if to_insert == row:
      return

  return  l.append(to_insert)

# Create a dict with an array containing every bw as json object
for i in range(len(df)) :
  row_id = df.loc[i, key_bw_id]

  # Instantiate dictionaries
  typology_dict = {}
  use_dict = {}
  function_dict = {}

  set_material = set()

  # create the current bw if not already in the main dict
  if row_id not in builtworks:
    builtworks[row_id] = {}

  # iterate all columns
  for y in range(1, len(df.columns)):

    # save value and the column name
    val = clear(df.iloc[i, y])
    col = df.columns[y]

    if val is not None and type(val) is str:

      # Material
      if col == key_material:

        if builtworks[row_id].get(key_material) is None:
          builtworks[row_id][key_material] = set()

        for material in val.split(';'):
          set_material.add(material.strip())

      # Function
      elif col == key_function:

        if builtworks[row_id].get(key_function) is None:
          builtworks[row_id][key_function] = []
        
        function_dict[key_function] = val

      elif col == key_function_start:
        function_dict[key_function_start] = val

      elif col == key_function_end:
        function_dict[key_function_end] = val

      # Typology
      elif col == key_typology:

        if builtworks[row_id].get(key_typology) is None:
          builtworks[row_id][key_typology] = []

        typology_dict[key_typology] = val

      elif col == key_typology_start:
        typology_dict[key_typology_start] = val

      elif col == key_typology_end:
        typology_dict[key_typology_end] = val
      
      # Use
      elif col == key_use:

        # Create the list if doesn't exist
        if builtworks[row_id].get(key_use) is None:
          builtworks[row_id][key_use] = []

        use_dict[key_use] = val
      
      elif col == key_use_start:
        use_dict[key_use_start] = val
      
      elif col == key_use_end:
        use_dict[key_use_end] = val

      # Residual columns
      else:
        builtworks[row_id][col] = val

  # Append dictionaries only if not equal
  insert_in_list(builtworks[row_id][key_typology], typology_dict)
  insert_in_list(builtworks[row_id][key_use], use_dict)
  insert_in_list(builtworks[row_id][key_function], function_dict)

  builtworks[row_id][key_material] = set_material 


for bw_id, bw in builtworks.items():

  # Create the current row
  xml_row = et.Element(key_row)

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

  # SHP_Lenght
  # base_tag(xml_row, key_shape_lenght,  bw[key_shape_lenght])

  # SHP_Area
  # base_tag(xml_row, key_shape_area,  bw[key_shape_area])

  # Materials
  if bw.get(key_material) is not None and len(bw.get(key_material)) > 0:

    # Get the set of materials
    text_materials = bw.get(key_material)

    # Create the tag Materials
    materials = et.SubElement(xml_row, key_materials)

    for current_material in text_materials:

      # Create the tag Material
      material = et.SubElement(materials, key_material)

      current_material = get_bw_material(current_material)

      # Set eng name
      base_tag(material, key_eng, current_material.get(key_material))   

      if current_material.get(key_json_ita) is not None:
        base_tag(material, key_ita, current_material.get(key_json_ita))

      if current_material.get(key_json_aat) is not None:
        base_tag(material, key_aat, current_material.get(key_json_aat))

  # Functions
  if bw.get(key_function) is not None and len(bw.get(key_function)) > 0:

    functions = et.SubElement(xml_row, key_functions)
    for current_function in bw.get(key_function):

      function_tag = et.SubElement(functions, key_function)

      base_tag(function_tag, key_function, current_function.get(key_function))
      base_tag(function_tag, key_function_start, current_function.get(key_function_start))
      base_tag(function_tag, key_function_end, current_function.get(key_function_end))

  # Uses
  if bw.get(key_use) is not None and len(bw.get(key_use)) > 0:

    uses = et.SubElement(xml_row, key_uses)
    for current_use in bw.get(key_use):

      # create xml tag
      use_tag = et.SubElement(uses, key_use)

      # update current_use with data from uses list
      current_use = get_bw_use(current_use)

      # Set eng name
      base_tag(use_tag, key_eng, current_use.get(key_use))

      if current_use.get(key_json_ita) is not None:
        base_tag(use_tag, key_ita, current_use.get(key_json_ita))

      if current_use.get(key_json_aat) is not None:
        base_tag(use_tag, key_aat, current_use.get(key_json_aat))

      if current_use.get(key_use_start) is not None:
        base_tag(use_tag, key_use_start, current_use.get(key_use_start))

      if current_use.get(key_use_end) is not None:
        base_tag(use_tag, key_use_end, current_use.get(key_use_end))

  # Typologies
  if bw.get(key_typology) is not None and len(bw.get(key_typology)) > 0:

    typologies = et.SubElement(xml_row, key_typologies)
    for current_typology in bw.get(key_typology):

      # create xml tag
      typology_tag = et.SubElement(typologies, key_typology)

      # update current_typology with data from typology list
      current_typology = get_bw_typology(current_typology)

      # Set eng name
      base_tag(typology_tag, key_eng, current_typology.get(key_typology))

      if current_typology.get(key_json_ita) is not None:
        base_tag(typology_tag, key_ita, current_typology.get(key_json_ita))

      if current_typology.get(key_json_aat) is not None:
        base_tag(typology_tag, key_aat, current_typology.get(key_json_aat))

      if current_typology.get(key_typology_start) is not None:
        base_tag(typology_tag, key_typology_start, current_typology.get(key_typology_start))

      if current_typology.get(key_typology_end) is not None:
        base_tag(typology_tag, key_typology_end, current_typology.get(key_typology_end))

  """
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
  """

  final = md.parseString(et.tostring(xml_row, method='xml')).toprettyxml()

  write_file(bw_id, final)