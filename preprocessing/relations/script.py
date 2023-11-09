from xml.dom import minidom as md, getDOMImplementation
import xml.etree.ElementTree as et
from datetime import datetime, timezone
import os
import json
import uuid

def _write_file(row_id, text):
  output_directory = os.path.join(root_path, 'transformation', t, 'data')
  if not os.path.isdir(output_directory):
    os.mkdir(output_directory)
  output_filename = os.path.join(output_directory, f'{row_id}.xml')
  with open(output_filename, 'w') as f:
    f.write(text)



t = 'relations'

dir_path = os.path.dirname(os.path.realpath(__file__))
root_path = os.path.join(dir_path, os.path.pardir, os.path.pardir)
dir_extraction = os.path.join(root_path, 'extraction', 'transformed')

uuid_filename = os.path.join(dir_path, os.pardir, 'relations.json')


####### KEYS ###########
KEY_ROW = 'ROW'
KEY_UUID = "UUID"

KEY_ID_BIBLIOGRAPHY = 'ID_BIBLIOGRAPHY'
KEY_ID_PERSON = 'ID_PERSON'
KEY_ID_ACTOR = 'ID_ACTOR'
KEY_ID_PLACE = 'ID_PLACE'
KEY_ID_SOURCE = 'ID_SOURCE'

KEY_UUID_LEFT = 'UUID_LEFT'
KEY_UUID_RIGHT = 'UUID_RIGHT'

KEY_TYPE_LEFT = 'TYPE_LEFT'
KEY_TYPE_RIGHT = 'TYPE_RIGHT'

# INPUT
IN_KEY_EVENT_ID = 'ID_EVENT'
IN_KEY_EVENT_NAME = 'Name_Event'
IN_KEY_EVENT_TYPOLOGY = 'Subtypology'
IN_KEY_EVENT_SYNOPSIS = 'Synopsis'


# OUTPUT
OUT_KEY_EVENT_ID = IN_KEY_EVENT_ID.lower()
OUT_KEY_EVENT_NAME = IN_KEY_EVENT_NAME.lower()
OUT_KEY_EVENT_TYPOLOGY = IN_KEY_EVENT_TYPOLOGY.lower()
OUT_KEY_EVENT_SYNOPSIS = IN_KEY_EVENT_SYNOPSIS.lower()

OUT_KEY_EVENT_BIBLIOGRAPHIC_ITEMS = 'related_bibitems'
OUT_KEY_EVENT_BIBLIOGRAPHIC_ITEM = 'related_bibitem'

OUT_KEY_EVENT_SOURCES = 'related_sources'
OUT_KEY_EVENT_ACTORS = 'related_actors'
OUT_KEY_EVENT_SOURCE = 'related_source'
OUT_KEY_EVENT_ACTOR = 'related_actor'

# dicts of relational data
dict_event_x_people = json.load(open(os.path.join(dir_path, 'event_x_people.json')))
dict_event_x_sources = json.load(open(os.path.join(dir_path, 'event_x_sources.json')))
dict_event_x_places = json.load(open(os.path.join(dir_path, 'event_x_places.json')))

# dicts of uuids
dict_events = json.load(open(os.path.join(dir_path, os.pardir, 'events.json')))

def _create_row(uuid, left_uuid, left_type, right_uuid, right_type):
  new_row = et.Element(KEY_ROW)

  node_uuid_relation = et.SubElement(new_row, KEY_UUID)
  node_uuid_relation.text = uuid
  
  node_uuid_left = et.SubElement(new_row, KEY_UUID_LEFT)
  node_type_left = et.SubElement(new_row, KEY_TYPE_LEFT)
  
  node_uuid_left.text = left_uuid
  node_type_left.text = left_type
  
  node_uuid_right = et.SubElement(new_row, KEY_UUID_RIGHT)
  node_type_right = et.SubElement(new_row, KEY_TYPE_RIGHT)
  
  node_uuid_right.text = right_uuid
  node_type_right.text = right_type

  return new_row

def process_left_x_right(dict_relation, dict_left, left_type, right_type, uuid_dict, limit, is_bw=False):
  
  cnt = 0
  
  for key, value in dict_relation.items():
    for relation in value:

      if cnt == int(limit):
        return

      if is_bw:
        for k, v in dict_event_x_places.items():
          if relation in v:
            right_uuid = int(relation)
      else:
        right_uuid = relation[KEY_UUID]
      
      try:
        if key not in uuid_dict:
          uuid_dict[key] = {
            KEY_UUID: str(uuid.uuid1()),
            KEY_UUID_LEFT: dict_left[key][KEY_UUID],
            KEY_TYPE_LEFT: left_type,
            KEY_UUID_RIGHT: right_uuid,
            KEY_TYPE_RIGHT: right_type
          }
          
        relation = uuid_dict[key]

        new_row = _create_row(relation[KEY_UUID], relation[KEY_UUID_LEFT], relation[KEY_TYPE_LEFT], relation[KEY_UUID_RIGHT], relation[KEY_TYPE_RIGHT])

        final = md.parseString(et.tostring(new_row, method='xml')).toprettyxml()
        _write_file(relation[KEY_UUID], final)
        
      except Exception as e:
        print(e)
        print(relation)
        continue
      
      finally:
        cnt += 1
        
  return uuid_dict

def execute(limit, sa=None):

  uuid_dict = {}

  if os.path.exists(uuid_filename):
    uuid_dict = json.load(open(uuid_filename))
  
  # Process events x people
  #uuid_dict = process_left_x_right(dict_event_x_people, dict_events, 'event', 'actor', uuid_dict, limit)
  

  uuid_dict = process_left_x_right(dict_event_x_places, dict_events, 'event', 'builtwork', uuid_dict, limit, is_bw=True)

  # Process events x sources
  #process_event_x_sources(limit)  
    
  with open(uuid_filename, 'w') as f:
    f.write(json.dumps(uuid_dict, indent=2, sort_keys=True))