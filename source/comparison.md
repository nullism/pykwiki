[[
title: Feature Comparison
tags: [compare]
]]

# Compare PyKwiki, WordPress, Drupal, and MediaWiki

{tpl:table}
headers: 
    - ''
    - PyKwiki
    - WordPress
    - Drupal
    - MediaWiki
rows:
-
    - "<b>Authoring</b>"
    - "Markdown file-based"
    - "WYSIWYG"
    - "WYSIWYG"
    - "MediaWiki web editor"
-
    - "<b>Hosting</b>"
    - 'Static files'
    - "PHP and MySQL required"
    - "PHP and MySQL required"
    - "PHP and MySQL required"
-
    - "<b>Security</b>"
    - 'As secure as the web host'
    - 'Requires patching'
    - 'Requires patching'
    - 'Requires patching'
-
    - "<b>Search</b>"
    - "Simple weighted"
    - 'Simple weighted'
    - 'Weighted or natual language<sup>1</sup>'
    - 'Natural language'
-
    - "<b>Cross-post inclusion</b>"
    - 'Built-in'
    - 'No'
    - 'Available via plugins'
    - 'Built-in'
-
    - "<b>Post Templates</b>"
    - 'Built-in'
    - 'Available via plugins'
    - 'Available via plugins'
    - 'Built-in'
-
    - "<b>Revert changes</b>"
    - "Via repository, such as Git"
    - "Requires plugins"
    - "Requires plugins"
    - "Built-in"
-
    - "<b>Portable</b>"
    - "Yes, anything with Markdown"
    - "No"
    - "Not by default<sup>1</sup>"
    - "No, unless target supports MediaWiki syntax"
{endtpl}

1. Supported with additional plugins
2. Supported with protocol specific plugins, but not all protocols and methods are supported, ie: authoring from a git repository.
