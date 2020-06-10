import pandas as pd
import xml.dom.minidom as md
import xml.etree.ElementTree as et
import os

# TODO pass the file as arg
dir_path = os.path.dirname(os.path.realpath(__file__))
filename = os.path.join(dir_path, 'People.xml')

# Input keys
key_row = 'ROW'
key_title = 'Title'

# Custom created keys
key_titles = 'Titles'

tree = et.parse(filename)
root = tree.getroot()

# Iterate each ROW
for row in root.findall(key_row):

  # Copy the current row
  new_row = et.Element(key_row)

  # Titles
  if row.find(key_title).text is not None:
    val_titles = row.find(key_title)
    val_titles = val_titles.text.split(' ; ')

    titles = et.SubElement(new_row, key_titles)

    for title in val_titles:
      new_title = et.SubElement(titles, key_title)
      new_title.text = title.strip()

  final = md.parseString(et.tostring(
      new_row, encoding='utf8', method='xml')).toprettyxml()
  print(final)