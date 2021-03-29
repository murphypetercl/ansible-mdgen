# Getting Started

## To Install

Install using pip as follows:
```
pip install ansible-mdgen
```

## To run

Call ansible-mdgen passing in the path to the role
```
ansible-mdgen <path_to_role>
```

That's it! You should now see a docs directory in your role with all the various md files.

## To annotate
To provide and output variable descriptions add a comment with the var annotation as follows:
```
# @var: <variable_name>: <variable_description>
```

You may want to provide further details on the variable. To do this create an @var block as follows:
```
# @var: 
# <variable_name>:
#   description: <variable_description>
#   <some_meta>: <some_value>
#   <some_other_meta>: <some_other_value>
# @var_end
```
For example:
```
# @var: 
# minio_server_datadirs:
#   description: Minio server data directory
#   type: string
#   vault_required: true
# @var_end
```
This will be displayed as follows:

<strong>minio_server_datadirs</strong>

Minio server data directory
...
  
```

/var/lib/minio
...
  
```
|Type|Vault required|Where referenced|
| :--- | :--- | :--- |
|string|True|templates/minio.env.j2<br/>|

If there are many var fields you may want to transpose the table for a better visual display. To do this set the transpose_variable_table variable to True in your configuration file. The output will then be displayed as follows:

<strong>minio_server_datadirs</strong>

Minio server data directory
...
  
```

/var/lib/minio
...
  
```
|Meta|Value|
| :--- | :--- |
|<strong>Type</strong>|string|
|<strong>Vault required</strong>|True|
|<strong>Where referenced</strong>|templates/minio.env.j2<br/>|

## To debug

Pass the options -vvv for debugging

## Next steps

As you can tell this ties in nicely with mkdocs. If not done already then create an mkdocs.yml file in the root of your role directory. To view the Tasks flow page correctly you will require the mermaid2 plugin:
```
pip install mkdocs-mermaid2-plugin
```
And add the following plugin to mkdocs.yml
```
plugins:
  - search
  - mermaid2
```

Run the following to serve your docs locally:
```
mkdocs serve
```
See [here](https://www.mkdocs.org/) for more details on mkdocs.

### Tips

I like to use the [material theme](https://squidfunk.github.io/mkdocs-material/getting-started/) for displaying my docs similar to the docs you are looking at right now but that is completely an end user choice.

Also you may want the option to download the docs as a PDF file. To do that, install the following mkdocs plugin:
```
mkdocs-with-pdf
```
And add the configuration to your mkdocs.yml
```
plugins:
  - search
  - mermaid2
  - with-pdf:
      author: Peter Murphy
      copyright: My Company
      cover_subtitle: Ansible role to deploy and configure Minio in distributed mode
      toc_level: 2
```

Also it helps to add in navigation to display the documentation in the correct order:
e.g.
```
nav:
  - index.md
  - Defaults:
    - defaults/main.md
  - Vars:
    - variables/main.md
  - Tasks:
    - tasks/flow.md
    - tasks/main.md
    - tasks/users.md
    - tasks/file-system.md
    - tasks/minio.md
  - Templates:
      - roletemplates/minio.env.j2.md
      - roletemplates/minio.init.j2.md
      - roletemplates/minio.service.j2.md
  - Handlers:
    - handlers/main.md
  - appendix.md
```