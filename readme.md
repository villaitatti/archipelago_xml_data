Add requirements with:
```
pip3 install to-requirements.txt
```


Execute the python script with these options. E.g. `python archipelago_xml_data.py -a event -p -u`
```
Usage: archipelago_xml_data.py [OPTIONS]

Options:
  -e, --extraction      Execute the extraction
  -p, --preprocessing   Execute the pre-processing
  -t, --transformation  Execute the transformation
  -u, --upload          Execute the upload
  -d, --delete          Execute the delete
  -c, --config          Name of upload configuration to use in config.ini
  -a TEXT               Types to iterate  [required]
  -l, --limit TEXT      Number of files to execute
  --help                Show this message and exit.
```


## Username and Password

When specifying paramters `-u -d` you sould also add a file called `config.ini` in the `upload` directory.
It sould be constructed as following:

```
[online]
username = USERNAME   #replace with your username
password = PASSWORD   #replace with your password
endpoint = ENDPOINT   #replace with your endpoint
graph_prefix = PREFIX #replace with the prefix the graphs should have
```

In this case, please add parameter `-c online` when running the script. **Note:** -c parameter must match the configuration parameter, in this case "online".