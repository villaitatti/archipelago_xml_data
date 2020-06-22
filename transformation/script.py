import os

dir_path = os.path.dirname(os.path.realpath(__file__))

def base_path(name):
    return os.path.join(dir_path, name)

table_folder = base_path('people')
table_folder_in = os.path.join(table_folder, 'data')
table_folder_out = os.path.join(table_folder, 'out')

engine = base_path('x3ml-engine-1.9.0-exejar.jar')
policy = base_path('archipelago_generator_policy.xml')
ext = 'text/turtle'

mapping_x3ml = os.path.join(table_folder, 'mapping.x3ml')

for root, dirs, src_files in os.walk(table_folder_in):

    total = len(src_files)
    cnt = 1

    for src_file in src_files:

        src_file_full = os.path.join(table_folder_in, src_file)

        if os.path.isfile(src_file_full): 

            out_file = src_file.replace('xml', 'ttl')

            if not os.path.exists(table_folder_out):
                os.mkdir(table_folder_out)

            out_file_full = os.path.join(table_folder_out, out_file)

            print(f'Running => {cnt}/{total}')
            os.system(f'java -jar {engine} -i {src_file_full} -x {mapping_x3ml} -p {policy} -o {out_file_full} -f {ext}')

            cnt += 1

'java -jar x3ml-engine-1.9.0-exejar.jar -i data/166.xml -x archipelago.x3ml -policy ../../archipelago_generator_policy.xml -o output.ttl -f text/turtle'