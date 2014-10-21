[[
title: Release Notes
tags: [release notes]
]]

[TOC]

# v1.0.1 - 2013-11-21

First stable release. Is **not** compatible with previous versions.

* renamed "Page", "PageController" and all related methods and instances to use "post" instead of "page"
* updated themes to use new Post system.
* major changes to `pykwiki.core`
    * All instances of Page are now replaces with Post
    * Added working pagination
* updated `pykwiki.ext.page` and renamed it to `pykwiki.ext.post`

# v0.3.2 - 2013-11-12

Added pagination support.

# v0.3.1 - 2013-11-10

Fixed issue with page lists not rendering. 

Added themes to the core packages.

* Theme: Readable
* Theme: United

# v0.3 - 2013-11-05

Added several themes to the core packages.

* Theme: Amelia
* Theme: Slate
* Theme: Cyborg

# v0.2 - 2013-11-02

* Added to a git repository.
* Implemented client-side search indexing.
* Implemented tag / category system.

# v0.1 - 2013-10-15

Initial public release. 
