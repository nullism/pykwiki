import markdown
from pykwiki.core import conf, Page

PAGE_RE = r'(\[\[(.*?)\]\])' 

class PagePattern(markdown.inlinepatterns.Pattern):
    def handleMatch(self, m):
        parts = m.group(3).split(':')
        page = parts[0]
        action = 'link'
        if len(parts) > 1:
            action = parts[-1]

        if not page.endswith(conf.source_ext):
            page = page + conf.source_ext

        pg = Page(page)

        if action == 'link':
            url = '%s/%s'%(conf.web_prefix, 
                page.replace(conf.source_ext, conf.target_ext))
            el = markdown.util.etree.Element("a")
            el.set('href', url)
            el.text = markdown.util.AtomicString(pg.title)
            return el

        if action == 'url':
            url = '%s/%s'%(conf.web_prefix,
                page.replace(conf.source_ext, conf.target_ext))
            return url

        if action == 'description':
            return pg.description

        if action == 'blurb':
            return pg.blurb

        if action == 'title':
            return pg.title

        return 'Invalid action: %s'%(action)

class PageExtension(markdown.Extension):

    def extendMarkdown(self, md, md_globals):
        md.inlinePatterns['pykwiki.page'] = PagePattern(PAGE_RE, md)

def makeExtension(configs=None):
    return PageExtension(configs=configs)

if __name__ == "__main__":
    import doctest
    doctest.testmod()
