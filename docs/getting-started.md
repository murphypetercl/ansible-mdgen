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

Also you may want to option to download the docs as a PDF file. To do that, install the following mkdocs plugin:
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