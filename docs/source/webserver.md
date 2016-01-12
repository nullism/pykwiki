[[
title: Webserver Setup
tags: [configuration]
]]

The examples assume the path to your project's `docroot` directory is `/home/hpotter/pykwiki/MyBlog/docroot/`

# SimpleHTTPServer

    :::text
    $ cd /home/hpotter/pykwiki/MyBlog/docroot
    $ python -m SimpleHTTPServer
    Serving HTTP on 0.0.0.0 port 8000 ...

# Apache

    :::apache
    <VirtualHost *:80>
        ServerName www.myblog.com
        DocumentRoot "/home/hpotter/pykwiki/MyBlog/docroot/"
        ErrorDocument 404 /404.html
        <Directory "/home/hpotter/pykwiki/MyBlog/docroot/">
            RewriteEngine Off
            Options Indexes FollowSymLinks MultiViews
            AllowOverride None
            Order allow,deny
            allow from all
        </Directory>
    </VirtualHost>


