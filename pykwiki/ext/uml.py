import markdown
from pykwiki.core import conf
import yaml
import jinja2
import re

UML_RE = r'^(\{uml\})(.+?)(\{enduml\})'
PLANT_UML_CONFIGS = {}

class UMLPreprocessor(markdown.preprocessors.Preprocessor):

    def __init__(self, md):
        self.config = md.plant_options

    def run(self, lines):

        try:
            import plantuml
        except:
            print("WARNING: Plantuml not installed for this python version: ext.uml disabled.")
            return lines
    
        
        text = '\n'.join(lines)
        pat = re.compile(UML_RE, re.DOTALL|re.M)
        ms = pat.findall(text)
        if not ms:
            return lines

        puml = plantuml.PlantUML(**self.config)

        for m in ms:
            uml = m[1]
            url = puml.get_url(uml)
            text = pat.sub('<img src="%s"/>'%(url), text, 1)  
 
        return text.split('\n')

class UMLExtension(markdown.Extension):

    def __init__(self, **kwargs):
        self.config = kwargs

    def extendMarkdown(self, md, md_globals):
        md.plant_options = self.config
        md.preprocessors.add('pykwiki.uml', UMLPreprocessor(md), '_begin')

def makeExtension(**configs):
    PLANT_UML_CONFIGS = configs
    return UMLExtension(**configs)

if __name__ == "__main__":
    import doctest
    doctest.testmod()
