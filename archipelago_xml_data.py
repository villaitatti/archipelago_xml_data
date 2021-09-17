import click
import importlib
import transformation.script as transformation
import upload.script as upload

@click.command()
@click.option('-e', '--extraction', 'exec_extraction', is_flag=True, help="Execute the extraction")
@click.option('-p', '--preprocessing', 'exec_preprocessing', is_flag=True, help="Execute the pre-processing")
@click.option('-t', '--transformation', 'exec_transformation', is_flag=True, help="Execute the transformation")
@click.option('-u', '--upload', 'exec_upload', is_flag=True, help="Execute the upload")
@click.option('-a', required=True, multiple=True, help="Types to iterate")
@click.option('-l', '--limit', help="Number of files to execute", default=None)

def execute_pipeline(exec_extraction, exec_preprocessing, exec_transformation, exec_upload, a, limit):

  if limit:
    print(f'A limit of {limit} as been passed.')

  for file in a:

    print(f'\n{file}')

    if(exec_preprocessing):
      try:
        print('Executing preprocessing ...')
        mod = importlib.import_module(f'preprocessing.{file}.script')
        mod.execute(limit)
        print('Done preprocessing.')
      
      except ImportError as err:
        print('Error:', err)

      print()

    if(exec_transformation):
      print('Executing transformation ...')
      transformation.execute(file, limit)
      print('Done transformation.\n')

    if(exec_upload):
      print('Executing upload...')
      upload.execute(file, limit)
      print('Done upload.\n')

if __name__ == '__main__':
    execute_pipeline()