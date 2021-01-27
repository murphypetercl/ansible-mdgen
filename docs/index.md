# Introduction

Ansible-mdgen is a python package used to auto generate documentation for an ansible role. It is a highly configurable tool and uses mdUtils to create the .md files.

## How does it work?

The package reads all tasks, handlers, defaults, variables, files and templates and produces equivalent .md files in the docs directory of the role. It also allows you to configure it so that you can combine tasks, variables, templates, etc... into single .md files.

If the docs directory does not exist then it will be created. 

### Tasks
- The package iterates over each of the tasks files, parsing the yaml to extract the "name" values and "tags" values from each task and writes it to the .md file. So good descriptions on the task names will lead to better documentation.

- The package also generates a flow graph based on the include_tasks and import_tasks. This is useful in particular for larger roles to see the picture of how various task files are tied together.

### Variables
- The package iterates over all variables in the defaults and vars directories. To provide descriptions of the variables you can add the "@var:" annotation in the comment above the variable:
```
# @var: <variable_name>: <variable_description>
```
For example:
```
# @var: my_var: This is a description of my variable!
```
- The package also identifies where the variable is used in the role and this is displayed under the "Where referenced" section under each variable. This is useful to see how the variables are used and also to identify if there are variables that are unused in the role.