# Header content

By default, this theme does not contain any header content, it only has a sidebar and a main content window.
However, you can define your own HTML in a header that will be inserted **above everything else**.
To do so, you must define your own Sphinx Template in a specific location.
The contents of this template will be inserted into the theme.
Here is how to do this:

- Create a templates folder in your theme's root. Assuming your documentation is in the `docs/` folder:

  ```console
  $ cd docs/
  $ mkdir _templates
  ```
- Add the `_templates/` folder to your Sphinx configuration templates:

  ```python
  templates_path = ["_templates"]
  ```
- Create the following template file and add HTML to id:

  ```console
  $ echo "<p>Some text!</p>" > _templates/sections/header.html
  ```
- Build your documentation, and you should see content of this file show up above your site.

## Style the header

Note that the header has very little styling applied to it by default.
So you should [add custom styles to the theme](custom-css.md) in order to achieve the look and feel you want.
