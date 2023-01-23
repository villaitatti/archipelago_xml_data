import click
import importlib
import transformation.script as transformation
import upload.script as upload

@click.command()
@click.option('-p', '--preprocessing', 'exec_preprocessing', is_flag=True, help="Execute the pre-processing")
@click.option('-t', '--transformation', 'exec_transformation', is_flag=True, help="Execute the transformation")
@click.option('-u', '--upload', 'exec_upload', is_flag=True, help="Execute the upload", default=False)
@click.option('-d', '--delete', 'exec_delete', is_flag=True, help="Execute the delete", default=False)
@click.option('-c', '--config', 'config', help="configuration option", default='veniss')
@click.option('-a', required=True, multiple=True, help="Types to iterate")
@click.option('-l', '--limit', help="Number of files to execute", default=None)

def execute_pipeline(exec_preprocessing, exec_transformation, exec_upload, exec_delete, a, limit, config):

  if limit:
    print(f'A limit of {limit} as been passed.')

  for file in a:

    print(f'\n{file}')

    if exec_preprocessing:
      try:
        print('Executing preprocessing ...')
        mod = importlib.import_module(f'preprocessing.{file}.script')
        mod.execute(limit)
        print('Done preprocessing.')
      
      except ImportError as err:
        print('Error:', err)

      print()

    if exec_transformation:
      print('Executing transformation ...')
      transformation.execute(file, limit)
      print('Done transformation.\n')

    if exec_upload or exec_delete:
      print('Calling RS graph api...')
      upload.execute(file, limit, exec_delete, exec_upload, config)
      print('Done.\n')

if __name__ == '__main__':
    execute_pipeline()