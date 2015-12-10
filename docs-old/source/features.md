[[
title: Features
tags: [features]
timestamp: 2013-10-12 14:21
]]

# Features

An overview of PyKwiki's most important features.
See also: [[comparison]]

<div class="row">

{tpl:feature}
    name: Recent Posts
    class: col-sm-4
    description: PyKwiki works well for blogs,
        review sites, or anything else that needs
        a "recent posts" type of feature.
    screenshot: /uploads/features/recent_posts.png
    link: /posts.html
    link_label: Try it out &raquo; 
{endtpl}

{tpl:feature}
    name: Ranked Searching
    class: col-sm-4
    description: PyKwiki indexes your pages when you change them.
        This index is a pure JSON file optimized for fast searches.
    screenshot: /uploads/features/builtin-search.png
    link: /about-search.html
{endtpl}


{tpl:feature}
name: Post Templates
class: col-sm-4
description: Easily create complex templates
    using Jinja2 syntax and the built-in <code>tpl</code>
    Markdown extension.
screenshot: /uploads/features/templates.png
link: /extensions.html#pykwikiexttpl
{endtpl}

</div><!-- End row -->

<div class="row">

{tpl:feature}
name: Markdown Editing
class: col-sm-4
description: Edit posts using an efficient 
    and well supported format. No more messing
    with broken WYSIWYG tools &mdash; you can use any text
    editor you prefer.
screenshot: /uploads/pykwiki-screenshot-editor.png
link: /markdown.html
{endtpl}

{tpl:feature}
name: Easy Setup
class: col-sm-4
description: Because PyKwiki does not use a database
    or require WSGI, PHP, or any other server side scripting,
    setup is a breeze.
screenshot: /uploads/features/easy-setup.png 
link: /getting-started.html
{endtpl}

{tpl:feature}
name: Fastest Page Loads
class: col-sm-4
description: By skipping the database and
    saving server side processing for "compile"
    time, PyKwiki loads pages as fast as your
    webserver can serve static files.
screenshot: /uploads/pykwiki-screenshot-speed.png 
link: /speed.html
{endtpl}

</div><!-- End row -->

<div class="row">
{tpl:feature}
name: Security
class: col-sm-4
description: Because PyKwiki is simply a collection of
    compiled static files, it's as secure as your webserver.
{endtpl}

{tpl:feature}
name: Beautiful
class: col-sm-4
description: By default, PyKwiki gives you all the beauty and 
    elegance of Bootstrap. 
screenshot: /uploads/themes/pykwiki-theme-amelia.png
link: /themes.html
{endtpl}

{tpl:feature}
name: Feeds
class: col-sm-4
description: Since version 1.0.6, Pykwiki supports automatic RSS
    feeds, if an rss.xml template is present in the theme.
screenshot: /uploads/features/rss.png
{endtpl}

</div>
