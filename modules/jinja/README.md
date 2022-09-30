# Jinja

## Resource
- [official doc](https://jinja.palletsprojects.com/en/3.1.x/)

## Basics
- Jinja’s philosophy is that while application logic belongs in Python if possible, it shouldn’t make the template designer’s job difficult by restricting functionality too much.
- Jinja uses a central object called the template Environment. Instances of this class are used to store the configuration and global objects, and are used to load templates from the file system or other locations.
- The high-level API is the API you will use in the application to load and render Jinja templates.
  - To load a template from this environment, call the `get_template()` method, which returns the loaded `Template`
  - To render it with some variables, call the `render()` method.

## About Jinja template (engine)
- A Jinja template is simply a text file. Jinja can generate any text-based format (HTML, XML, CSV, LaTeX, etc.).
- Any file can be loaded as a template, regardless of file extension.
  - Adding a .jinja extension may make it easier for some IDEs or editor plugins, but is not required.
  - Another good heuristic for identifying templates is that they are in a templates folder, regardless of extension.
- A template contains
  - **variables** and/or **expressions**, which get replaced with values when a template is rendered;
  - and **tags**, which control the logic of the template.
- delimiters (with default configs):
  - `{% ... %}` for **Statements**
  - `{{ ... }}` for **Expressions** to print to the template output
  - `{# ... #}` for **Comments** not included in the template output
