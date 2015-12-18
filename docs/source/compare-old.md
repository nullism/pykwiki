[[
title: Comparison to 1x
hide_author: true
]]

# Comparison to 1.x

Pykwiki 2.x offers several improvements. The most notable
of these is the single-theme concept. To customize the look
and feel of Pykwiki 1.x, a user would need to edit their themes HTML 
files. In Pykwiki 2.x, a user can simply edit the `settings.scss` file
to easily change major style components of Pykwiki. 

{tpl:table}
headers: ['', Pykwiki 1.x, Pykwiki 2.x]
rows: [
    ['Look and Feel', 'Uses full themes', 'Single theme uses scss via styles<sup>1</sup>'],
    ['Uploads', 'Uses uploads/ directory', 'Uses extension list in config to find all matching files<sup>2</sup>'],
    ['TPL Extension', 'Requires source/*.tpl', 'Can use source/*.tpl or source/tpl/*.tpl'],
    ['Nested Menus', 'One level deep', 'Up to two levels deep via sections'],    
]
{endtpl}

1. This allows Pykwiki to ensure theme html files are always up to date.
2. This allows users to specify file types by extension that will be
    uploaded to the docroot.
