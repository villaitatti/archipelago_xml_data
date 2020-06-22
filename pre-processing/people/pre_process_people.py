import pandas as pd
import xml.dom.minidom as md
import xml.etree.ElementTree as et
import os
import re
import json

# TODO pass the file as arg
dir_path = os.path.dirname(os.path.realpath(__file__))
filename = os.path.join(dir_path, 'People.xml')

# Geonames dictionary
geonames_dict = json.load(open(os.path.join(dir_path, 'geonames.json'),'r'))

def write_file(row_id, text):

  output_directory = os.path.join(dir_path, '..', 'script' ,'data')

  if not os.path.isdir(output_directory):
    os.mkdir(output_directory)

  output_filename = os.path.join(output_directory, f'{row_id}.xml')

  with open(output_filename, 'w') as f:
    f.write(text)

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

tree = et.parse(filename)
root = tree.getroot()

ns = {'ns': 'http://www.filemaker.com/fmpdsoresult'}

tags = root.findall(f'ns:{key_row}', ns)

# Iterate each ROW
for row in tags:

    # Copy the current row
    new_row = et.Element(key_row)
    row_id = row.find(f'ns:{key_id_person}', ns).text 

    #ID person
    id_person = et.SubElement(new_row, key_id_person)
    id_person.text = row_id

    # given name 
    given_name = et.SubElement(new_row, key_given_name)
    given_name.text = row.find(f'ns:{key_given_name}', ns).text

    # surname
    surname = et.SubElement(new_row, key_surname)
    surname.text = row.find(f'ns:{key_surname}', ns).text

    # alias
    alias = et.SubElement(new_row, key_alias)
    alias.text = row.find(f'ns:{key_alias}', ns).text

    # Titles
    if row.find(f'ns:{key_title}', ns).text is not None:
      val_titles = row.find(f'ns:{key_title}', ns)
      val_titles = val_titles.text.split(' ; ')

      titles = et.SubElement(new_row, key_titles)

      for title in val_titles:
        new_title = et.SubElement(titles, key_title)
        new_title.text = title.strip()

    # patronymic
    patronymic = et.SubElement(new_row, key_patronymic)
    patronymic.text = row.find(f'ns:{key_patronymic}', ns).text

    # occupation
    occupation = et.SubElement(new_row, key_occuption)
    occupation.text = row.find(f'ns:{key_occuption}', ns).text

    # activities
    if row.find(f'ns:{key_activities_role}', ns).text is not None:
      val_activities = row.find(f'ns:{key_activities_role}', ns)
      val_activities = val_activities.text.split(';')

      new_activities = et.SubElement(new_row, key_activities)

      cnt = 1

      for activity in val_activities:
        new_activity = et.SubElement(new_activities, key_activity)

        id_activity = et.SubElement(new_activity, key_id)
        id_activity.text = str(cnt)

        new_title = et.SubElement(new_activity, key_title)
        new_title.text = re.sub(r'\([0-9-:]*\)', '', activity).strip()

        new_start = et.SubElement(new_activity, key_start)
        new_end = et.SubElement(new_activity, key_end)
        activity_dates = re.sub(r'[^0-9-:]', '', activity)

        if len(activity_dates) > 0:
          activity_date = activity_dates.split(':')

          new_start.text = activity_date[0]

          if len(activity_date) > 1:
            new_end.text = activity_date[1]

        cnt += 1

    # place of birth
    place_birth = et.SubElement(new_row, key_place_birth)
    place_birth.text = row.find(f'ns:{key_place_birth}', ns).text
    
    # place of death
    place_death = et.SubElement(new_row, key_place_death)
    place_death.text = row.find(f'ns:{key_place_death}', ns).text

    # work location
    if row.find(f'ns:{key_work_location}', ns).text is not None:

      work_locations = et.SubElement(new_row, key_work_locations)

      locations = row.find(f'ns:{key_work_location}', ns).text
      locations = locations.split(' ; ')
      
      for location in locations:
        work_location = et.SubElement(work_locations, key_work_location)
        work_location.text = location

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
    notes = et.SubElement(new_row, key_notes)
    notes.text = row.find(f'ns:{key_notes}', ns).text

    final = md.parseString(et.tostring(
        new_row, method='xml')).toprettyxml()

    write_file(row_id, final)
