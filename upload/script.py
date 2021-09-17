import requests
import os
import json
import ast
import uuid
import urllib


def execute(typology, limit):

  key_usr = 'usr'
  key_psw = 'psw'
  dir_out = 'out'

  dir_path = os.path.dirname(os.path.realpath(__file__))
  dir_output = os.path.join(dir_path, typology, dir_out)

  auth = json.load(open(os.path.join(dir_path, '.config'),'r'))
  for root, dirs, src_files in os.walk(dir_output):
    cnt = 0
    for filename in src_files:

      if limit and cnt == int(limit):
        break

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
      cnt+=1
