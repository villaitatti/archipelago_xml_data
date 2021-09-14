from xml.dom import minidom as md, getDOMImplementation
import xml.etree.ElementTree as et
import os
import json

dir_path = os.path.dirname(os.path.realpath(__file__))
ns = {'ns': 'http://www.filemaker.com/fmpdsoresult'}

keys = {
    "row": "ROW",
    "id_event": "ID_EVENT",
    "id_person": "ID_PERSON",
    "id_place": "ID_PLACE",
    "id_bibliography": "ID_BIBLIOGRAPHY",
    "id_source": "ID_SOURCE",

    "date" : "Date",
    "pages" : "Pages",

    "role" : "Role",

    "event" : "Event",

    "name" : "Name",
    "surname" : "Surname"
}

jason = {
    "events":{},
    "people":{},
    "places":{},
    "bibliography":{},
    "sources":{}
}

events_x_bibliography_file = os.path.join(dir_path, '../../export/transformed/TBL_EVENTS_X_BIBLIOGRAPHY.xml')
events_x_people_file = os.path.join(dir_path, '../../export/transformed/TBL_EVENTS_X_PEOPLE.xml')
events_x_places_file = os.path.join(dir_path, '../../export/transformed/TBL_EVENTS_X_PLACES.xml')
events_x_sources_file = os.path.join(dir_path, '../../export/transformed/TBL_EVENTS_X_SOURCES.xml')
sources_x_people_file = os.path.join(dir_path, '../../export/transformed/TBL_SOURCES_X_PEOPLE.xml')

events_x_bibliography_tree = et.parse(events_x_bibliography_file).getroot().findall(f'ns:{keys["row"]}', ns)
events_x_people_tree = et.parse(events_x_people_file).getroot().findall(f'ns:{keys["row"]}', ns)
events_x_places_tree = et.parse(events_x_places_file).getroot().findall(f'ns:{keys["row"]}', ns)
events_x_sources_tree = et.parse(events_x_sources_file).getroot().findall(f'ns:{keys["row"]}', ns)
sources_x_people_tree = et.parse(sources_x_people_file).getroot().findall(f'ns:{keys["row"]}', ns)


def check_event_in_json(id_event):
    if id_event not in jason['events']:
        jason['events'][id_event] = {"people": {}, "places":{}, "bibliography":{}, "sources":{}}


def do_events_x_bibliography():
    for row in events_x_bibliography_tree:
        id_event = row.find(f'ns:{keys["id_event"]}', ns).text
        id_bibliography = row.find(f'ns:{keys["id_bibliography"]}', ns).text
        date = row.find(f'ns:{keys["date"]}', ns).text
        pages = row.find(f'ns:{keys["pages"]}', ns).text

        #events -> bibliography
        check_event_in_json(id_event)
        if id_bibliography not in jason['events'][id_event]['bibliography']:
            jason['events'][id_event]['bibliography'][id_bibliography] = {keys["date"]: date, keys["pages"]: pages}

        #bibliography -> events
        if id_bibliography not in jason['bibliography']:
            jason['bibliography'][id_bibliography] = {"events": {}}

        if id_event not in jason['bibliography'][id_bibliography]['events']:
            jason['bibliography'][id_bibliography]['events'][id_event] = {keys["date"]: date, keys["pages"]: pages}

    print("\033[94mevents_x_bibliography: Done.")

def do_events_x_people():
    for row in events_x_people_tree:
        id_event = row.find(f'ns:{keys["id_event"]}', ns).text
        id_person = row.find(f'ns:{keys["id_person"]}', ns).text
        role = row.find(f'ns:{keys["role"]}', ns).text

        #events -> people
        check_event_in_json(id_event)
        if id_person not in jason['events'][id_event]['people']:
            jason['events'][id_event]['people'][id_person] = {keys["role"]: role}

        #people -> #events
        if id_person not in jason['people']:
            jason['people'][id_person] = {"events": {}, "sources": {}}

        if id_event not in jason['people'][id_person]['events']:
            jason['people'][id_person]['events'][id_event] = {keys["role"]: role}

    print("\033[94mevents_x_people: Done.")

def do_events_x_places():
    for row in events_x_places_tree:
        id_event = row.find(f'ns:{keys["id_event"]}', ns).text
        id_place =  row.find(f'ns:{keys["id_place"]}', ns).text
        date = row.find(f'ns:{keys["date"]}', ns).text

        #events -> places
        check_event_in_json(id_event)
        if id_place not in jason['events'][id_event]['places']:
            jason['events'][id_event]['places'][id_place] = {keys["date"]: date}

        #places -> events
        if id_place not in jason['places']:
            jason['places'][id_place] = {"events": {}}

        if id_event not in jason['places'][id_place]['events']:
            jason['places'][id_place]['events'][id_event] = {keys["date"]: date}

    print("\033[94mevents_x_places: Done.")


def do_events_x_sources():
    for row in events_x_sources_tree:
        id_event = row.find(f'ns:{keys["id_event"]}', ns).text
        id_source =  row.find(f'ns:{keys["id_source"]}', ns).text
        event = row.find(f'ns:{keys["event"]}', ns).text

        #events -> sources:
        check_event_in_json(id_event)
        if id_source not in jason['events'][id_event]['sources']:
            jason['events'][id_event]['sources'][id_source] = {keys["event"]: event}

        #sources -> events:
        if id_source not in jason['sources']:
            jason['sources'][id_source] = {"events": {}, "people": {}}

        if id_event not in jason['sources'][id_source]['events']:
            jason['sources'][id_source]['events'][id_event] = {keys['event']: event}

    print("\033[94mevents_x_sources: Done.")


def do_sources_x_people():
    for row in sources_x_people_tree:
        id_person = row.find(f'ns:{keys["id_person"]}', ns).text
        id_source =  row.find(f'ns:{keys["id_source"]}', ns).text
        name = row.find(f'ns:{keys["name"]}', ns).text
        surname = row.find(f'ns:{keys["surname"]}', ns).text

        #sources -> people:
        if id_source not in jason['sources']:
            jason['sources'][id_source] = {"people" : {}, "events": {}}

        if id_person not in jason['sources'][id_source]['people']:
            jason['sources'][id_source]['people'][id_person] = {keys["name"]: name, keys["surname"]: surname}

        #people -> sources:
        if id_person not in jason['people']:
            jason['people'][id_person] = {"events": {}, "sources":{}}

        if id_source not in jason['people'][id_person]['sources']:
            jason['people'][id_person]['sources'][id_source] = {keys["name"]: name, keys["surname"]: surname}

    print("\033[94msources_x_people: Done.")



do_events_x_bibliography()
do_events_x_people()
do_events_x_places()
do_events_x_sources()
do_sources_x_people()

with open(os.path.join(dir_path, 'association_tables.json'), 'w') as outfile:
    json.dump(jason, outfile)

print("\033[92mAll Done!")