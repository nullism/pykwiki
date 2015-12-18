[[
title: Webserver Setup
tags: [configuration]
]]

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


