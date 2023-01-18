import uuid
from xml.dom import minidom as md, getDOMImplementation
import xml.etree.ElementTree as et
import os
import csv
import json
import dateutil.parser
import pandas as pd
from datetime import datetime


def execute(limit):

  # Store paths
  dir_path = os.path.dirname(os.path.realpath(__file__))
  filename = os.path.join(dir_path, os.pardir, os.pardir,
                          'extraction', 'transformed', 'Sources.xml')
  output_directory = os.path.join(
      dir_path, os.pardir, os.pardir, 'transformation', 'source', 'data')

  if not os.path.isdir(output_directory):
    os.mkdir(output_directory)

  # File with all UUIDs
  uuid_filename = os.path.join(dir_path, os.pardir, 'source.json')
  actors_filename = os.path.join(dir_path, os.pardir, 'actor.json')

  # Method called to write data file
  def write_file(text):
    output_filename = os.path.join(output_directory, f'{row_id}.xml')
    with open(output_filename, 'w') as f:
      f.write(text)

  # Method to create a base tag with only text
  def base_tag(parent, key, text):
    # Block None text
    if text is None:
      return

    # Block empty and wrong end
    text = str(text)
    if not text:
      return

    tag = et.SubElement(parent, key)
    tag.text = text

  # Method to retrieve value from a key file
  def get_value_from_key(key):
    return row.find(f'ns:{key}', ns).text

  # Method that transform typology into its ID
  # by lowering all letters and replacing whitespaces with _
  def get_id_from_typology(typology):
    typology = str(typology).replace(' ', '_')
    return typology.lower()
  
  # Method returning actor by name
  def get_actor_id_by_name(name):

    # Check actor name for each actor
    for actor_id in actors_dict:
      actor = actors_dict[actor_id]

      if actor[KEY_RELATION_NAME] and actor[KEY_RELATION_NAME] == name:
        return actor_id
    
    return None

  # List of KEYS

  KEY_UUID_SOURCE = 'uuid_source'
  KEY_RELATION_NAME = 'Name'

  KEY_IN_ROW = 'ROW'
  KEY_OUT_ROW = 'source'
  KEY_OUT_LABEL = 'label'

  KEY_IN_ID = 'ID_SOURCE'
  KEY_IN_TITLE = 'Title'
  KEY_IN_ORIGINALTITLE = 'Original_Title'
  KEY_IN_SYNOPSIS = 'Synopsis'
  KEY_IN_TRANSCRIPTION = 'Trascription'
  KEY_IN_LANGUAGE = 'Language'
  KEY_IN_TYPOLOGY = 'Typology'
  KEY_IN_MEDIUM = 'Medium'
  KEY_IN_DIMENSIONS = 'Dimensions'
  KEY_IN_AUTHOR = 'Author_Surname_Name'

  KEY_OUT_ID = KEY_IN_ID.lower()
  KEY_OUT_TITLE = KEY_IN_TITLE.lower()
  KEY_OUT_ORIGINALTITLE = KEY_IN_ORIGINALTITLE.lower()
  KEY_OUT_SYNOPSIS = KEY_IN_SYNOPSIS.lower()
  KEY_OUT_TRANSCRIPTION = KEY_IN_TRANSCRIPTION.lower()
  KEY_OUT_LANGUAGE = KEY_IN_LANGUAGE.lower()
  KEY_OUT_TYPOLOGY = KEY_IN_TYPOLOGY.lower()
  KEY_OUT_MEDIUM = KEY_IN_MEDIUM.lower()
  KEY_OUT_DIMENSIONS = KEY_IN_DIMENSIONS.lower()
  KEY_OUT_AUTHOR = KEY_IN_AUTHOR.lower()

  # Read file
  tree = et.parse(filename)
  root = tree.getroot()
  ns = {'ns': 'http://www.filemaker.com/fmpdsoresult'}

  # UUID dictionaries
  uuid_dict = {}
  if os.path.isfile(uuid_filename):
    uuid_dict = json.load(open(uuid_filename))
  
  actors_dict = {}
  if os.path.isfile(actors_filename):
    actors_dict = json.load(open(actors_filename))

  ##############################################################################################################
  ####################################### PRE-PROCESSING #######################################################
  ##############################################################################################################
  cnt = 0
  tags = root.findall(f'ns:{KEY_IN_ROW}', ns)

  for row in tags:

    # If the limit is reached.
    # Limit is passed as an arg when running the script
    if limit and cnt == int(limit):
      break

    # Save id_source, which is also the KEY to store the UUID
    id_source = get_value_from_key(KEY_IN_ID)

    # Add this source to the UUID dict if not already there
    if id_source not in uuid_dict:
      uuid_dict[id_source] = {
          KEY_UUID_SOURCE: str(uuid.uuid1())
      }

    # root tag
    new_row = et.Element(KEY_OUT_ROW)

    # Get and store UUID
    row_id = uuid_dict[id_source][KEY_UUID_SOURCE]
    base_tag(new_row, KEY_OUT_ID, row_id)

    # Attributed title
    attributed_title = get_value_from_key(KEY_IN_TITLE)
    base_tag(new_row, KEY_OUT_TITLE, attributed_title)

    # Original title
    original_title = get_value_from_key(KEY_IN_ORIGINALTITLE)
    base_tag(new_row, KEY_OUT_ORIGINALTITLE, original_title)

    # Synopsis
    synopsis = get_value_from_key(KEY_IN_SYNOPSIS)
    base_tag(new_row, KEY_OUT_SYNOPSIS, synopsis)

    # Transcription
    transcription = get_value_from_key(KEY_IN_TRANSCRIPTION)
    base_tag(new_row, KEY_OUT_TRANSCRIPTION, transcription)

    # Typology
    typology = get_id_from_typology(get_value_from_key(KEY_IN_TYPOLOGY))
    base_tag(new_row, KEY_OUT_TYPOLOGY, typology)
    
    # Medium
    medium = get_value_from_key(KEY_IN_MEDIUM)
    base_tag(new_row, KEY_OUT_MEDIUM, medium)
    
    # Dimension
    dimensions = get_value_from_key(KEY_IN_DIMENSIONS)
    base_tag(new_row, KEY_OUT_DIMENSIONS, dimensions)

    # TODO parse actor name to retrieve its UUID
    author_name = get_value_from_key(KEY_IN_AUTHOR)
    author_id = get_actor_id_by_name(author_name)

    if author_id:
      base_tag(new_row, KEY_OUT_AUTHOR, author_id)
    
    print(id_source)
    print(row_id)
    print(attributed_title)
    print()
    
    final = md.parseString(et.tostring(new_row, method='xml')).toprettyxml()
    write_file(final)

    cnt += 1

  # Save file with UUIDs
  with open(uuid_filename, 'w') as f:
    f.write(json.dumps(uuid_dict, indent=4, sort_keys=True))
