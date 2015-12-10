[[
title: Code-Hilite Examples
tags: [examples]
]]

[TOC]

PyKwiki uses the Markdown module's [codehilite](http://pythonhosted.org//Markdown/extensions/code_hilite.html) extension by default.

This extension is powered by [Pygments](http://pygments.org) and supports a [wide variety of languages](http://pygments.org/languages/).

# No hilighting (text)

    :::text
    Unhilighted:

        :::text
        No "syntax" highlighting here...

**Produces:**

Unhilighted:

    :::text
    No "syntax" highlighting here...


# Python

    :::text
    Sample *Python*:

        :::python
        def foo():
            print("Bar")
            return False

**Produces:**

Sample *Python*:

    :::python
    def foo():
        print("Bar")
        return False

    

# INI Configuration files.

    :::text
    Contents of `myconfig.ini`:

        :::ini
        ; Database connection info
        server = localhost
        password = "ASDFG123456"
        db_server = mydb.localhost

**Produces:**

Contents of `myconfig.ini`:

    :::ini
    ; Database connection info
    server = localhost
    password = "ASDFG123456"
    db_server = mydb.localhost

