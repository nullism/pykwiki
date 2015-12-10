[[
title: Getting Started
tags: [setup]
]]

[TOC]

# Getting Started

This guide outlines the minimal steps to get PyKwiki serving static files.

## Requirements

PyKwiki does not require anything outside of Python, but it does require the following Python packages:

* `jinja2` (>=2.6) - Jinja2 is used to compile themes into .html.
    * Install with `sudo pip install jinja2`
* `markdown` (>=2.3) - MarkDown is the syntax used for PyKwiki.
    * Install with `sudo pip install markdown`
* `pyyaml` (>=3.0) - Configuration files use YAML
    * Install with `sudo pip install pyyaml`

The above packages should be auto-installed when PyKwiki is installed.

## Install PyKwiki

You can download the setup.py directly, or simply run:

    $ sudo pip install pykwiki

## Create a new project

The `pykwiki new <Name>` command creates a project directory in the current
working directory. The project directory will be named `<Name>`. 

    :::bash
    $ cd ~
    $ mkdir pykwiki_projects
    $ cd pykwiki_projects
    $ pykwiki new MySite
    ...

## Serve the default content

    :::bash
    $ cd MySite/
    $ pykwiki cache -f
    ...
    $ cd docroot
    $ python -m SimpleHTTPServer 5000

Now you can navigate to [http://localhost:5000](http://localhost:5000) to see that PyKwiki is working.

## Configuration

PyKwiki is now ready for final tweaks.

* [[authoring]] - About writing and publishing posts.

Configuration:

* [[config.yaml]] - Main configuration file.
* [[links.yaml]] - Menu hierarchy configuration file.
