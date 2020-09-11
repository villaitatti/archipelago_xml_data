import xml.dom.minidom as md
import xml.etree.ElementTree as et
import os
import re
import json

# TODO pass the file as arg
dir_path = os.path.dirname(os.path.realpath(__file__))
filename = os.path.join(dir_path, 'People.xml')

association_tables = json.load(open(os.path.join(dir_path, '../association_tables/', 'association_tables.json'), 'r'))

# Geonames dictionary
geonames_dict = json.load(open(os.path.join(dir_path, '../geonames/', 'geonames.json'), 'r'))

def write_file(row_id, text):

  output_directory = os.path.join(dir_path, '../..', 'transformation/people/' ,'data')

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
key_surname = 'Surname'
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


# Custom created keys
key_titles = 'Titles'
key_activities = 'Activities'
key_activity = 'Activity'
key_id = 'Id'
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


def explode_text(s, parent, current, id=None):

  if s is None:
    return 

  tag = et.SubElement(parent, current)

  # AAT
  try:
    if re.search(regex_square, s):
      aat = re.findall(regex_aat, s)[0]
      aat = re.sub(regex_square, '', aat, re.S)

      new_aat = et.SubElement(tag, key_aat)
      new_aat.text = aat.strip()

      s = re.sub(regex_aat, '', s)
    
  except TypeError as err:
    pass


  # ITA
  try:
    if re.search(regex_curly, s):
      ita = re.findall(regex_ita, s)[0]
      ita = re.sub(regex_curly, '', ita)

      new_ita = et.SubElement(tag, key_ita)
      new_ita.text = ita.strip()

      s = re.sub(regex_ita, '', s)

  except TypeError as err:
    pass

  # DATE
  try:
    if re.search(regex_date, s):
      date = re.findall(regex_date, s)[0]
      date = re.sub(regex_round, '', date)

      dates = date.split('-')

      new_start = et.SubElement(tag, key_start)
      new_start.text = dates[0]

      new_end = et.SubElement(tag, key_end)
      new_end.text = dates[1]
      
      s = re.sub(regex_date, '', s)

  except (TypeError, IndexError) as err:
    pass

  # ENG
  try:
    eng = et.SubElement(tag, key_eng)
    eng.text = s.strip()

  except TypeError as err:
    pass

def explode_place(parent, text):
  try:
      location_id = geonames_dict[text][0]["geoname_id"]
      
      place_birth_id = et.SubElement(parent, key_geo)
      place_birth_id.text = location_id
  except:
    pass

  place_birth_name = et.SubElement(parent, key_label)
  place_birth_name.text = text


# Iterate each ROW
for row in tags:

    # Copy the current row
    new_row = et.Element(key_row)
    row_id = row.find(f'ns:{key_id_person}', ns).text 

    #ID person
    id_person = et.SubElement(new_row, key_id_person)
    id_person.text = row_id

    #TODO Actor type

    # given name 
    given_name = et.SubElement(new_row, key_given_name)
    given_name.text = row.find(f'ns:{key_given_name}', ns).text

    # surname
    surname = et.SubElement(new_row, key_surname)
    surname.text = row.find(f'ns:{key_surname}', ns).text

    # alias
    explode_text(row.find(f'ns:{key_alias}', ns).text, new_row, key_alias)

    # Titles
    # If the text is not empty
    if row.find(f'ns:{key_title}', ns).text is not None:
      val_titles = row.find(f'ns:{key_title}', ns)
      val_titles = val_titles.text.split(';')

      titles = et.SubElement(new_row, key_titles)

      [explode_text(title, titles, key_title) for title in val_titles]
    
    # patronymic
    explode_text(row.find(f'ns:{key_patronymic}', ns).text, new_row, key_patronymic)

    # occupation
    explode_text(row.find(f'ns:{key_occuption}', ns).text, new_row, key_occuption)

    # activities
    if row.find(f'ns:{key_activities_role}', ns).text is not None:
      val_activities = row.find(f'ns:{key_activities_role}', ns)
      val_activities = val_activities.text.split(';')

      new_activities = et.SubElement(new_row, key_activities)

      cnt = 1

      for activity in val_activities:

        explode_text(activity, new_activities, key_activity)
        cnt += 1

    # place of birth
    explode_place(et.SubElement(new_row, key_place_birth), row.find(f'ns:{key_place_birth}', ns).text)

    # place of death
    explode_place(et.SubElement(new_row, key_place_death), row.find(f'ns:{key_place_death}', ns).text)

    # work location
    if row.find(f'ns:{key_work_location}', ns).text is not None:

      work_locations = et.SubElement(new_row, key_work_locations)

      locations = row.find(f'ns:{key_work_location}', ns).text
      locations = locations.split(';')
      
      for location in locations:
        explode_place(et.SubElement(work_locations, key_work_location), location.strip())
        

    # birthdate earliest
    birthdate_earliest = et.SubElement(new_row, key_birthdate_earliest)
    birthdate_earliest.text = row.find(f'ns:{key_birthdate_earliest}', ns).text 

    # deathdate earliest
    deathdate_latest = et.SubElement(new_row, key_deathdate_lastest)
    deathdate_latest.text = row.find(f'ns:{key_deathdate_lastest}', ns).text

    # marriage date
    marriage_date = et.SubElement(new_row, key_marriage_date)
    marriage_date.text = row.find(f'ns:{key_marriage_date}', ns).text

    # will date
    will_date = et.SubElement(new_row, key_will_date)
    will_date.text = row.find(f'ns:{key_will_date}', ns).text

    # century
    century = et.SubElement(new_row, key_century)
    century.text = row.find(f'ns:{key_century}', ns).text

    # fraction century
    fraction_century = et.SubElement(new_row, key_fraction_century)
    fraction_century.text = row.find(f'ns:{key_fraction_century}', ns).text

    # notes
    explode_text(row.find(f'ns:{key_notes}', ns).text, new_row, key_notes)

    final = md.parseString(et.tostring(
        new_row, method='xml')).toprettyxml()

    write_file(row_id, final)
