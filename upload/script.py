import requests
import os
import json
import ast
import uuid
import urllib
import configparser

out_dir = 'out'

def execute(typology, limit, d=None, u=None, config_param='veniss', sa=None):

  def _get_credentials(type):
    config = configparser.ConfigParser()
    try:
      path = os.path.join(dir_path, 'config.ini')
      config.read(path)

      return {
        KEY_USERNAME: config.get(type, KEY_USERNAME),
        KEY_PASSWORD: config.get(type, KEY_PASSWORD),
        KEY_ENDPOINT: config.get(type, KEY_ENDPOINT),
        KEY_PREFIX: config.get(type, KEY_PREFIX)
      }
      
    except Exception as ex:
      print('Error. Have you created the psw.ini file? see readme.md')

  dir_path = os.path.dirname(os.path.realpath(__file__))
  dir_output = os.path.join(dir_path, typology, out_dir)
  
  KEY_USERNAME = 'username'
  KEY_PASSWORD = 'password'
  KEY_ENDPOINT = 'endpoint'
  KEY_PREFIX = 'graph_prefix'
  
  credentials = _get_credentials(config_param)

  for root, dirs, src_files in os.walk(dir_output):

    # Execute if SA is not set, or it is set and current folder is in SA
    current_folder = os.path.basename(root)
    if (sa is None or len(sa) == 0) or (sa is not None and current_folder in sa):
      cnt = 0

      for filename in src_files:

        if limit and cnt == int(limit):
          break

        graph_prefix = credentials[KEY_ENDPOINT] if KEY_PREFIX in credentials else credentials[KEY_PREFIX]

        if (sa is not None and len(sa) > 0):
          normal_uri =  f"{graph_prefix}/resource/{typology}/{current_folder}/{filename.replace('.ttl','')}/container/context"
        else:
          normal_uri =  f"{graph_prefix}/resource/{typology}/{filename.replace('.ttl','')}/container/context"
        
        graph_uri = urllib.parse.quote(normal_uri, safe='') 
        request_url = f'{credentials[KEY_ENDPOINT]}/rdf-graph-store?graph={graph_uri}'

        print(f'### {normal_uri}')

        #DEL
        if d:
          command = f'curl -u {credentials[KEY_USERNAME]}:{credentials[KEY_PASSWORD]} -X DELETE -H \'Content-Type: text/turtle\' {request_url}'
          print(f'DEL\t\t{os.system(command)}')

        #POST
        if u:
          command = f'curl -u {credentials[KEY_USERNAME]}:{credentials[KEY_PASSWORD]} -X POST -H \'Content-Type: text/turtle\' --data-binary \'@{os.path.join(root,filename)}\' {request_url}'
          print(f'POST\t\t{os.system(command)}')

        print('\n')
        cnt+=1

  if u:
    command = f'curl -u {credentials[KEY_USERNAME]}:{credentials[KEY_PASSWORD]} -H \'Content-Type: application/sparql-update; charset=UTF-8\' -H \'Accept: text/boolean\' -d \'@{os.path.join(dir_path, "remove_type.sq")}\' {credentials[KEY_ENDPOINT]}/sparql'
    print(f'DEL ?s a arconto:Remove\t\t{os.system(command)}') 

    command = f'curl -u {credentials[KEY_USERNAME]}:{credentials[KEY_PASSWORD]} -H \'Content-Type: application/sparql-update; charset=UTF-8\' -H \'Accept: text/boolean\' -d \'@{os.path.join(dir_path, "remove_prop.sq")}\' {credentials[KEY_ENDPOINT]}/sparql'
    print(f'DEL ?s arconto:Remove ?o\t{os.system(command)}') 