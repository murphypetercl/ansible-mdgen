# ansible-mdgen

[![<CircleCI>](https://circleci.com/gh/murphypetercl/ansible-mdgen.svg?style=svg)](https://app.circleci.com/pipelines/github/murphypetercl/ansible-mdgen?branch=main)

Generate documentation for ansible roles

## Description

This package reads all task and variables files and creates equivalent .md files in the docs directory of the role. It also allows you to configure it so that you can combine tasks into a single .md file.

If docs directory does not exist then it will be created. 

The script iterates over each of the tasks files, parsing the yaml to extract the "name" values from each task and writing it to the .md file. So good descriptions on the task names will lead to better documentation.

## To install
```
pip install ansible-mdgen
```


## To run

Call ansible-mdgen passing in the path to the role
```
ansible-mdgen <path_to_role>
```

See --help for all available options

## To configure

Create a configuration file called ansible-mdgen.yaml in the root of the project that you want to document. Alternatively rename the config file to something else and specify this in the command line using the -C or --conf options.
```
ansible-mdgen <path_to_role> --conf <name_of_config_file>
```

In the configuration file you can specify to combine various task files into a single md file for output e.g. 
```
tasks:
  combinations:
    - filename: <name_of_single_file_to_create_1>
      files_to_combine:
        - name: <name_of_file_to_include_1>
        - name: <name_of_file_to_include_2>
        - name: <name_of_file_to_include_3>
    - filename: <name_of_single_file_to_create_2>
      files_to_combine:
        - name: <name_of_file_to_include_1>
        - name: <name_of_file_to_include_2>

e.g. 

tasks:
  combinations:
    - filename: SystemSetup
      files_to_combine:
        - name: install-packages.yml
        - name: configure-services.yml
        - name: start-services.yml
    - filename: UserSetup
      files_to_combine:
        - name: create-users.yml
        - name: assign-privileges.yml
```
Combining tasks in a single .md file may be useful where related tasks have been broken down logically into different files but for documentation readability are better suited to being in one file.

## To annotate
To provide and output default variable descriptions add a comment with the var annotation as follows:
```
# @var: <variable_name>: <variable_description>
```
Note: currently only available for defaults and vars directory files...

## To debug

Pass the options -vvv for debugging

## Credits

The idea for this project is based on (and includes some code from) [ansible-autodoc](https://github.com/AndresBott/ansible-autodoc) by Andres Bott so credit to him for his work.