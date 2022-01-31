import pandas as pd
import numpy as np
from datetime import datetime
import xml.dom.minidom as md
import xml.etree.ElementTree as et
import os
import re
import json

def execute(limit):

  def order_df(df):
    df = df.set_index(key_bw_id)
    df = df.sort_index()
    df.to_csv(os.path.join(dir_path, f'{buildings}_ordered{buildings_ext}'), sep='\t')

  def write_file(name, text, ext='xml'):

    output_directory = os.path.join(dir_path, os.path.pardir, os.path.pardir, 'transformation', 'builtwork', data_dir)

    if not os.path.isdir(output_directory):
      os.mkdir(output_directory)

    output_filename = os.path.join(output_directory, f'{name}.{ext}')

    with open(output_filename, 'w') as f:
      f.write(text)

  def base_tag(parent, key, text):
    # Block None text
    if text is None:
      return

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
    if name is not None:
      for person in people_dict:
        current_name = re.sub(r'[\[{].*}','',person.get(key_surname)).strip()
        if name.lower() == current_name.lower():
          return person

    return None

  def add_person(parent, key):
    current_person = get_person(key)
    if current_person is not None:
      base_tag(parent, key_person_id, current_person.get(key_person_id))

  buildings = 'SS_BLDGS'
  buildings_ext = '.tsv'
  data_dir = 'data'

  # TODO pass the file as arg
  dir_path = os.path.dirname(os.path.realpath(__file__))
  filename = os.path.join(dir_path,data_dir, buildings + buildings_ext)

  bw_typologies_filename = os.path.join(dir_path, data_dir, 'bw_typologies.tsv')
  bw_uses_filename = os.path.join(dir_path, data_dir, 'bw_uses.tsv')
  bw_materials_filename = os.path.join(dir_path, data_dir, 'bw_materials.tsv')
  bw_islands_filename = os.path.join(dir_path, data_dir, 'bw_islands.tsv')

  # Geonames dictionary
  geonames_dict = json.load(open(os.path.join(dir_path, os.path.pardir, os.path.pardir, 'utils', 'geonames', 'geonames.json'), 'r'))
  people_dict = json.load(open(os.path.join(dir_path, os.path.pardir, 'actor', 'people.json'), 'r'))

  bw_typologies = pd.read_csv(bw_typologies_filename, sep='\t').reset_index().to_json(orient='records')
  bw_uses = pd.read_csv(bw_uses_filename, sep='\t').reset_index().to_json(orient='records')
  bw_materials = pd.read_csv(bw_materials_filename, sep='\t').reset_index().to_json(orient='records')
  bw_islands = pd.read_csv(bw_islands_filename, sep='\t').reset_index().to_json(orient='records')

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
  key_materials = 'materials'
  key_functions = 'functions'
  key_uses = 'uses'
  key_typologies = 'typologies'
  key_owners = 'owners'
  key_tenants = 'tenants'
  key_architects = 'architects'
  key_patrons = 'patrons'
  key_eng = 'eng'
  key_ita = 'ita'
  key_aat = 'aat'
  key_geo = 'geo'
  key_person_id = 'person_id'
  key_position = 'pos'

  # JSON keys
  key_json_aat = 'AAT ID'
  key_json_name = 'NAME'
  key_json_url = 'URL'
  key_json_ita = 'ITA'
  key_json_geonames = 'Geonames ID'
  key_surname = 'Surname'

  dtypes = {key_start:str, key_end:str, key_height:str, key_architect:str, key_patron: str, key_owner: str, key_tenant: str, key_shape_lenght:str, key_architects:str}
  df = pd.read_csv(filename, sep='\t', dtype=dtypes)

  builtworks = {}

  def clear(val):
    # Clear nan words
    if (type(val) is np.int64 or type(val) is np.float64 or type(val) is float) and np.isnan(val): 
      return ''
      
    return str(val)

  def add_to_set(key, bw_dict, id, val):
    if bw_dict[id].get(key) is None:
      bw_dict[id][key] = set()
      
    bw_dict[id][key].add(val)

  def insert_in_list(l, to_insert):

    # Block empty dict
    if not to_insert:
      return

    for row in l:
      if to_insert == row:
        return

    return  l.append(to_insert)

  # COLLAPSING ROWS 
  for i, row in df.iterrows():

    row_id = row[key_bw_id]
    
    # Instantiate dictionaries
    typology_dict = {}
    use_dict = {}
    function_dict = {}
    owner_dict = {}
    tenant_dict = {}

    material_set = set()
    architect_set = set()
    patron_set = set()

    # create the current bw if not already in the main dict
    if row_id not in builtworks:
      builtworks[row_id] = {}

    # iterate all columns
    for y in range(1, len(df.columns)):

      # save value and the column name
      val = clear(df.iloc[i, y])
      col = df.columns[y]

      if val is not None and type(val) and val:

        # Material
        if col == key_material:

          if builtworks[row_id].get(key_material) is None:
            builtworks[row_id][key_material] = set()

          for material in val.split(';'):
            material_set.add(material.strip())

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

        # Owner
        elif col == key_owner:

          if builtworks[row_id].get(key_owner) is None:
            builtworks[row_id][key_owner] = []

          owner_dict[key_owner] = val

        elif col == key_owner_start:
          owner_dict[key_owner_start] = val

        elif col == key_owner_end:
          owner_dict[key_owner_end] = val

        # Tenant
        elif col == key_tenant:

          if builtworks[row_id].get(key_tenant) is None:
            builtworks[row_id][key_tenant] = []

          tenant_dict[key_tenant] = val

        elif col == key_tenant_start:
          tenant_dict[key_tenant_start] = val

        elif col == key_tenant_end:
          tenant_dict[key_tenant_end] = val

        # Architect
        elif col == key_architect:
          if builtworks[row_id].get(key_architect) is None:
            builtworks[row_id][key_architect] = set()
          
          architect_set.add(val)

        # Patron
        elif col == key_patron:
          if builtworks[row_id].get(key_patron) is None:
            builtworks[row_id][key_patron] = set()
          
          patron_set.add(val)

        # Residual columns
        else:
          builtworks[row_id][col] = val

    # Append dictionaries only if not equal
    try:
      insert_in_list(builtworks[row_id][key_typology], typology_dict)
    except KeyError:
      pass
    try:
      insert_in_list(builtworks[row_id][key_use], use_dict)
    except KeyError:
      pass
    try:
      insert_in_list(builtworks[row_id][key_function], function_dict)
    except KeyError:
      pass
    try:
      insert_in_list(builtworks[row_id][key_owner], owner_dict)
    except KeyError:
      pass
    try:
      insert_in_list(builtworks[row_id][key_tenant], tenant_dict)
    except KeyError:
      pass

    builtworks[row_id][key_material] = material_set
    builtworks[row_id][key_architect] = architect_set
    builtworks[row_id][key_patron] = patron_set

  cnt = 0

  # PRE-PROCESSING
  for bw_id, bw in builtworks.items():

    if limit and cnt == int(limit):
      break

    # Create the current row
    xml_row = et.Element(key_row)

    st_volume = et.SubElement(xml_row, 'st_volume')

    # Processing ST Volume
    # bw id
    base_tag(st_volume, key_bw_id, bw_id)

    # Start_Earliest 
    base_tag(st_volume, key_start,  bw.get(key_start))

    # End_Latest 
    base_tag(st_volume, key_end,  bw.get(key_end))

    if bw.get(key_end) is not None:
      year_end = datetime.strptime(bw.get(key_end), '%Y-%m-%d').year
    else:
      year_end = 'today'

    year_start = datetime.strptime(bw.get(key_start), '%Y-%m-%d').year
    st_volume_name = f'{bw.get(key_name)} of {get_bw_island(bw.get(key_islandname)).get(key_json_name)} from {year_start} to {year_end}'

    base_tag(st_volume, 'label', st_volume_name)
      

    # Processing Building

    builtwork = et.SubElement(xml_row, 'builtwork')

    # IslandName
    island = et.SubElement(builtwork, key_islandname)

    current_island = get_bw_island(bw.get(key_islandname))

    base_tag(island, key_ita,  current_island.get(key_json_name))
    base_tag(island, key_geo,  current_island.get(key_json_geonames))

    # Start_Earliest 
    base_tag(builtwork, key_start,  bw.get(key_start))

    # End_Latest 
    base_tag(builtwork, key_end,  bw.get(key_end))

    # Name 
    base_tag(builtwork, key_name,  bw.get(key_name))

    # Height
    base_tag(builtwork, key_height,  bw.get(key_height))

    # SHP_Lenght
    # If is null
    try:
      base_tag(builtwork, key_shape_lenght,  bw[key_shape_lenght])
    except Exception:
      pass

    # SHP_Area
    try:
      base_tag(builtwork, key_shape_area,  bw[key_shape_area])
    except Exception:
      pass

    # Materials
    if bw.get(key_material) is not None and len(bw.get(key_material)) > 0:

      # Get the set of materials
      text_materials = bw.get(key_material)

      # Create the tag Materials
      materials = et.SubElement(builtwork, key_materials)

      for current_material in text_materials:

        # Create the tag Material
        material = et.SubElement(materials, key_material)

        current_material = get_bw_material(current_material)

        # Set eng name
        base_tag(material, key_eng, current_material.get(key_material))   
        base_tag(material, key_ita, current_material.get(key_json_ita))
        base_tag(material, key_aat, current_material.get(key_json_aat))

    # Functions
    if bw.get(key_function) is not None and len(bw.get(key_function)) > 0:

      functions = et.SubElement(builtwork, key_functions)
      for current_function in bw.get(key_function):

        function_tag = et.SubElement(functions, key_function)
        function_tag.attrib[key_position] = str(bw.get(key_function).index(current_function) + 1)

        base_tag(function_tag, key_function, current_function.get(key_function))
        base_tag(function_tag, key_function_start, current_function.get(key_function_start))
        base_tag(function_tag, key_function_end, current_function.get(key_function_end))

    # Uses
    if bw.get(key_use) is not None and len(bw.get(key_use)) > 0:

      uses = et.SubElement(builtwork, key_uses)
      for current_use in bw.get(key_use):

        # create xml tag
        use_tag = et.SubElement(uses, key_use)
        use_tag.attrib[key_position] = str(bw.get(key_use).index(current_use) + 1)

        # update current_use with data from uses list
        current_use = get_bw_use(current_use)

        # Set eng name
        base_tag(use_tag, key_eng, current_use.get(key_use))
        base_tag(use_tag, key_ita, current_use.get(key_json_ita))
        base_tag(use_tag, key_aat, current_use.get(key_json_aat))
        base_tag(use_tag, key_use_start, current_use.get(key_use_start))
        base_tag(use_tag, key_use_end, current_use.get(key_use_end))

    # Typologies
    if bw.get(key_typology) is not None and len(bw.get(key_typology)) > 0:

      typologies = et.SubElement(builtwork, key_typologies)
      for current_typology in bw.get(key_typology):

        # create xml tag
        typology_tag = et.SubElement(typologies, key_typology)
        typology_tag.attrib[key_position] = str(bw.get(key_typology).index(current_typology) + 1)

        # update current_typology with data from typology list
        current_typology = get_bw_typology(current_typology)

        # Set resulting elements
        base_tag(typology_tag, key_eng, current_typology.get(key_typology))
        base_tag(typology_tag, key_ita, current_typology.get(key_json_ita))
        base_tag(typology_tag, key_aat, current_typology.get(key_json_aat))
        base_tag(typology_tag, key_typology_start, current_typology.get(key_typology_start))
        base_tag(typology_tag, key_typology_end, current_typology.get(key_typology_end))

    # Owners
    if bw.get(key_owner) is not None and len(bw.get(key_owner)) > 0:

      owners = et.SubElement(builtwork, key_owners)
      for current_owner in bw.get(key_owner):

        # Create xml tag
        owner_tag = et.SubElement(owners, key_owner)
        # Save owner position in list
        owner_tag.attrib[key_position] = str(bw.get(key_owner).index(current_owner) + 1)

        base_tag(owner_tag, key_person_id, current_owner.get(key_owner))
        base_tag(owner_tag, key_owner_start, current_owner.get(key_owner_start))
        base_tag(owner_tag, key_owner_end, current_owner.get(key_owner_end))

    # Tenants
    if bw.get(key_tenant) is not None and len(bw.get(key_tenant)) > 0:

      tenants = et.SubElement(builtwork, key_tenants)
      for current_tenant in bw.get(key_tenant):

        # Create xml tag
        tenant_tag = et.SubElement(tenants, key_tenant)
        tenant_tag.attrib[key_position] = str(bw.get(key_tenant).index(current_tenant) + 1)

        base_tag(tenant_tag, key_person_id, current_tenant.get(key_tenant))
        base_tag(tenant_tag, key_tenant_start, current_tenant.get(key_tenant_start))
        base_tag(tenant_tag, key_tenant_end, current_tenant.get(key_tenant_end))

    # Architects
    if bw.get(key_architect) is not None and len(bw.get(key_architect)) > 0:  

      architects = et.SubElement(builtwork, key_architects)
      for current_architect in bw.get(key_architect):
        base_tag(et.SubElement(architects, key_architect), key_person_id, current_architect)

    # Patrons
    if bw.get(key_patron) is not None and len(bw.get(key_patron)) > 0:
      
      patrons = et.SubElement(builtwork, key_patrons)
      for current_patron in bw.get(key_patron):
        base_tag(et.SubElement(patrons, key_patron), key_person_id, current_patron)


    final = md.parseString(et.tostring(xml_row, method='xml')).toprettyxml()

    write_file(bw_id, final)
  
    cnt+=1