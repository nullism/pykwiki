[[
title: config.yaml
tags: [configuration]
]]

# config.yaml

Below is a typical `config.yaml` file

    :::yaml
    # Maximum number of words to use in a blurb
    blurb_max: 50
    # The default home page to be written as docroot/index.html
    home_page: home.md
    site:
        # The site title, used in <title>
        title: My PyKwiki Project
        # Author for use in meta name=author
        author: Example Author
        # Description for use in meta name=description
        description: "Example Site Description
            goes here"
        # Keywords for use in meta name=keywords
        keywords: "example, pykwiki"
        # (new in v1.0.5) Base URL is used by RSS feeds, no web_prefix
        base_url: http://www.example.com 
    # The style is the folder name from ./styles/
    style: default
    # Theme is now "null", but can be specified for overriding. 
    theme: null
    # Web prefix, must not end with "/"
    web_prefix: ''
    # The project's directory
    base_path: /home/HarryPotter/MyPyKwikiProject/
    # The date format used by posts
    date_format: '%B %d, %Y'
    # The time format used by posts
    time_format: '%H:%M:%S'
    # The timestamp format used by posts, this must match
    #   the format found in the post data block, if specified
    timestamp_format: '%Y-%m-%d %H:%M'
    # Post list section
    postlist:
        # How many posts to show per page
        per_page: 5
        # Maximum number of pages to render
        max_pages: 20
        # What type of post data to display (blurb, preview, full)
        post_type: preview
        # What field to order posts by (mtime, title)
        order_field: mtime
        # What direction to order posts (descending, ascending)
        order_type: descending
    # The version information
    version: 2
    # Upload extensions are file extensions that will
    # be copied from source/ to docroot/
    upload_exts:
    - .gif
    - .jpg
    - .jpeg
    - .png
    - .tiff
    - .pdf


## Parts

* `blurb_max` - specifies how many words of a post should be shown.
* `home_page` - Tells PyKwiki to look for this post in the `source` 
    directory, and if found, save it to `index.html` in the `docroot`
    directory.
* `web_prefix` - This should be an empty string if not specified.
    This is usefull for serving multiple PyKwiki projects from the same docroot directory.
* `base_path` - This is the full path to your PyKwiki Project's directory.
* `site` - Generate site settings
    * `title` - The human readable site title. Most themes will
        populate the html `<title>` attribute with this value.
    * `author` - Most themes put this value in `<meta name=author>`
    * `description` - Most themes use this value in `<meta name=description>`
    * `keywords` - This is a string of keywords that some themes use in `<meta name=keywords>`
    * `base_url` - This is the base url of your site without a trailing slash or web prefix.
* `date_format` - This describes how the date will appear when themes lookup a post's date. It uses [strftime](http://docs.python.org/2/library/time.html#time.strftime) formatting.
* `time_format` - This describes how the time will appear when themes lookup a post's time. It uses [strftime](http://docs.python.org/2/library/time.html#time.strftime) formatting.
* `timestamp_format` - This describes how the date and time will appear when themes lookup a post's timestamp.It also uses [strftime](http://docs.python.org/2/library/time.html#time.strftime) formatting. 
    * **This format must match the format in the [post data block](/authoring.html#post-data-block)**.
* `upload_exts` - This YAML list contains file extensions, including the dot (.), for file types that will be copied from source/ to docroot/.
    * For example, if you have `source/my_vacation_pics/pic21.png` and `.png` in `upload_exts` then `pic21.png` will be copied to `docroot/my_vacation_pics/pic21.png` when cached.
