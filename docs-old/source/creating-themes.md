[[
title: Creating Themes
tags: [editing]
]]

[TOC]

{tpl:versionwarning}
version: 1.0.1
{endtpl}

# Creating themes

PyKwiki themes are designed to be easy to create. 

Visit [[api]] to see a list of advanced functions and properties available to themes.

## Theme Directory Structure

    :::text
    ThemeName/
        info.yaml
        options.yaml
        menu.html
        post.html
        postlist.html
        posts.html
        search.html
        static/

* `info.yaml` - Includes information about the theme, such as author, version, and description.
* `menu.html` - Renders the site menu.
* `post.html` - Rendered for each page in `source`.
* `postlist.html` - Displays a list of posts as configured by `conf.postlist`.
* `posts.html` - Paginates `postlist-N.html`
* `search.html` - The search post.
* `static/` - All files in this directory will be copied to `docroot/static/`. 

## info.yaml

This file provide PyKwiki with some basic knowledge. 

    :::yaml
    name: Some Theme
    description: This is a special theme
    author: Your Name
    author_email: youremail
    license: MIT, GPL, BSD, etc.
    version: 1.0

## options.yaml

This *optional* file contains data used by your theme. It is a dictionary passed in to all of your theme templates as `topt`. 

Example `options.yaml` content:

    :::yaml
    # Invert the bootstrap navbar?
    invert_navbar: false
    # Custom copyright footer
    copyright_footer: &copy; 2013 My Name
    # Body background color
    background_color: #fff;

In the theme you might access these with:

    :::jinja
    <body style="background: {{topt.background_color}}">
    <div id="navbar navbar-{% if topt.invert_navbar %}inverted{% else %}default{% endif %}">
    ...    
    <div id="footer">
    {{topt.copyright_footer|default('&copy; Nobody')}} - Powered by PyKwiki
    </div>
    ...


## menu.html

This renders the PyKwiki theme. The `links` variable is made available when this template is rendered.

Here's an example link file that nests a single level deep. The following example uses a Jinja2 macro to make an infinitely nesting list.

    :::jinja
    {% macro make_links(ls) %}
        <ul>
        {% for link in ls %}
        <li>
        {% if link.href %}
            <a href="{{link.href}}" target="{{link.target|default('_self')}}">{{link.label}}</a>
        {% else %}
            <b>{{link.label}}</b>
        {% endif %}

        {% if link.children %}
            {{ make_links(link.children }}
        {% endif %}
        </li>
        {% endfor %}
        </ul>
    {%- endmacro %}
    
    {{ make_links(links) }} 

The `links` list is a list of `link` objects. The properties of a `link` object are as follows.

* `label` - The human readable link label.
* `target` - *Optional*. Specifies the value that should go in `target`, like `_self` or `_blank`.
* `href` - *Optional*. The url of the post. It may be an internal relative path to a page, or it may include `http`. 
* `rel` - PyKwiki populates this with one of `external` or `internal`. 
* `children` - *Optional*. A list of links that follow the current link.

## post.html

This is the template rendered for each source page you have. This template has access to the `conf`, `ctrl` and [post](/api.html#post-object) objects.

An example `post.html` template:

    :::jinja
    {% extends 'layout.html' %}
    {% block title %}{{post.title}}{% endblock %}
    {% block content %}
        {% for tag in post.tags %}
            <a href="{{conf.web_prefix}}/{{conf.search_tpl}}?t={{tag}}">{{tag}}</a>
        {% endfor %}
        {{post.target_text|safe}}
    {% endblock %}

## postlist.html

This page simply renders a list of pages, passed into the template as `posts`. Each member of `posts` is a [post](/api.html#post-object) object instance. 

This is rendered multiple times. 

The post list should support the three posts types from [[config.yaml]]. These are `full`, `preview`, and `blurb`. 

* `full` - Show the entire post.
* `preview` - Only a portion of the post. (For example, in a max-height, overflow hidden div).
* `blurb` - Only show the `post.blurb` text.

### Variables passed to postlist.html

* `posts` - A list of [post](/api.html#post-object) object instances.
* `page_count` - The number of postlist pages to be made.
* `post_count` - The total number of posts.
* `post_type` - One of `preview`, `full`, `blurb`.
* `this_page_num` - The page number being rendered.
* `per_page` - The number of posts per page.

An example `postlist.html` template:

    :::jinja
    
    {% for post in posts %}
    <div>
        <h2>
            <a href="{{post.url}}">{{post.title}}</a>
            <span class="pull-right text-muted">{{post.mdate_string}}</span>
        </h2>
        <div>
            {% if post_type == 'full' %}
                {{post.target_text}}
            {% elif post_type == 'preview' %}
                <div class="htmltruncate-md">
                    {{post.target_text}}
                    <div class="htmltruncate-bottom"></div>
                </div>
                <a href="{{post.url}}">...</a>
            {% else %}
                {{post.blurb}}
                <a href="{{post.url}}">Read more</a>
            {% endif %}
        </div>
    </div>
    {% endfor %}
    
## posts.html

The posts template is used when displaying lists of pages as posts. It should use Ajax or iframes to load the generated `postlist-N.html` files. 

Example `posts.html` template:

    :::jinja
    {% extends 'layout.html' %}
    {% block title %}Recent{% endblock %}
    {% block content %}
    <script>
    var this_page = 1; 
    function load_postlist_cb(data) { 
        $('#postlist_wrap').html(data);
        $('.toc').hide();
    }

    function load_postlist(page_num) { 
        if((page_num > {{page_count}})||(page_num < 1)) { 
            alert('That page does not exist');
        }
        $.get('{{conf.web_prefix}}/postlist-'+page_num+'.html',
            load_postlist_cb,
            "html");
        this_page = page_num;
    }

    $(document).ready(function() { 
        load_postlist(1);
    });

    </script>

    <button onclick="load_postlist(this_page-1);">Previous</button>
    <button onclick="load_postlist(this_page+1);">Next</button>

    <div id="postlist_wrap"></div>

    {% endblock %}

### Variables passed to posts.html

* `page_count` - The number of postlist pages to be made.
* `post_count` - The total number of posts.
* `per_page` - The number of posts per page.

## search.html

This template is used for performing client site searches. The JSON index file (`conf.index_file`) contains information about search terms. The JSON post data file (`conf.post_data_file`) contains
information about posts, such as tags and blurbs. For more information about these files and their format, see [[about-search]]. 

<div class="alert alert-info">This file is considered to be the most complicated part of theme creation. It is recommended that a theme author takes a look at one of the existing `search.html` templates to fully understand how it works.</div>


## static/

Every file in the static directory is copied to `docroot/static/`. 

Themes typically include JavaScript and CSS from this directory, example:

    :::jinja
    ...
    <script src="{{conf.web_prefix}}/static/somejavascript.js"></script>
    <link rel="stylesheet" href="{{conf.web_prefix}}/static/css/style1.css" />
    ...


# Bundling for distribution

The top-level directory in the theme zip file should be the name of your theme. It should be structured so it can be installed with the following commands:

    :::bash
    $ cd themes/
    $ unzip theme-yourtheme.zip


