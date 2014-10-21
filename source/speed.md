[[
title: Speed
tags: [configuration, features]
]]

# Faster than PHP

PyKwiki is fast because it's 100% static. No server side processing is necessary. Why regenerate a page every single time someone visits it? PyKwiki regenerates the page only when its content has changed. 

*But wait! How can that be if you have built-in searching?* PyKwiki generates a JSON index file for page searches, so unlike most other static content systems, you don't need to rely on a third party to perform searches. 
 
## Optimizing PyKwiki

In most cases, PyKwiki won't require any optimization. However, if a PyKwiki site happens to receive hundreds of thousands of views per day, then there are a few different techniques to help remove this load.

1. Use Nginx or Apache Workers MPM. 
    * This alone can greatly increase page performance.
2. Cache content.
    * Tell your webserver to cache content in the user's browser for a few hours. They won't see updates when they're released, but this can dramatically reduce server load.
3. Use a CDN.
    * Use something like [Cloud Flare](http://cloudflare.com) to cache your content on a CDN. This can be the most expensive option, but it works well.


