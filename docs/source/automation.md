[[
title: Automation
tags: [configuration]
timestamp: 2016-01-12 22:19
]]

This page contains examples of automating Pykwiki.

# Automatic Pull and Cache

This example is useful if you have multiple or remote contributers 
committing to a project `source/` directory stored in a git repository,
and you want to automatically update the web-page.

    :::bash
    #!/bin/bash
    # Example automated Pull & Cache cron
    
    die() {
        echo "$1"
        exit 1
    }
    
    unset GIT_DIR
    project_dir="/home/hpotter/MyPykwikiProject/"
    cd $project_dir || die "Could not CD to $project_dir"
    git pull origin master ||  die "Could not git-pull"
    pykwiki cache -f || die "Could not cache files"

Then, to run that script as a cron, save it as `pykwiki-pull-cron.sh`, and add the following entry in your user's crontab. 

    :::bash
    */5 * * * * /home/hpotter/pykwiki-pull-cron.sh > /tmp/pykwiki-pull-cron.out 2>&1

# Cache, Commit, and Push

A simple script to cache source files, commit everything, and push to a git repository might be:

    :::bash
    #!/bin/bash
    project_dir="/home/hpotter/MyPykwikiProject/"
    cd $project_dir || exit 1
    pykwiki cache -f
    git add --all
    git commit -m "Updated MyPykwikiProject"
    git push origin master
    

