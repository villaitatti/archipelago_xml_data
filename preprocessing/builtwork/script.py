import pandas as pd
import numpy as np
from datetime import datetime, timezone
import xml.dom.minidom as md
import xml.etree.ElementTree as et
import os
import re
import json
import uuid

def execute(limit):
  
  def get_type(filename):
    if "BLDG" in filename:
      return "building"

    if "IS" in filename:
      return "island"

    if "OS" in filename:
      return "open_space"

  def order_df(df):
    df = df.set_index(key_bw_id)
    df = df.sort_index()
    df.to_csv(os.path.join(
        dir_path, f'{buildings}_ordered{buildings_ext}'), sep='\t')

  def write_file(name, text, ext='xml'):

    output_directory = os.path.join(
        dir_path, os.path.pardir, os.path.pardir, 'transformation', 'builtwork', data_dir)

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
            current_typology[key_json_aat] = str(
                int(bw_typology.get(key_json_aat)))
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

    name = current_material
    current_material = {key_material: current_material}

    for bw_material in json.loads(bw_materials):

      if name.lower() == bw_material.get(key_json_name).lower():

        try:
          current_material[key_json_aat] = str(
              int(bw_material.get(key_json_aat)))
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
        current_name = re.sub(r'[\[{].*}', '', person.get(key_surname)).strip()
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

  dir_path = os.path.dirname(os.path.realpath(__file__))
  filename = os.path.join(dir_path, data_dir, buildings + buildings_ext)

  bw_typologies_filename = os.path.join(
      dir_path, data_dir, 'bw_typologies.tsv')
  bw_uses_filename = os.path.join(dir_path, data_dir, 'bw_uses.tsv')
  bw_materials_filename = os.path.join(dir_path, data_dir, 'bw_materials.tsv')
  bw_islands_filename = os.path.join(dir_path, data_dir, 'bw_islands.tsv')

  # Geonames dictionary
  geonames_dict = json.load(open(os.path.join(
      dir_path, os.path.pardir, os.path.pardir, 'utils', 'geonames', 'geonames.json'), 'r'))
  people_dict = json.load(
      open(os.path.join(dir_path, os.path.pardir, 'actor', 'people.json'), 'r'))

  bw_typologies = pd.read_csv(
      bw_typologies_filename, sep='\t').reset_index().to_json(orient='records')
  bw_uses = pd.read_csv(
      bw_uses_filename, sep='\t').reset_index().to_json(orient='records')
  bw_materials = pd.read_csv(
      bw_materials_filename, sep='\t').reset_index().to_json(orient='records')
  bw_islands = pd.read_csv(
      bw_islands_filename, sep='\t').reset_index().to_json(orient='records')

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
  key_label = 'label'

  key_production = 'production'
  key_destruction = 'destruction'
  key_role_patrons = 'role_patrons'
  key_role_patron = 'role_patron'
  key_role_architects = 'role_architects'
  key_role_architect = 'role_architect'

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
  key_transformation_use = 'transformation_use'
  key_transformation_uses = 'transformation_uses'

  key_transformation_typology = 'transformation_typology'
  key_transformation_typologies = 'transformation_typologies'

  key_transformation_function = 'transformation_function'
  key_transformation_functions = 'transformation_functions'

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
  key_uuid = 'UUID'

  key_from = 'from'
  key_to = 'to'

  key_identifier = 'id'

  # JSON keys
  key_json_aat = 'AAT ID'
  key_json_name = 'NAME'
  key_json_url = 'URL'
  key_json_ita = 'ITA'
  key_json_geonames = 'Geonames ID'
  key_surname = 'Surname'

  key_st_volume = 'st_volume'

  uuid_filename = os.path.join(dir_path, 'uuid.json')
  uuid_bw = 'bw_uuid'
  uuid_st = 'st_uuid'

  def escape_uri(text):
    return str(text).lower().replace(" ", "_")

  dtypes = {key_start: str, key_end: str, key_height: str, key_architect: str, key_patron: str,
            key_owner: str, key_tenant: str, key_shape_lenght: str, key_architects: str}
  df = pd.read_csv(filename, sep='\t', dtype=dtypes, keep_default_na=False)

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

    return l.append(to_insert)

  # COLLAPSING ROWS

  def parse_entity_date(entity):

    if col not in builtworks[bw_name]:
      builtworks[bw_name][col] = [entity]

    if entity not in builtworks[bw_name][col]:
      builtworks[bw_name][col].append(entity)
      


  for i, row in df.iterrows():

    bw_name = row[key_name]

    if bw_name not in builtworks:
      builtworks[bw_name] = {}

    for y in range(1, len(df.columns)):

      # save value and the column name
      val = clear(df.iloc[i, y])
      col = df.columns[y]

      # Island Name is a single string
      if col == key_islandname:
        builtworks[bw_name][col] = val

      # Name is a single string
      if col == key_name:
        builtworks[bw_name][col] = val

      # Save earliest start
      if col == key_start:
        if col not in builtworks[bw_name] or val < builtworks[bw_name][col]:
          builtworks[bw_name][col] = val

      # Save latest end 
      if col == key_end:
        if col not in builtworks[bw_name] or val > builtworks[bw_name][col]:
          builtworks[bw_name][col] = val
      
      # Function
      if col == key_function and val:
        parse_entity_date({
          key_function: val,
          key_function_start: row[key_function_start],
          key_function_end: row[key_function_end]
        })

      # Use
      if col == key_use and val:
        parse_entity_date({
          key_use: val,
          key_use_start: row[key_use_start],
          key_use_end: row[key_use_end]
        })

      # Typology
      if col == key_typology and val:
        parse_entity_date({
          key_typology: val,
          key_typology_start: row[key_typology_start],
          key_typology_end: row[key_typology_end]
        })

      # Owner
      if col == key_owner and val:
        parse_entity_date({
          key_owner: val,
          key_owner_start: row[key_owner_start],
          key_owner_end: row[key_owner_end]
        })

      # Owner
      if col == key_tenant and val:
        parse_entity_date({
          key_tenant: val,
          key_tenant_start: row[key_tenant_start],
          key_tenant_end: row[key_tenant_end]
        })

      if val and (col == key_material or col == key_patron):
        if col not in builtworks[bw_name] or val not in builtworks[bw_name][col]:
          builtworks[bw_name][col] = val

      # add ST Volume

      st_volume = {
        key_bw_id: row[key_bw_id],
        key_start: row[key_start],
        key_end: row[key_end]
      }

    if key_st_volume not in builtworks[bw_name]:
      builtworks[bw_name][key_st_volume] = []

    if st_volume not in builtworks[bw_name][key_st_volume]:
      builtworks[bw_name][key_st_volume].append(st_volume)

  cnt = 0
  uuid_dict = {}
  
  if os.path.isfile(uuid_filename):
    uuid_dict = json.load(open(uuid_filename))

  ##############################################################################################################
  ####################################### PRE-PROCESSING #######################################################
  ##############################################################################################################

  for bw_id, bw in builtworks.items():

    name = f'{bw.get(key_name)} ({bw.get(key_islandname)})'

    if name not in uuid_dict:
      uuid_dict[name] = {
        uuid_bw: str(uuid.uuid1())
      }
    
    if limit and cnt == int(limit):
      break

    # Create the current row
    xml_row = et.Element(key_row)

    #######################
    # Processing Building #
    #######################

    builtwork = et.SubElement(xml_row, 'builtwork')

    # Type
    builtwork_type = et.SubElement(builtwork, 'type')
    builtwork_type.text = get_type(bw_id)

    tag_container = et.SubElement(builtwork, 'container')

    parent_container = et.SubElement(tag_container, 'parent')
    parent_container.text = 'formContainer'

    label_container = et.SubElement(tag_container, 'label')
    label_container.text = f'LDP container of {name}'

    creator_container = et.SubElement(tag_container, 'creator')
    creator_container.text = 'admin'

    time_container = et.SubElement(tag_container, 'time')
    time_container.text = datetime.now(tz=timezone.utc).strftime("%Y-%m-%d %H:%M:%S")

    # UUID
    builtwork_uuid = uuid_dict[name][uuid_bw]
    base_tag(builtwork, key_uuid, builtwork_uuid)

    # IslandName
    island = et.SubElement(builtwork, key_islandname)

    current_island = get_bw_island(bw.get(key_islandname))

    base_tag(island, key_ita,  current_island.get(key_json_name))
    base_tag(island, key_geo,  current_island.get(key_json_geonames))

    # Production
    production_tag = et.SubElement(builtwork, key_production)
    base_tag(production_tag, key_date, bw.get(key_start))

    # Destruction
    if bw.get(key_end) is not None:
      destruction_tag = et.SubElement(builtwork, key_destruction)
      base_tag(destruction_tag, key_date,  bw.get(key_end))

    # Name
    base_tag(builtwork, key_name, name)

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

        # Set identifier
        base_tag(material, key_identifier, escape_uri(current_material.get(key_material)))

    # Functions
    list_functions = []
    if bw.get(key_function) is not None and len(bw.get(key_function)) > 0:

      functions = et.SubElement(builtwork, key_functions)
      for i, current_function in enumerate(bw.get(key_function)):

        function_tag = et.SubElement(functions, key_function)
        function_tag.attrib[key_position] = str(
            bw.get(key_function).index(current_function) + 1)

        identifier = escape_uri(current_function.get(key_function))

        base_tag(function_tag, key_eng, current_function.get(key_function))
        base_tag(function_tag, key_function_start,
                 current_function.get(key_function_start))
        base_tag(function_tag, key_function_end,
                 current_function.get(key_function_end))
        base_tag(function_tag, key_identifier, identifier)

        # Extract transformation
        list_functions.append({
          key_date: current_function.get(key_function_start),
          key_name: current_function.get(key_function)
        })

    # Uses
    list_uses = []
    if bw.get(key_use) is not None and len(bw.get(key_use)) > 0:

      uses = et.SubElement(builtwork, key_uses)
      for i, current_use in enumerate(bw.get(key_use)):

        # create xml tag
        use_tag = et.SubElement(uses, key_use)
        use_tag.attrib[key_position] = str(
            bw.get(key_use).index(current_use) + 1)

        # update current_use with data from uses list
        current_use = get_bw_use(current_use)

        identifier = escape_uri(current_use.get(key_use))

        # Set eng name
        base_tag(use_tag, key_eng, current_use.get(key_use))
        base_tag(use_tag, key_ita, current_use.get(key_json_ita))
        base_tag(use_tag, key_aat, current_use.get(key_json_aat))
        base_tag(use_tag, key_use_start, current_use.get(key_use_start))
        base_tag(use_tag, key_use_end, current_use.get(key_use_end))
        base_tag(use_tag, key_identifier, identifier)

        # Extract transformation
        list_uses.append({
          key_date: current_use.get(key_use_start),
          key_name: current_use.get(key_use)
        })

    # Typologies
    list_typologies = []
    if bw.get(key_typology) is not None and len(bw.get(key_typology)) > 0:

      typologies = et.SubElement(builtwork, key_typologies)
      for i, current_typology in enumerate(bw.get(key_typology)):

        # create xml tag
        typology_tag = et.SubElement(typologies, key_typology)
        typology_tag.attrib[key_position] = str(
            bw.get(key_typology).index(current_typology) + 1)

        # update current_typology with data from typology list
        current_typology = get_bw_typology(current_typology)

        identifier = escape_uri(current_typology.get(key_typology))

        # Set resulting elements
        base_tag(typology_tag, key_eng, current_typology.get(key_typology))
        base_tag(typology_tag, key_ita, current_typology.get(key_json_ita))
        base_tag(typology_tag, key_aat, current_typology.get(key_json_aat))
        base_tag(typology_tag, key_typology_start,
                 current_typology.get(key_typology_start))
        base_tag(typology_tag, key_typology_end,
                 current_typology.get(key_typology_end))
        base_tag(typology_tag, key_identifier, identifier)

        list_typologies.append({
          key_date: current_typology.get(key_typology_start),
          key_name: current_typology.get(key_typology)
        })

    # Owners
    if bw.get(key_owner) is not None and len(bw.get(key_owner)) > 0:

      owners = et.SubElement(builtwork, 'acquisitions')
      sorted_owners = sorted(bw.get(key_owner), key=lambda d: d[key_owner_start])

      prev_owner = None
      for current_owner in sorted_owners:

        # Create xml tag
        owner_tag = et.SubElement(owners, 'acquisition')
        
        base_tag(owner_tag, key_uuid, str(uuid.uuid1()))
        base_tag(owner_tag, key_to, current_owner.get(key_owner))

        if prev_owner is not None:
          base_tag(owner_tag, key_from, prev_owner.get(key_owner))

        base_tag(owner_tag, key_date, current_owner.get(key_owner_start))
        prev_owner = current_owner

    # Tenants
    if bw.get(key_tenant) is not None and len(bw.get(key_tenant)) > 0:

      tenants = et.SubElement(builtwork, 'custodies')
      sorted_tenants = sorted(bw.get(key_tenant), key=lambda d: d[key_tenant_start])

      prev_tenant = None
      for current_tenant in sorted_tenants:

        # Create xml tag
        tenant_tag = et.SubElement(tenants, 'custody')

        base_tag(tenant_tag, key_uuid, str(uuid.uuid1()))
        base_tag(tenant_tag, key_to, current_tenant.get(key_tenant))

        if prev_tenant is not None:
          base_tag(tenant_tag, key_from, prev_tenant.get(key_tenant))

        base_tag(tenant_tag, key_date, current_tenant.get(key_tenant_start))

      prev_tenant = current_tenant

    # Architects
    if bw.get(key_architect) is not None and len(bw.get(key_architect)) > 0:
      
      role_architects_tag = et.SubElement(production_tag, key_role_architects)

      for current_architect in bw.get(key_architect):
        
        role_architect_tag = et.SubElement(role_architects_tag, key_role_architect)

        base_tag(role_architect_tag, key_uuid, str(uuid.uuid1()))
        base_tag(role_architect_tag, key_person_id, current_architect)

    # Patrons
    if bw.get(key_patron) is not None and len(bw.get(key_patron)) > 0:

      role_patrons_tag = et.SubElement(production_tag, key_role_patrons)

      for current_patron in bw.get(key_patron):

        role_patron_tag = et.SubElement(role_patrons_tag, key_role_patron)

        base_tag(role_patron_tag, key_uuid, str(uuid.uuid1()))
        base_tag(role_patron_tag, key_person_id, current_patron)
    
    # Transformation functions
    if len(list_functions) > 1:
      list_functions_sorted = sorted(list_functions, key=lambda d: d[key_date])
      transformation_functions = et.SubElement(builtwork, key_transformation_functions)

      for i, function in enumerate(list_functions_sorted):

        label = 'Transformation of function '
        transformation_function = et.SubElement(transformation_functions, key_transformation_function)

        base_tag(transformation_function, 'transformation_function_uuid', str(uuid.uuid1()))
        base_tag(transformation_function, 'pos', str(i))
        base_tag(transformation_function, 'to', escape_uri(function[key_name]))
        base_tag(transformation_function, key_function_start, function[key_date])

        if i>0:
          prev = list_functions_sorted[i-1][key_name]
          base_tag(transformation_function, 'from', escape_uri(prev))
          label += f'from {prev} '

        base_tag(transformation_function, key_label, f'{label}to {function[key_name]} ({function[key_date]})')

    # Transformation uses
    if len(list_uses) > 1:
      list_uses_sorted = sorted(list_uses, key=lambda d: d[key_date]) 
      transformation_uses = et.SubElement(builtwork, key_transformation_uses)

      for i, use in enumerate(list_uses_sorted):
        
        label = 'Transformation of use '
        transformation_use = et.SubElement(transformation_uses, key_transformation_use)

        base_tag(transformation_use, 'transformation_use_uuid', str(uuid.uuid1()))
        base_tag(transformation_use, 'pos', str(i))
        base_tag(transformation_use, 'to', escape_uri(use[key_name]))
        base_tag(transformation_use, key_use_start, use[key_date])

        if i>0:
          prev = list_uses_sorted[i-1][key_name]
          base_tag(transformation_use, 'from', escape_uri(prev))
          label += f'from {prev} '

        base_tag(transformation_use, key_label, f'{label}to {use[key_name]} ({use[key_date]})')

    # Transformation typologies
    if len(list_typologies) > 1:
      list_typologies_sorted = sorted(list_typologies, key=lambda d: d[key_date])
      transformation_typologies = et.SubElement(builtwork, key_transformation_typologies)

      for i, typology in enumerate(list_typologies_sorted):

        label = 'Transformation of typology '
        transformation_typology = et.SubElement(transformation_typologies, key_transformation_typology)

        base_tag(transformation_typology, 'transformation_typology_uuid', str(uuid.uuid1()))
        base_tag(transformation_typology, 'pos', str(i))
        base_tag(transformation_typology, 'to', escape_uri(typology[key_name]))
        base_tag(transformation_typology, key_typology_start, typology[key_date])
      
        if i>0:
          prev = list_typologies_sorted[i-1][key_name]
          base_tag(transformation_typology, 'from', escape_uri(prev))
          label += f'from {prev} '
        
        base_tag(transformation_typology, key_label, f'{label}to {typology[key_name]} ({typology[key_date]})')


    ########################
    # Processing ST Volume #
    ########################
    st_volumes = et.SubElement(xml_row, 'st_volumes')


    # UUID

    for st_volume_curr in bw.get(key_st_volume):

      st_volume = et.SubElement(st_volumes, 'st_volume')

      st_volume_id = st_volume_curr[key_bw_id]

      if st_volume_id not in uuid_dict[name]:
        uuid_dict[name][st_volume_id] = str(uuid.uuid1())

      st_volume_uuid = uuid_dict[name][st_volume_id]
      base_tag(st_volume, key_uuid, st_volume_uuid)

      # bw id
      base_tag(st_volume, key_bw_id, st_volume_id)

      # Start_Earliest
      base_tag(st_volume, key_start,  st_volume_curr.get(key_start))

      # End_Latest
      base_tag(st_volume, key_end,  st_volume_curr.get(key_end))

      if bw.get(key_end) is not None:
        year_end = datetime.strptime(st_volume_curr.get(key_end), '%Y-%m-%d').year
      else:
        year_end = 'today'

      year_start = datetime.strptime(st_volume_curr.get(key_start), '%Y-%m-%d').year
      st_volume_name = f'{name} from {year_start} to {year_end}'

      base_tag(st_volume, 'label', st_volume_name)
      base_tag(st_volume, 'dig_label', f'Digital Object (2D representation) associated with {st_volume_name}') 

    final = md.parseString(et.tostring(xml_row, method='xml')).toprettyxml()

    write_file(builtwork_uuid, final)

    cnt += 1

  with open(uuid_filename, 'w') as f:
    f.write(json.dumps(uuid_dict, indent=4, sort_keys=True))