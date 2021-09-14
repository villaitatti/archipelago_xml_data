import requests
import os
import json
import ast
import uuid
import urllib

typology = 'builtwork'

key_usr = 'usr'
key_psw = 'psw'

timestring = '%Y-%m-%dT%H:%M:%S'

key_text = 'text'
key_spans = 'spans'

key_pos = 'pos'
key_off = 'off'
key_id = 'id'

key_start = 'start'
key_end = 'end'

key_xpath_selector = 'xpath_selector'
key_text_position_selector = 'text_position_selector'

dir_path = os.path.dirname(os.path.realpath(__file__))
dir_out = 'out'
dir_txt = 'txt'
dir_rdf = 'rdf'
dir_int = 'intermediate'

dir_input = os.path.join(dir_path, dir_out, dir_txt)
dir_output = os.path.join(dir_path, os.path.pardir, typology, dir_out)

auth = json.load(open(os.path.join(dir_path, '.config'),'r'))
for root, dirs, src_files in os.walk(dir_output):
  for filename in src_files:

    graph_uri = urllib.parse.quote(f"http://archipelago.itatti.harvard.edu/resource/{typology}/{filename.replace('.ttl','')}/context", safe='') 
    request_url = f'https://archipelago.itatti.harvard.edu/rdf-graph-store?graph={graph_uri}'

    print(f'### {filename} ###')
    #DEL
    command = f'curl -u {auth.get(key_usr)}:{auth.get(key_psw)} -X DELETE -H \'Content-Type: text/turtle\' {request_url}'
    print(f'DEL\t\t{os.system(command)}')

    #POST
    command = f'curl -u {auth.get(key_usr)}:{auth.get(key_psw)} -X POST -H \'Content-Type: text/turtle\' --data-binary \'@{os.path.join(dir_output,filename)}\' {request_url}'
    print(f'POST\t\t{os.system(command)}')

    print('\n')
