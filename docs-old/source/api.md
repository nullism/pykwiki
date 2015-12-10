[[
title: API
tags: [configuration, editing]
]]

[TOC]

{tpl:versionwarning}
version: 1.0
{endtpl}

# Application Programming Interface

## conf Object

The conf object is made available to all theme templates.

### Properties

**config.yaml**

Any property in `config.yaml` is available to this object. 

**Useful properties for themes**

* `web_prefix` - When a theme makes calls to local resources, it should join the path to the resource
    with this property. `$.get('{{conf.web_prefix}}/idx.json')` for example.
* `search_tpl` - The search template. Default is "search.html". 

## ctrl Object

The `ctrl` object contains information about all PyKwiki posts on a site. It has several useful 
methods for generating lists of posts and calendars. 

### Functions

* `get_posts()`
    * `sort_key='mtime'` - The post object property to sort the returned posts by.
    * `direction='descending'` - The sort order. `descending` or `ascending`.
    * `limit=None` - The maximum number of posts to return. `0` or `None` is unlimited.
    * `filters=None` - A nested list of filters and operators. Example:
        * `[['mtime','>',1234567890], ['title','!=','Foo']]` will filter on posts that do not have the title of "Foo" *and* have a date greater than the epoch of "1234567890".
    * `private=False` - Bool that indicates whether or not the results should include posts marked as private. Default is false. 

## post Object

The post object contains all information about a specific post. It is made available to the
`post.html` template as `post`.  

### Properties

**General information**

* `title` - The post's title from the [post data block](/authoring.html#post-data-block).
* `blurb` - The blurb or description of the post. This will be auto generated on access if no blurb or description was specified in the [post data block](/authoring.html#post-data-block).
* `author` - The author of the post if specified, else returns the site's author.
* `description` - The post's description; used in `<meta name="description">`.
* `keywords` - A string of keywords; used in `<meta name="keywords">`.
* `tags` - A list of tags for the post. 
* `url` - The relative url to access the post. Includes `web_prefix` if specified.
* `source_path` - The full file system path to the source post.
* `target_path` - The full file system path to the rendered (docroot) post.

**Content**

* `source_text` - The raw markdown of the post.
* `target_text` - The rendered HTML of the post.

**Date and time**

* `mtime` - Epoch of the post's `timestamp` if specified, else it's the modified date.
* `mtime_string` - String of the post's time, formatted by `conf.time_format`.
* `mdate_string` - String of the post's date, formatted by `conf.date_format`.
* `mtimestamp` - String of the post's timestamp, formatted by `conf.timestamp_format`.
* `mtime_tuple` - A `time.localtime()` time struct.
* `mtime_hour` - The (24) hour of the post timestamp.
* `mtime_minute` - The minute of the post timestamp.
* `mdate_day` - The day of the month of the post timestamp.
* `mdate_month` - The month of the post timestamp.
* `mdate_year` - The four digit year of the post timestamp.




