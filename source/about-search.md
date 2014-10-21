[[
title: About Search
tags: [features]
]]

[TOC]

# About Search

## How it works

### 1. The search index

Existing content is cached, and a search index is built.

    $ pykwiki cache
    ...
 
The search index gets written to `conf.index_file` (default: `idx.json`). 

**Sample JSON index file format**

    :::javascript
    {
        "index":{
            "foo":[3,2,5], "bar":[3,1,6], "baz":[2],
            ...
        },
        "ids":{
            "1": "somepage.html", "2": "other-page.html", "3": "baz.html",
            ...
        }
        ...
    }

The `index` object contains a list of words as properties. Each word has a list of page ids after it. The list is sorted by the number of times that word appears in a page. In the above example, `"foo"` appears most in page id `3`, which is `baz.html`. The `"ids"` object holds the mapping of ids to pages. 

### 2. Themes load the index

Themes that support basic search (currently all of them) also use `conf.post_data_file` (default: `posts.json`) to load information about a page after filtering search results. 

**Sample JSON post data file format**

    :::javascript
    {
        "info":{
            "somepage.html": { 
                "title":"Some Page",
                "url":"/somepage.html", // Relative URL
                "mtime":123456789000, // Miliseconds since 1/1/1970
                "mtimestamp":"2010-01-01 10:10", // Page().mtimestamp
                "mdate_string":"January 01, 2010", // Page().mdate_string
                "mtime_string":"10:10", // Page().mtime_string
            },
            ...
        },        
    }


### 3. Users enter search terms

Themes specify how to compare user search terms against `conf.index_file`. In most cases, it goes like this: 

1. Split users' search terms into a list
2. Remove non alphanumeric characters
3. Compare each word in the list against the index to determine the order to display pages.


