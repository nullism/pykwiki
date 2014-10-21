[[
title: Remote Editing Tutorial
tags: [editing, configuration, tutorials]
]]

[TOC]

# Remote editing with Bit Torrent Sync

BitTorrent Sync is free software available from [http://www.bittorrent.com/sync](http://www.bittorrent.com/sync).

## BT Sync Server Setup

1. [Download BT Sync](http://www.bittorrent.com/sync/downloads) for your server OS.
2. Extract it somewhere

        :::bash
        $ cd /path/to/btsync
        $ tar -xvzf btsync_some_version.tar.gz

3. Run the server
    
        :::bash
        $ cd btsync_some_version/
        $ sudo ./btsync

4. Access the BT Sync web GUI: `http://<your-domain>:8888`.
5. Add a PyKwiki project folder and copy the folder key.

## BT Sync Client Setup

1. [Download](http://www.bittorrent.com/sync/downloads) and install BT Sync.
2. Follow the BT Sync instruction to create a new directory and add the folder key generated in
the [BT Sync Server Setup](#bt-sync-server-setup) step.

## Webserver setup

1. Configure your webserver to serve static files out of the BT Sync `docroot` folder. See [[webserver]] for more information.
2. Setup cron jobs to periodically cache and index the content from BT Sync `source`.

        :::bash
        # PyKwiki Caching Example Cron Jobs
        # ----------------------------------------------------------------
        # Cache just page content once per minute, very fast
        * * * * * pykwiki -b /path/to/btsync/project/folder/ cache -q
        # Cache everything (all pages and theme files) and rebuild the search index
        #   since this can take a little longer, run this every 5 minutes
        */5 * * * * pykwiki -b /path/to/btsync/project/folder/ cache -f


