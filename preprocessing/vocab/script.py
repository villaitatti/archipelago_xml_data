from contextlib import nullcontext
from curses import keyname
import json
import os
import uuid
import pandas as pd
import numpy as np
import xml.etree.ElementTree as et
import xml.dom.minidom as md
import unidecode
import datetime

dir_path = os.path.dirname(os.path.realpath(__file__))
dir_data = os.path.join(dir_path, 'data')

KEY_UUID_VOCABULARY = 'uuid_vocab'

KEY_BASE = 'VOCAB_ENTRY'
KEY_AAT = 'AAT ID'
KEY_NAME = 'NAME'
KEY_URL = 'URL'
KEY_ITA = 'ITA'
KEY_PARENT = 'PARENT'
KEY_COLLECTION = 'COLLECTION'

def write_xml(dir_name, name, text):
  output_directory = os.path.join(
        dir_path, os.path.pardir, os.path.pardir, 'transformation', 'vocab', 'data', dir_name)

  if not os.path.isdir(output_directory):
    os.mkdir(output_directory)
    
  output_filename = os.path.join(output_directory, f'{name}.xml')

  with open(output_filename, 'w') as f:
    f.write(text)

def escape_uri(text):

  # Remove left and right whitespaces
  text = text.strip()

  # Replace accents 
  text = str(unidecode.unidecode(text))

  # To lowercase
  text = text.lower()

  # Replace whitespaces with _
  text = text.replace(" ", "_")
  
  text = text.replace("(", "")
  text = text.replace(")", "")

  return text

def execute(sa=None, limit = -1):

  for file in os.listdir(dir_data):

    # Check if file is CSV and selected for pipeline
    if file.endswith(".csv") and sa and os.path.splitext(file)[0] in sa:
      
      file_path = os.path.join(dir_data, file)
      dir_name = os.path.splitext(file)[0]
      
      uuid_vocab_filename = os.path.join(dir_path, os.pardir, f'vocab_{dir_name}.json')
      uuid_vocab_dict = {}
      
      if os.path.exists(uuid_vocab_filename):
        uuid_vocab_dict = json.load(open(uuid_vocab_filename))

      ##############################################################################################################
      ####################################### PRE-PROCESSING #######################################################
      ##############################################################################################################
      df_file = pd.read_csv(file_path, dtype = str).fillna(value = 'None')
      for num, row in df_file.iterrows():

        if limit and int(limit) == num:
          break

        # XML root
        root = et.Element(KEY_BASE)

        # identifier
        name = escape_uri(row[KEY_NAME])
        
        if name not in uuid_vocab_dict:
          uuid_vocab_dict[name] = {
            KEY_UUID_VOCABULARY: str(uuid.uuid1())
          }
        
        current_uuid = uuid_vocab_dict[name][KEY_UUID_VOCABULARY]
        
        # UUID
        tag_identifier = et.SubElement(root, 'identifier')
        tag_identifier.text = current_uuid

        # label eng
        eng = et.SubElement(root, 'eng')
        eng.text = row[KEY_NAME].strip()

        # Collection
        collection = et.SubElement(root, 'collection')
        collection.text = row[KEY_COLLECTION].strip()

        # label ita
        ita = et.SubElement(root, 'ita')
        ita.text = row[KEY_ITA].strip()

        # is root ?
        parent = row[KEY_PARENT]
        if parent != 'None':
          def execute_parent(parent):
            parent_uri = escape_uri(parent.strip())
            if parent_uri in uuid_vocab_dict:
              tag_parent = et.SubElement(root, 'broader')
              tag_parent.text = uuid_vocab_dict[parent_uri][KEY_UUID_VOCABULARY]
            
          if ',' in parent:
            for parent in parent.split(','):
              execute_parent(parent)
          else:
            execute_parent(parent)

        # URL optional
        try:
          url = row[KEY_AAT]
          if url != "None":
            tag_url = et.SubElement(root, 'related')
            tag_url.text = url

        except Exception as ex:
          print(ex)

        # LDP data for Researchspace
        tag_container = et.SubElement(root, 'container')

        parent_container = et.SubElement(tag_container, 'parent')
        parent_container.text = 'formContainer'

        label_container = et.SubElement(tag_container, 'label')
        label_container.text = f'LDP container of {name}'

        creator_container = et.SubElement(tag_container, 'creator')
        creator_container.text = 'admin'

        time_container = et.SubElement(tag_container, 'time')
        time_container.text = datetime.datetime.now(tz=datetime.timezone.utc).strftime("%Y-%m-%d %H:%M:%S")
      
        
        # write XML
        final = md.parseString(et.tostring(root, method='xml')).toprettyxml()
        write_xml(dir_name, current_uuid, final)
        print(name)

  # Write uuic dict file
  with open(uuid_vocab_filename, "w") as f:
    f.write(json.dumps(uuid_vocab_dict, indent=4, sort_keys=True))