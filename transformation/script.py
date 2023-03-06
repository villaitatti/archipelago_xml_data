# java -jar x3ml-engine-1.9.0-exejar.jar -i data/166.xml -x archipelago.x3ml -policy ../../archipelago_generator_policy.xml -o output.ttl -f text/turtle

import os
import sys

dir_path = os.path.dirname(os.path.realpath(__file__))


def base_path(name):
    return os.path.join(dir_path, name)


def execute(table_folder, limit):

    table_folder_in = os.path.join(dir_path, table_folder, 'data')
    table_folder_out = os.path.join(
        dir_path, '..', 'upload', table_folder, 'out')

    engine = base_path('x3ml-engine-1.9.0-exejar.jar')
    policy = base_path('archipelago_generator_policy.xml')
    ext = 'text/turtle'

    mapping_x3ml = os.path.join(dir_path, table_folder, 'mapping.x3ml')

    for root, dirs, src_files in os.walk(table_folder_in):

        current_folder = root.split(os.path.sep).pop()

        total = len(src_files)
        cnt = 1
        print(f'Found {total} file to transform in {current_folder}')

        if limit:
          limit = int(limit)
          total = limit

        src_files = sorted(src_files)

        for src_file in src_files:

            if limit and cnt == limit+1:
                break

            src_file_full = os.path.join(root, src_file)

            if os.path.isfile(src_file_full):

                out_file = src_file.replace('xml', 'ttl')

                if not os.path.exists(table_folder_out):
                    os.mkdir(table_folder_out)

                if table_folder == "vocab":
                    out_file_full = os.path.join(table_folder_out, current_folder,out_file)
                else:
                    out_file_full = os.path.join(table_folder_out, out_file)

                # Create parent folder if not exist
                if not os.path.exists(os.path.dirname(out_file_full)):
                  os.mkdir(os.path.dirname(out_file_full))

                command = f'java -jar {engine} -i {src_file_full} -x {mapping_x3ml} -p {policy} -o {out_file_full} -f {ext}'
                print(f'\n{out_file}\n\nRunning => {cnt}/{total}')
                print(command)
                
                os.system(command)

                cnt += 1
