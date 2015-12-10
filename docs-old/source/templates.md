[[
title: Helper Templates
tags: [authoring, editing]
]]

[TOC]

# Helper Templates

This page contains a collection of templates that may be considered useful. 

## Simple Tables

This template is a quick way to add simple tables without writing HTML. 
It takes two arguments: 

* `headers` - An *optional* YAML list specifying `<th>` elements - column headers.
* `rows` - A nested YAML list of rows and columns.

### Template

    :::html
    <table class="table">
    {% if headers %}
        <thead>
        <tr>
        {% for head in headers %}
            <th>{{head}}</th>
        {% endfor %}
        </tr>
        </thead>
    {% endif %}
    <tbody>
    {% for row in rows %}
        <tr>
        {% for col in row %}
            <td>{{col}}</td>
        {% endfor %}
        </tr>
    {% endfor %}
    </tbody>
    </table>

### Usage

Assuming you've saved this template as `source/table.tpl`:

    :::text
    {tpl:table}
    headers:
    - Column One
    - Column Two
    - Column Three
    rows: 
    -
        - Row 1, Col 1
        - Row 1, Col 2
        - Row 1, Col 3
    -
        - Row 2, Col 1
        - Row 2, Col 2
        - Row 2, Col 3
    -
        - ''
        - Row 3, Col 2
        - ''
    {endtpl}

Alternatively, you can use *nested brackets* for YAML lists, like so:

    :::text
    {tpl:table}
    headers: [Column One, Column Two, Column Three]
    rows: [
        [ "Row 1, Col 1", "Row 1, Col 2", "Row 1, Col 3"],
        [ "Row 2, Col 1", "Row 2, Col 2", "Row 2, Col 3"],
        [ "", "Row 3, Col 2", ""]
    ]
    {endtpl}
    

### Example

{tpl:table}
headers:
- Column One
- Column Two
- Column Three
rows: 
-
    - Row 1, Col 1
    - Row 1, Col 2
    - Row 1, Col 3
-
    - Row 2, Col 1
    - Row 2, Col 2
    - Row 2, Col 3
-
    - ''
    - Row 3, Col 2
    - ''
{endtpl}

## Responsive Bootstrap Thumbnails

This simple template is designed to be used with "Bootstrap 3" enabled themes, and accepts the following arguments:

* `image` - The web path to the image file
* `caption` - An optional text caption to display
* `width` - Optionally alter the thumbnail width, default 90%.
    * Uses CSS widths, such as `200px` or `50%`. 

### Template

    :::html
    <div style="text-align: center; margin-top: 10px; margin-bottom: 10px;">
        <div class="thumbnail" style="margin: auto; 
                width: {{width|default('90%')}}; 
                background: #f5f5f5; 
                text- align: center;">
            <a href="/uploads/{{image}}" target="_blank">
                <img src="/uploads/{{image}}" class="img-responsive" 
                    style="margin: auto;"/>
            </a>
            {% if caption %}
            <div class="caption">
                <p class="text-muted">{{caption}}</p>
            </div>
            {% endif %}
        </div>
    </div>

### Usage

Assuming the above template was saved as `source/thumb.tpl`, usage would be:

    :::text
    Here's an image:
    
    {tpl:thumb}
    image: someimage.png
    caption: This is my image!
    width: 300px
    {endtpl}


