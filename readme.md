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
  -a TEXT               Types to iterate  [required]
  -l, --limit TEXT      Number of files to execute
  --help                Show this message and exit.
```