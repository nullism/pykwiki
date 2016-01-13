[[
title: Automation
tags: [configuration]
timestamp: 2016-01-12 22:19
]]

This page contains examples of automating Pykwiki.


# Cache, Commit, and Push

A simple script to cache source files, commit everything, and push to a git repository might be:

    :::bash
    project_dir="/home/hpotter/MyPykwikiProject/"
    cd $project_dir || exit 1
    pykwiki cache -f
    git add --all
    git commit -m "Updated MyPykwikiProject"
    git push origin master
    

