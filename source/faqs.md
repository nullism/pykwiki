[[
title: Frequently Asked Questions
tags: [help]
]]

[TOC]

# Frequently Asked Questions

# About authoring

{section:one}

## How do I specify the date of the post?

In the [post configuration section](/authoring.html#post-data-block), set the `timestamp` key.
It must match the format from [[config.yaml]] - `timestamp_format`. 

**Example**

    :::text
    [[
    title: My Post
    tags: [stuff, moar stuff]
    timestamp: 2013-11-13 21:14
    ]]

See: [Post Data Block](/authoring.html#post-data-block) for more information.

{endsection}

## How do I set a list of posts as my homepage?

To set your home page to `posts.html` change `config.yaml` -&gt; `home_page` to the following:

    :::yaml
    ...
    home_page: posts.html
    ...

# About theming

## What theme templates are required? 

The required templates and files for a theme can be found under
[theme directory structure](/creating-themes.html#theme-directory-structure)
on the [[creating-themes]] page.


# About configuring

## What does a project directory look like?

You should checkout [[getting-started]], but it basically looks like this:

    MyProject/
        links.yaml
        config.yaml
        social.yaml
        source/
        docroot/
        themes/

## What webservers work with PyKwiki? 

Any webserver that serves static files should work with PyKwiki.
Two popular choices include Apache2 and Nginx.

## What versions of Python work with PyKwiki?

PyKwiki officially works with the following versions: 

* Python == 2.7
* Python >= 3.3

Python 3.2 is **not** supported because the Jinja2 2.6 package
does not support Python 3.2. Because PyKwiki requires Jinja2, 
there is no way around this. 

**Python 3.2 will not work**


