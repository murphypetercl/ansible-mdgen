# Configuration

Ansible-mdgen provides alot of configuration options. You can pass some configuration options via the command line but for complete configuration you would create a configuration file called .ansible-mdgen.yml in the root directory of the role.

## Command Line options

|Parameter|Description|
| :--- | :--- |
|``--project_dir``|The directory of the role that you want to document.|
|``-C --conf``|The configuration file you want to use if different to .ansible-mdgen|
|``-o``|Define the destination folder of your documenation|
|``-a``|Set .yaml as role files extension. By default .yml files are parsed|
|``-w``|Clear the output directory without asking|
|``-y``|Overwrite the output without asking|
|``--sample-config``|Print the sample configuration yaml file|
|``-V --version``|Get version|

## Configuration File

|Parameter|Description|Default|
| :--- | :--- | :--- |
|``output_dir``|Directory to output the docs|``./docs``|
|``output_tasks_dir``|Directory to output the tasks docs relative to output_dir|``tasks``|
|``output_handlers_dir``|Directory to output the handlers docs relative to output_dir|``handlers``|
|``output_defaults_dir``|Directory to output the defaults docs relative to output_dir|``defaults``|
|``output_variables_dir``|Directory to output the variables docs relative to output_dir|``variables``|
|``output_files_dir``|Directory to output the files docs relative to output_dir|``files``|
|``output_templates_dir``|Directory to output the templates docs relative to output_dir|``roletemplates``|
|``output_overwrite``|Determines if you want to overwrite the current docs in the output directory|``False``|
|``clear_output``|Determines if you want to clear all the current docs in the output directory|``False``|
|``output_templates``|Determines if you want to output the templates|``True``|
|``output_files``|Determines if you want to output the files|``True``|
|``transpose_variable_table``|Determines if you want to transpose the variable meta table|``False``|
|``yaml_extension``|Role's YAML files extension (dot should be included)|``.yml``|

### File Combinations
For file combinations see [here](../configuration/file-combinations.md)