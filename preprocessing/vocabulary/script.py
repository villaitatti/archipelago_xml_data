from contextlib import nullcontext
import os
import pandas as pd
import numpy as np
import xml.etree.ElementTree as et
import xml.dom.minidom as md

dir_path = os.path.dirname(os.path.realpath(__file__))
dir_data = 'data'

builtwork_filename = os.path.join(dir_path, dir_data, 'builtwork.csv')

KEY_BASE = 'VOCAB_ENTRY'
KEY_AAT = 'AAT ID'
KEY_NAME = 'NAME'
KEY_URL = 'URL'
KEY_ITA = 'ITA'
KEY_PARENT = 'PARENT'

def write_xml(name, text):
  output_directory = os.path.join(
        dir_path, os.path.pardir, os.path.pardir, 'transformation', 'vocabulary', dir_data)

  if not os.path.isdir(output_directory):
    os.mkdir(output_directory)

  output_filename = os.path.join(output_directory, f'{name}.xml')

  with open(output_filename, 'w') as f:
    f.write(text)

def escape_uri(text):
  return str(text).lower().replace(" ", "_")

def execute(limit):
  df_builtwork = pd.read_csv(builtwork_filename, dtype = str).fillna(value = 'None')

  for num, row in df_builtwork.iterrows():

    # XML root
    root = et.Element(KEY_BASE)

    # identifier
    name = escape_uri(row[KEY_NAME])
    tag_identifier = et.SubElement(root, 'identifier')
    tag_identifier.text = name

    # label ita
    ita = et.SubElement(root, 'ita')
    ita.text = row[KEY_ITA]

    # label eng
    eng = et.SubElement(root, 'eng')
    eng.text = row[KEY_NAME]

    # is root ?
    parent = row[KEY_PARENT]
    if parent != 'root':
      parent_uri = escape_uri(parent)
      tag_parent = et.SubElement(root, 'broader')
      tag_parent.text = parent_uri

    # URL optional
    url = row[KEY_AAT]
    if url != "None":
      tag_url = et.SubElement(root, 'related')
      tag_url.text = url

    # write XML
    final = md.parseString(et.tostring(root, method='xml')).toprettyxml()
    write_xml(name, final)
    print(name)
