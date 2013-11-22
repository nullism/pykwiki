import markdown
from pykwiki.core import conf
import yaml
import jinja2
import re

TPL_RE = r'^(\{tpl:(.+?)\})(.+?)(\{endtpl\})'

def render_tpl(f, **kwargs):
    env = jinja2.Environment(loader=jinja2.FileSystemLoader(
        [conf.source_path]))
    tpl = env.get_template(f)
    return tpl.render(conf=conf, **kwargs)

class TPLPreprocessor(markdown.preprocessors.Preprocessor):
    def run(self, lines):
        text = '\n'.join(lines)
        pat = re.compile(TPL_RE, re.DOTALL|re.M)
        ms = pat.findall(text)
        if not ms:
            return lines

        for m in ms:

            tpl = m[1]
            args = m[2]

            if not tpl.endswith(conf.template_ext):
                tpl = tpl + conf.template_ext
            
            d = {}
            if args:
                d = yaml.load(args)           
            
            html = render_tpl(tpl, **d)
            text = pat.sub(html, text, 1)        
 
        return text.split('\n')

class TPLExtension(markdown.Extension):

    def extendMarkdown(self, md, md_globals):
        md.preprocessors.add('pykwiki.tpl', TPLPreprocessor(md), '_begin')

def makeExtension(configs=None):
    return TPLExtension(configs=configs)

if __name__ == "__main__":
    import doctest
    doctest.testmod()
