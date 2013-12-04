import markdown
from pykwiki.core import conf, Post

POST_RE = r'(\[\[([a-zA-Z0-9]+.*?)\]\])' 
SEC_START_RE = r'(\{section:(.*?)\})'
SEC_END_RE = r'(\{endsection\})'

class SectionStartPattern(markdown.inlinepatterns.Pattern):
    """ Clean {section:} start tag """
    def handleMatch(self, m):
        return ''

class SectionEndPattern(markdown.inlinepatterns.Pattern):
    """ Clean {endsection} tag """
    def handleMatch(self, m):
        return ''

class PostPattern(markdown.inlinepatterns.Pattern):
    def handleMatch(self, m):
        parts = m.group(3).split(':')
        post = parts[0]
        action = 'link'
        extra = None
        if len(parts) > 1:
            action = parts[1]
            if len(parts) > 2:
                extra = parts[2]

        if not post.endswith(conf.source_ext):
            post = post + conf.source_ext

        pg = Post(post)

        # For [[page:link]]
        if action == 'link':
            url = '%s/%s'%(conf.web_prefix, 
                post.replace(conf.source_ext, conf.target_ext))
            el = markdown.util.etree.Element("a")
            el.set('href', url)
            el.text = markdown.util.AtomicString(pg.title)
            return el

        # For [[page:url]]
        if action == 'url':
            url = '%s/%s'%(conf.web_prefix,
                post.replace(conf.source_ext, conf.target_ext))
            return url

        # For [[page:description]]
        if action == 'description':
            return pg.description

        # For [[page:blurb]]
        if action == 'blurb':
            return pg.blurb
        
        # For [[page:title]]
        if action == 'title':
            return pg.title

        # For [[page:section:section_name]]
        if action == 'section':
            if not extra:
                return 'No section name given'
            sec = pg.get_section(extra, raw=False) 
            if not sec:
                return 'Cannot find section: %s'%(extra)
            el = markdown.util.etree.Element("div")
            markdown.Markdown().parser.parseChunk(el, sec)
            #print "="*80, "\n", sec, "\n", "="*80
            return el

        return 'Invalid action: %s'%(action)

class PostExtension(markdown.Extension):

    def extendMarkdown(self, md, md_globals):
        md.inlinePatterns['pykwiki.post'] = PostPattern(POST_RE, md)
        md.inlinePatterns['pykwiki.post.section_start'] = SectionStartPattern(SEC_START_RE, md)
        md.inlinePatterns['pykwiki.post.section_end'] = SectionEndPattern(SEC_END_RE, md)

def makeExtension(configs=None):
    return PostExtension(configs=configs)

if __name__ == "__main__":
    import doctest
    doctest.testmod()
