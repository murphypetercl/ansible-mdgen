# File combinations

You may not want to produce .md for all your role files. With the combinations configuration you can specify which files to output and also which files you would like to combine. For example you may have several task files but would like to just create one .md file with all the tasks from these files. To do that you would add the following configuration:
```
<file_type>:
  combinations:
    - filename: <name_of_file_to_create_1>
      files_to_combine:
        - name: <name_of_file_to_include_1>
        - name: <name_of_file_to_include_2>
        - name: <name_of_file_to_include_3>
    - filename: <name_of_file_to_create_2>
      files_to_combine:
        - name: <name_of_file_to_include_1>
        - name: <name_of_file_to_include_2>
```
- ``<file_type>`` could be tasks, handlers, defaults, variables, files or templates.
- ``<name_of_file_to_create_x>`` is the name of the file that you want to create and includes all the documentation from the ``<name_of_file_to_include_y>`` in the files_to_combine list

e.g.
```
tasks:
  combinations:
    - filename: main
      files_to_combine:
        - name: main.yml
    - filename: users
      files_to_combine:
        - name: minio/users.yml
    - filename: file-system
      files_to_combine:
        - name: volumes.yml
        - name: directories.yml
    - filename: minio
      files_to_combine:
        - name: minio/minio.yml
        - name: minio/firewall.yml
```