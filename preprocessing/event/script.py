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


t = 'event'

dir_path = os.path.dirname(os.path.realpath(__file__))
root_path = os.path.join(dir_path, os.path.pardir, os.path.pardir)
dir_extraction = os.path.join(root_path, 'extraction', 'transformed')

filename = os.path.join(dir_path, 'Events.xml')
uuid_filename = os.path.join(dir_path, os.pardir, 'events.json')


####### KEYS ###########
KEY_ROW = 'ROW'
KEY_UUID = "UUID"

KEY_ID_BIBLIOGRAPHY = 'ID_BIBLIOGRAPHY'
KEY_ID_PERSON = 'ID_PERSON'
KEY_ID_ACTOR = 'ID_ACTOR'
KEY_ID_PLACE = 'ID_PLACE'
KEY_ID_SOURCE = 'ID_SOURCE'


# INPUT
IN_KEY_EVENT_ID = 'ID_EVENT'
IN_KEY_EVENT_NAME = 'Name_Event'
IN_KEY_EVENT_TYPOLOGY = 'Subtypology'
IN_KEY_EVENT_SYNOPSIS = 'Synopsis'
IN_KEY_EVENT_DATE_EARLIEST = 'Date_Earliest'
IN_KEY_EVENT_CENTURY = 'Century'
IN_KEY_EVENT_FRACTION_CENTURY = 'Fraction_century'


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

OUT_KEY_EVENT_DATE_NOTE = 'note'
OUT_KEY_EVENT_DATE = 'date'
OUT_KEY_EVENT_DAY = 'day'
OUT_KEY_EVENT_MONTH = 'month'
OUT_KEY_EVENT_YEAR = 'year'

vocab_event = json.load(
    open(os.path.join(dir_path, os.pardir, 'vocab_event.json')))


def execute(limit, sa=None):

  tree = et.parse(filename)
  tags = tree.getroot().findall(KEY_ROW)

  uuid_dict = {}
  if os.path.exists(uuid_filename):
    uuid_dict = json.load(open(uuid_filename))

  cnt_total = 0

  # Iterate each ROW
  for row in tags:

    if limit and cnt_total == int(limit):
      break

    # Copy the current row
    new_row = et.Element(KEY_ROW)

    # Stora row id and its UUID
    row_id = row.find(IN_KEY_EVENT_ID).text

    if row_id not in uuid_dict:
      uuid_dict[row_id] = {
          KEY_UUID: str(uuid.uuid1())
      }

    row_uuid = uuid_dict[row_id][KEY_UUID]

    # Row ID
    node_event_id = et.SubElement(new_row, OUT_KEY_EVENT_ID)
    node_event_id.text = row_uuid

    # Name Event
    event_name = row.find(IN_KEY_EVENT_NAME).text
    node_event_name = et.SubElement(new_row, OUT_KEY_EVENT_NAME)
    node_event_name.text = event_name

    # Typology
    event_typology = row.find(IN_KEY_EVENT_TYPOLOGY).text
    if event_typology and event_typology in vocab_event:
      event_typology = event_typology.lower()
      node_event_typology = et.SubElement(new_row, OUT_KEY_EVENT_TYPOLOGY)
      node_event_typology.text = vocab_event[event_typology]['uuid_vocab']

    # Synopsis
    event_synopsis = row.find(IN_KEY_EVENT_SYNOPSIS)
    node_event_synopsis = et.SubElement(new_row, OUT_KEY_EVENT_SYNOPSIS)
    node_event_synopsis.text = event_synopsis

    # Date

    try:
      date_total = row.find(IN_KEY_EVENT_DATE_EARLIEST).text
      date_parse = datetime.strptime(date_total, '%Y-%m-%d')

      node_event_date = et.SubElement(new_row, OUT_KEY_EVENT_DATE)

      if date_parse.year:
        node_event_year = et.SubElement(node_event_date, OUT_KEY_EVENT_YEAR)
        node_event_year.text = str(date_parse.year)

      if date_parse.month:
        node_event_month = et.SubElement(node_event_date, OUT_KEY_EVENT_MONTH)
        node_event_month.text = str(date_parse.month)

      if date_parse.day:
        node_event_day = et.SubElement(node_event_date, OUT_KEY_EVENT_DAY)
        node_event_day.text = str(date_parse.day)

      century = row.find(IN_KEY_EVENT_CENTURY).text
      century_fraction = row.find(IN_KEY_EVENT_FRACTION_CENTURY).text

      notes = ''
      
      if century is not None:
        notes = notes + century + ' '
      if century_fraction is not None:
        notes = notes + century_fraction

      if notes:
        node_notes = et.SubElement(node_event_date, OUT_KEY_EVENT_DATE_NOTE)
        node_notes.text = notes
    except ValueError as err:
      print(err)
    

    # Container
    tag_container = et.SubElement(new_row, 'container')

    parent_container = et.SubElement(tag_container, 'parent')
    parent_container.text = 'formContainer'

    label_container = et.SubElement(tag_container, 'label')
    label_container.text = f'LDP container of Event {row_id}'

    creator_container = et.SubElement(tag_container, 'creator')
    creator_container.text = 'admin'

    time_container = et.SubElement(tag_container, 'time')
    time_container.text = datetime.now(
        tz=timezone.utc).strftime("%Y-%m-%d %H:%M:%S")

    # Save files
    final = md.parseString(et.tostring(
        new_row, method='xml')).toprettyxml()
    _write_file(row_uuid, final)

    with open(uuid_filename, 'w') as f:
      f.write(json.dumps(uuid_dict, indent=4, sort_keys=True))

    cnt_total += 1
