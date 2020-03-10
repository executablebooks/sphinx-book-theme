# Controlling page layout

## Sidebar content

You can also specify content that should exist in the sidebar. This content
will be placed to the right, allowing it to exist separately from your main
content. To add sidebar content, use this syntax:

````
```{sidebar} **My sidebar title**
Here is my sidebar content, it is pretty cool!
```
````

```{sidebar} **Here is my sidebar content**
It is pretty cool!
```

### Adding content to sidebars

Sidebar content can include all kinds of things, such as code blocks:

````{sidebar} Code blocks in sidebars
```python
print("here is some python")
```
````

`````
````{sidebar} Code blocks in sidebars
```python
print("here is some python")
```
````
`````

as well as admonitions and images:

````{sidebar} **Notes in sidebars**
```{note}
Wow, a note with an image in a sidebar!
![](../images/cool.jpg)
```
````

`````
````{sidebar} **Notes in sidebars**
```{note}
Wow, a note with an image in a sidebar!
![](../images/cool.jpg)
```
````
`````

## Full-width content

```{note}
:class: tag_fullwidth
This is my test
```

Let's see what happens