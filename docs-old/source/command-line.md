[[
title: PyKwiki Command Line
tags: [configuration, usage]
]]

# Basic Usage

    :::bash
    usage: pykwiki [-h] [-b BASE_PATH] [-c CONFIG_FILE]
                   {new,index,cache,info,theme} ...

    positional arguments:
      {new,index,cache,info,theme}
        new                 create a new project
        index               build the search index
        cache               cache and index posts
        info                display PyKwiki information
        theme               control built-in themes

    optional arguments:
      -h, --help            show this help message and exit
      -b BASE_PATH, --base-path BASE_PATH
                            the base directory to operate on, defaults to current
                            directory
      -c CONFIG_FILE, --config-file CONFIG_FILE
                            full path to configuration YAML file to load

# Cache posts

## Quick caching

Quick caching only changes the content of your pages. It does not rebuild the search index,
post lists (/posts.html), cache uploads, or build the site menu.

    :::bash
    $ pykwiki -c /path/to/my/config.yaml cache -q

## Forced caching

Forced caching without the `-q` flag rebuilds everything. It caches all posts, uploads, menus, and theme templates.

    :::bash 
    $ pykwiki -c /path/to/my/config.yaml cache -f

Forced caching **with** the `-q` flag caches every post, but it skips the search index, uploads, and theme files.

    :::bash
    $ pykwiki -c /path/to/my/config.yaml cache -qf

## Smart caching

Using the `cache` command by itself causes PyKwiki to attempt to detect changes and rebuild what is necessary to update your site. It rebuilds menus if `links.yaml` has been modified, it caches theme files if it detects at least one updated post, and it caches all modified posts.

    :::bash
    $ pykwiki -c /path/to/my/config.yaml cache

# Install themes

To install any of the [[themes]] included in the PyKwiki distribution, run the following command:

    :::bash
    $ pykwiki -c /path/to/my/config.yaml theme install <theme name>


