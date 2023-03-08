from email.mime import base
import xml.dom.minidom as md
import xml.etree.ElementTree as et
from datetime import datetime, timezone
import uuid
import os
import re
import json

actor_group = [123, 16, 107, 184, 73, 133, 106, 42,
               155, 17, 18, 102, 87, 86, 94, 124, 95, 89, 88, 90]

def execute(limit, sa=None):

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

  t = 'actor'

  dir_path = os.path.dirname(os.path.realpath(__file__))
  root_path = os.path.join(dir_path, os.path.pardir, os.path.pardir)
  filename = os.path.join(dir_path, 'People.xml')

  uuid_filename = os.path.join(dir_path, os.pardir, 'actor.json')
  occp_filename = os.path.join(dir_path, 'actor_occupation.json')
  occp_filename_processed = os.path.join(dir_path, 'actor_occupation-manual_processed.json')
  actor_uuid = 'actor_uuid'

  uuid_dict = {}
  if os.path.isfile(uuid_filename):
    uuid_dict = json.load(open(uuid_filename))

  # Geonames dictionary
  geonames_dict = json.load(
      open(os.path.join(root_path, 'utils', 'geonames', 'geonames.json'), 'r'))

  def write_file(row_id, text):

    output_directory = os.path.join(root_path, 'transformation', t, 'data')

    if not os.path.isdir(output_directory):
      os.mkdir(output_directory)

    output_filename = os.path.join(output_directory, f'{row_id}.xml')

    with open(output_filename, 'w') as f:
      f.write(text)

  regex_square = r'[\[\]]'
  regex_curly = r'[\{\}]'
  regex_round = r'[\(\)]'

  regex_aat = r'\[[A-Z0-9]+\]'
  regex_ita = r'{.*}'
  regex_date = r'\([0-9\-]+\)'

  # Input keys
  key_row = 'ROW'
  key_id_person = 'ID_PERSON'
  key_given_name = 'Given_Name'
  key_appellation = 'Appellation'
  key_surname = 'Surname'
  key_name = 'Name'
  key_alias = 'Alias'
  key_title = 'Title'
  key_patronymic = 'Patronymic'
  key_occuption = 'Occupation'
  key_activities_role = 'Activities_Roles'
  key_place_birth = 'Place_of_birth'
  key_place_death = 'Place_of_death'
  key_work_location = 'Work_location'
  key_birthdate_earliest = 'Birth_Date_Earliest'
  key_birthdate_latest = 'Birth_Date_Latest'
  key_deathdate_earliest = 'Death_Date_Earliest'
  key_deathdate_lastest = 'Death_Date_Latest'
  key_marriage_date = 'Marriage_Date'
  key_will_date = 'Will_Date'
  key_century = 'Century'
  key_fraction_century = 'Fraction_Century'
  key_notes = 'Notes'

  key_birth = 'birth'
  key_death = 'death'
  key_date = 'date'
  key_place = 'place'

  # Custom created keys
  key_titles = 'Titles'
  key_activities = 'Activities'
  key_activity = 'Activity'
  key_activity_subject = "subject"
  key_activity_place = "place"
  key_activity_date = "date"
  key_activity_note = "note"
  key_id = 'Id'
  key_uuid = 'UUID'
  key_start = 'Start'
  key_end = 'End'
  key_root = 'Root'
  key_work_locations = 'Work_locations'
  key_geo = 'geo'
  key_label = 'label'

  key_aat = 'aat'
  key_ita = 'ita'
  key_eng = 'eng'


  key_events = "Events"
  key_event = "Event"
  key_role = "Role"

  tree = et.parse(filename)
  root = tree.getroot()

  ns = {'ns': 'http://www.filemaker.com/fmpdsoresult'}

  tags = root.findall(f'ns:{key_row}', ns)

  all_people = []

  def explode_text(s):

    data = {}

    if s is None:
      return

    # AAT
    try:
      if re.search(regex_square, s):
        aat = re.findall(regex_aat, s)[0]
        aat = re.sub(regex_square, '', aat, re.S)

        data[key_aat] = aat.strip()

        s = re.sub(regex_aat, '', s)

    except TypeError as err:
      pass

    # ITA
    try:
      if re.search(regex_curly, s):
        ita = re.findall(regex_ita, s)[0]
        ita = re.sub(regex_curly, '', ita)

        data[key_ita] = ita.strip()

        s = re.sub(regex_ita, '', s)

    except TypeError as err:
      pass

    # DATE
    try:
      if re.search(regex_date, s):
        date = re.findall(regex_date, s)[0]
        date = re.sub(regex_round, '', date)

        dates = date.split('-')

        data[key_start] = dates[0]
        data[key_end] = dates[1]

        s = re.sub(regex_date, '', s)

    except (TypeError, IndexError) as err:
      pass

    # ENG
    try:
      data[key_eng] = s.strip()

    except TypeError as err:
      pass

    return data

  def explode_place(parent, text):
    try:
      location_id = geonames_dict[text][0]["geoname_id"]

      place_birth_id = et.SubElement(parent, key_geo)
      place_birth_id.text = location_id
    except:
      pass

    place_birth_name = et.SubElement(parent, key_label)
    place_birth_name.text = text

  def escape_uri(text):
    text = str(text).lower()
    text = text.replace(' ', '_')
    text = text.replace('.', '_')
    text = text.replace('\'', '_')
    return text

  cnt_total = 0

  occp_dict = {}
  if os.path.exists(occp_filename):
    occp_dict = json.load(open(occp_filename))

  occp_dict_processed = {}
  if os.path.exists(occp_filename_processed):
    occp_dict_processed = json.load(open(occp_filename_processed))

  # Iterate each ROW
  for row in tags:

    if limit and cnt_total == int(limit):
      break

    row_id = row.find(f'ns:{key_id_person}', ns).text

    # Actor type
    actor_type = "person"
    if int(row_id) in actor_group:
      actor_type = "group"

    # Copy the current row
    new_row = et.Element(actor_type)

    # given name
    given_name = row.find(f'ns:{key_given_name}', ns).text
    if given_name is None:
      given_name = ""

    # surname
    surname = row.find(f'ns:{key_surname}', ns).text
    surname = re.sub(regex_ita, '', surname).rstrip()

    if given_name:
      name = str(f'{surname}, {given_name}').strip()
    else:
      name = surname.strip()

    if row_id not in uuid_dict:
      uuid_dict[row_id] = {
        actor_uuid: str(uuid.uuid1()),
        key_name: name
      }

    elif not uuid_dict[row_id][key_name]:
      uuid_dict[row_id][key_name] = name

    row_id = uuid_dict[row_id][actor_uuid]

    # ID person
    id_person = et.SubElement(new_row, key_id_person)
    id_person.text = row_id

    print(f'{row_id} is of type: {actor_type}')

    if actor_type == "person":
      # given name
      node_given_name = et.SubElement(new_row, key_given_name)
      node_given_name.text = given_name

      # surname
      node_surname = et.SubElement(new_row, key_surname)
      node_surname.text = surname
      
      # alias
      alias_text = row.find(f'ns:{key_alias}', ns).text
      if alias_text is not None:
        alias = explode_text(alias_text)
        base_tag(new_row, key_alias, alias[key_eng])

      # patronymic
      patronymic = row.find(f'ns:{key_patronymic}', ns).text
      if patronymic is not None:
        base_tag(new_row, key_patronymic, escape_uri(explode_text(patronymic)[key_eng]))

    else:
      node_appellation = et.SubElement(new_row, key_appellation)
      node_appellation.text = name

    # Container
    tag_container = et.SubElement(new_row, 'container')

    parent_container = et.SubElement(tag_container, 'parent')
    parent_container.text = 'formContainer'

    label_container = et.SubElement(tag_container, 'label')
    label_container.text = f'LDP container of {name}'

    creator_container = et.SubElement(tag_container, 'creator')
    creator_container.text = 'admin'

    time_container = et.SubElement(tag_container, 'time')
    time_container.text = datetime.now(tz=timezone.utc).strftime("%Y-%m-%d %H:%M:%S")

    # Titles
    # If the text is not empty
    titles_text = row.find(f'ns:{key_title}', ns).text
    if titles_text is not None:
      titles = et.SubElement(new_row, key_titles)

      for title in titles_text.split(';'):
        base_tag(titles, key_title, escape_uri(explode_text(title)[key_eng]))

    # occupation
    occupation = row.find(f'ns:{key_occuption}', ns).text
    if occupation is not None:
      base_tag(new_row, key_occuption, escape_uri(explode_text(occupation)[key_eng]))

    # Save activities in dict
    activities_text = row.find(f'ns:{key_activities_role}', ns).text
    if activities_text is not None:
      if row_id not in occp_dict:
        occp_dict[row_id] = []

      for activity in activities_text.split(';'):
        text = explode_text(activity)
          
        # Generate new entry in dictionary
        e = { key_eng: text[key_eng] }
        if key_ita in text:
          e[key_ita] = text[key_ita]
          
          occp_dict[row_id].append(e)

    # Save activities in xml
    if occp_dict_processed and row_id in occp_dict_processed:
      node_activities = et.SubElement(new_row, key_activities)

      for current_activity in occp_dict_processed[row_id]:
        node_activity = et.SubElement(node_activities, key_activity)

        node_activity_id = et.SubElement(node_activity, key_uuid)
        node_activity_id.text = str(uuid.uuid1())
        
        node_activity_subject = et.SubElement(node_activity, key_activity_subject)
        node_activity_subject.text = escape_uri(current_activity[key_activity_subject])
        
        if key_activity_place in current_activity:
          node_activity_place = et.SubElement(node_activity, key_activity_place)
          node_activity_place.text = escape_uri(current_activity[key_activity_place])

        if key_activity_date in current_activity:
          node_activity_date = et.SubElement(node_activity, key_activity_date)
          node_activity_date.text = current_activity[key_activity_date]
        
        if key_activity_note in current_activity:
          node_activity_note = et.SubElement(node_activity, key_activity_note)
          node_activity_note.text = current_activity[key_activity_note]

    # Birth
    birth_place = row.find(f'ns:{key_place_birth}', ns).text
    birth_date = row.find(f'ns:{key_birthdate_earliest}', ns).text

    if birth_date is not None or birth_place is not None:
      birth = et.SubElement(new_row, key_birth)

      if birth_date is not None:
        # It may contain "ca."
        birth_date = birth_date.replace('ca.','')
        base_tag(birth, key_date, birth_date)

      if birth_place is not None:
        base_tag(birth, key_place, escape_uri(birth_place))

    # Death
    death_place = row.find(f'ns:{key_place_death}', ns).text
    death_date = row.find(f'ns:{key_deathdate_lastest}', ns).text

    if death_date is not None or death_place is not None:
      death = et.SubElement(new_row, key_death)

      if death_date is not None:
        base_tag(death, key_date, death_date)

      if death_place is not None:
        base_tag(death, key_place, escape_uri(death_place))

    # marriage
    marriage_date = row.find(f'ns:{key_marriage_date}', ns).text
    if marriage_date is not None:
      base_tag(new_row, key_marriage_date, marriage_date)

    # will
    will_date = row.find(f'ns:{key_will_date}', ns).text
    if will_date is not None:
      base_tag(new_row, key_will_date, will_date)

    # century
    century = row.find(f'ns:{key_century}', ns).text
    if century is not None:
      base_tag(new_row, key_century, century)

    # fraction century
    fraction_century = row.find(f'ns:{key_fraction_century}', ns).text
    if fraction_century is not None:
      base_tag(new_row, key_fraction_century, fraction_century)

    """
    # work location
    if row.find(f'ns:{key_work_location}', ns).text is not None:

      work_locations = et.SubElement(new_row, key_work_locations)

      locations = row.find(f'ns:{key_work_location}', ns).text
      locations = locations.split(';')

      for location in locations:
        explode_place(et.SubElement(work_locations,
                                    key_work_location), location.strip())
    """

    # notes
    notes = row.find(f'ns:{key_notes}', ns).text
    if notes is not None:
      notes = explode_text(notes)
      base_tag(new_row, key_notes, notes[key_eng])

    all_people.append({
        key_appellation: name,
        key_id_person: id_person.text
    })

    final = md.parseString(et.tostring(
        new_row, method='xml')).toprettyxml()

    write_file(row_id, final)

    cnt_total += 1

  open(os.path.join(dir_path, 'people.json'), 'w').write(
      json.dumps(all_people, indent=4))

  with open(occp_filename, 'w') as f:
    f.write(json.dumps(occp_dict, indent=4, sort_keys=True))

  with open(uuid_filename, 'w') as f:
    f.write(json.dumps(uuid_dict, indent=4, sort_keys=True))
