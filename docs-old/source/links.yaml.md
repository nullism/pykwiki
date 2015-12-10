[[
title: links.yaml
tags: [configuration]
]]

# links.yaml


The `links.yaml` file specifies how PyKwiki should generate a menu for your site. 

**Example of the structure of a link:**

    :::yaml
    - Example Link Name:
        # PyKwiki page name, relative to the source directory, *optional*
        post: external-links
        # Used in <a href=>, *optional* 
        href: http://google.com
        # Target attribute, *optional*, defaults to _self
        target: _blank
        # Title is used in <a title=>, *optional*
        title: Some Website or Page
        # Children is used to specify sub link hierarchy, *optional*
        children: []

## Full menu example

    :::yaml
    - Home:
        post: home
        title: Visit the home page
    - GitHub:
        href: https://github.com/nullism/pykwiki
        title: Checkout the source code!
        target: _blank
    - About:
        children:
        - About The Author:
            post: about-the-author
        - About The Site:
            post: about-the-site
        - About PyKwiki:
            href: http://pykwiki.nullism.com/about.html
            target: _blank


        
