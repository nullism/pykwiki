[[
title: Style
tags: [customization, style]
]]

[TOC]

# Style System

## Directory Structure

A style has the following directory structure by default:

    :::text
    style-name/
        info.yaml
        settings.scss
        style.scss
        static/

## info.yaml

The `info.yaml` file must contain the following information:

* `name` - The name of the style; should match directory name.
* `version` - An integer or float version representation.
* `description` - A short description of the style.
* `long_description` - A more detailed description of the style.
* `author_name` - Name of the author.
* `author_email` - The email address of the author.
* `author_website` - The website of the author or style. 

Example from the `default` style:

    name: "default"
    version: 0.9
    description: "The default sleek style for PyKwiki 2"
    long_description: A green style with a collapsing
        table of contents. Mobile friendly.
    author_name: "Aaron Meier"
    author_email: "webgovernor@gmail.com"
    author_website: http://nullism.com


## settings.scss

This file typically contains basic settings that a user can tweak. 

## style.scss

This is the meat of the style. It should implement classes found in [default classes](#default-classes). 

## static/

This directory contains any static files to be included in the theme. 

As a minimum, the root of this directory should have the following files:

* `favicon-16x16.png`
* `favicon-32x32.png`
* `favicon-96x96.png`

# Default Classes

These classes are included with most PyKwiki styles. 

## alert

The `alert alert-x` classes are used to highlight important information. 

<div class="alert alert-info">
    This is <b>.alert .alert-info</b>
</div>

<div class="alert alert-warning">
    This is <b>.alert .alert-warning</b>
</div>

<div class="alert alert-error">
    This is <b>.alert .alert-error</b>
</div>

## col-N

The `.row` and `.col-N` classes are the basis of the grid system.

Each row is **12** columns wide. The columns collapse when
the browser window is below `$small-page-width` in pixels. 

For example, the following html:

    :::html
    <div class="row">
        <div class="col col-2 color-div">
            <h2>.col .col-2</h2>
        </div>
        <div class="col col-3 color-div">
            <h2>.col .col-3</h2>
        </div>
        <div class="col col-4 color-div">
            <h2>.col .col-4</h2>
        </div>
        <div class="col col-3 color-div">
            <h2>.col .col-3</h2>
        </div>
    </div>

Produces:

<div class="row">
    <div class="col col-2 color-div">
        <h2>.col .col-2</h2>
    </div>
    <div class="col col-3 color-div">
        <h2>.col .col-3</h2>
    </div>
    <div class="col col-4 color-div">
        <h2>.col .col-4</h2>
    </div>
    <div class="col col-3 color-div">
        <h2>.col .col-3</h2>
    </div>
</div>



All columns examples:

<div class="row">
<div class="col col-2 color-div">
    <h2>.col .col-2</h2>
</div>
<div class="col col-3 color-div">
    <h2>.col .col-3</h2>
</div>
<div class="col col-4 color-div">
    <h2>.col .col-4</h2>
</div>
<div class="col col-3 color-div">
    <h2>.col .col-3</h2>
</div>
</div>

<div class="row">
<div class="col col-6 color-div">
    <h2>.col .col-6</h2>
</div>
<div class="col col-6 color-div">
    <h2>.col .col-6</h2>
</div>
</div>

<div class="row">
<div class="col col-8 color-div">
    <h2>.col .col-8</h2>
</div>
<div class="col col-4 color-div">
    <h2>.col .col-4</h2>
</div>
</div>

<div class="row">
<div class="col col-10 color-div">
    <h2>.col .col-10</h2>
</div>
<div class="col col-2 color-div">
    <h2>.col .col-2</h2>
</div>
</div>

<div class="row">
<div class="col col-12 color-div">
    <h2>.col .col-12</h2>
</div>
</div>

## color-div

Styles a div with the `$primary-color` setting.

Example:

<div class="row">
<div class="col col-12 color-div"><p>This is in a colored div</p></div>
</div>
