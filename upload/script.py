import requests
import os
import json
import ast
import uuid
import urllib
import configparser


def execute(typology, limit, d=None, u=None, config_param='veniss'):

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
  dir_output = os.path.join(dir_path, typology, 'out')
  
  KEY_USERNAME = 'username'
  KEY_PASSWORD = 'password'
  KEY_ENDPOINT = 'endpoint'
  KEY_PREFIX = 'graph_prefix'
  
  credentials = _get_credentials(config_param)

  for root, dirs, src_files in os.walk(dir_output):
    cnt = 0
    for filename in src_files:

      if limit and cnt == int(limit):
        break

      graph_prefix = credentials[KEY_ENDPOINT]
      if KEY_PREFIX in credentials:
        graph_prefix = credentials[KEY_PREFIX]

      normal_uri = f"{graph_prefix}/resource/{typology}/{filename.replace('.ttl','')}/container/context"
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