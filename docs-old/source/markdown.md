[[
title: Markdown Basics
tags: [authoring]
]]

# Markdown

Markdown is a popular text format for editing files. It is often used to produce well formatted web content. It is used extensively by GitHub, Reddit, Stack Overflow, and many others. 

One of the easiest ways to become familiar with Markdown is to [give it a try](https://stackedit.io)!

## Text formatting

### Bold, italics, lists

    :::text
    *This is italic*
    
    **This is bold**

    This sentence has **bold**, *italics*, and ***bold-italics***

    * This is a list item
    * So is this
        * And this is a sublist item

    Numbered lists are easy

    1. First item
    2. Second item
        1. Sub second item
    3. Third item

The above Markdown produces the following HTML

    <p><em>This is italic</em></p>

    <p><strong>This is bold</strong></p>

    <p>This sentence has <strong>bold</strong>, <em>italics</em>, and <strong><em>bold-italics</em></strong></p>

    <ul>
        <li>This is a list item</li>
        <li>So is this
            <ul><li>And this is a sublist item</li></ul>
        </li>
    </ul>

    <p>Numbered lists are easy</p>

    <ol>
        <li>First item</li>
        <li>Second item
            <ol><li>Sub second item</li></ol>
        </li>
        <li>Third item</li>
    </ol>

### Headings

If you enter the following in your Markdown (`.md`) files:

    :::text
    <h1>An HTML h1 heading</h1>

    # An h1 heading

    Also an h1 heading
    ==================

    ## An h2 heading

    Also an h2 heading
    ------------------

    ### An h3 heading

    #### An h4 heading

You would see the following HTML on your page:

    <h1>An HTML h1 heading</h1>

    <h1>An h1 heading</h1>

    <h1>Also an h1 heading</h1>

    <h2>An h2 heading</h2>

    <h2>Also an h2 heading</h2>

    <h3>An h3 heading</h3>

    <h4>An h4 heading</h4>

