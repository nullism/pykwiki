[[
title: Webserver
tags: [configuration]
]]

# Webserver Configuration

## Apache

To configure Apache to work with PyKwiki, you'll need a virtual host entry for static files that points to the PyKwiki install. 

For example, if your project directory is `/home/hpotter/pykwiki/MyBlog`, then a virtual host entry might appear as follows:

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
