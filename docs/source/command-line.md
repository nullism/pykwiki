[[
title: Command Line Usage
tags: [pykwiki-cli]
]]

# Command Line Usage

    :::text
    usage: pykwiki [-h] [-b BASE_PATH] [-c CONFIG_FILE] [-v]
                   {new,upgrade,index,cache,info,style} ...

    positional arguments:
      {new,upgrade,index,cache,info,style}
        new                 create a new project
        upgrade             upgrade a project from 1.x to 2.x
        index               build the search index
        cache               cache and index posts
        info                display PyKwiki information
        style               display style information

    optional arguments:
      -h, --help            show this help message and exit
      -b BASE_PATH, --base-path BASE_PATH
                            the base directory to operate on, defaults to current
                            directory
      -c CONFIG_FILE, --config-file CONFIG_FILE
                            full path to configuration YAML file to load
      -v, --verbose         output debug messages

# Creating a new project

## Usage

    :::text
    usage: pykwiki new [-h] project_name

    positional arguments:
      project_name  the name of the project

    optional arguments:
      -h, --help    show this help message and exit


## Example:

    :::text
    /home/hpotter/pk_projects/]$ pykwiki new spellbook
    ...
    /home/hpotter/pk_projects/]$ cd spellbook
    /home/hpotter/pk_projects/spellbook/]$

The "spellbook" project directory is where `pykwiki` commands for that project will be ran.

# Caching/Building a project

To create the *html* files from your *markdown* the project needs to be cached.

## Usage

    :::text
    usage: pykwiki cache [-h] [-p POSTS [POSTS ...]] [-f] [-q]

    optional arguments:
      -h, --help            show this help message and exit
      -p POSTS [POSTS ...], --posts POSTS [POSTS ...]
                            a list of source posts to cache, like post1.md
                            post2.md ...
      -f, --force           force cache even if file has not been modified
      -q, --quick           Skip theme files, pagelist, and search index


