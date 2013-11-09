import logging
import os
import sys
import markdown
import jinja2
import re
import yaml
import json
import codecs
import shutil
import time

def render_template(f, **kwargs):
    env = jinja2.Environment(loader=jinja2.FileSystemLoader(
        [conf.theme_path, conf.default_theme_path]))
    tpl = env.get_template(f)
    return tpl.render(conf=conf, ctrl=ctrl, 
        topt=ctrl.theme_options, **kwargs)

def u_read(fname):
    fh = codecs.open(fname, encoding='utf-8')
    txt = fh.read()
    fh.close()
    return txt

def u_write(fname, data):
    fh = codecs.open(fname, encoding='utf-8', mode='w')
    fh.write(data)
    fh.close()

class Config(object):

    web_prefix = ''
    base_path = None
    source_dir = 'source'
    upload_dir = 'uploads'
    target_dir = 'docroot'
    link_file = 'links.yaml'
    theme_dir = 'themes'
    theme = 'default'
    logger = None
    site = {
        'title':'Example Site',
        'description':'Example Site Description',
        'author':'Example Author',
        'keywords':'example, pykwiki'
    }
    page_tpl = 'page.html'
    pages_tpl = 'pages.html'
    menu_tpl = 'menu.html'
    source_ext = '.md'
    target_ext = '.html'
    template_ext = '.tpl'
    index_file = 'idx.json'
    stop_words = ['the','and']
    markdown_exts = [
        'codehilite','toc',
        'pykwiki.ext.tpl',
        'pykwiki.ext.page',
    ]
    page_conf_re = re.compile('\[\[(.*?)\]\]', re.DOTALL)
    blurb_max = 50
    home_page = 'index.md'

    config_text_properties = [
        'web_prefix',
        'home_page',
        'theme',
        'blurb_max',
        'site',
        'base_path',
        'markdown_exts',
    ]

    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.DEBUG)
        if not self.logger.handlers:
            self.logger.addHandler(logging.StreamHandler())

    def __repr__(self):
        return '<Config() base: %s; source: %s; target: %s;>'\
            %(self.base_path, self.source_dir, self.target_dir)

    def check(self):

        if not self.base_path:
            raise Exception('conf.base_path not set!')

        if not os.path.exists(self.base_path): 
            raise Exception('Base path %s does not exist!'%(self.base_path))

        if not self.source_dir:
            raise Exception('conf.source_dir not set!')
    
        if not self.target_dir:
            raise Exception('conf.target_dir not set!')

        if not self.logger or not isinstance(self.logger, logging.Logger):
            raise Exception('conf.logger is invalid!')

        if self.web_prefix.endswith('/'):
            raise Exception('conf.web_prefix cannot end with "/"')

    @property
    def default_theme_path(self):
        return os.path.join(self.base_path, self.theme_dir, 'default')

    @property
    def theme_path(self):
        return os.path.join(self.base_path, self.theme_dir, self.theme)

    @property
    def source_path(self):
        return os.path.join(self.base_path, self.source_dir)

    @property
    def upload_path(self):
        return os.path.join(self.source_path, self.upload_dir)

    @property
    def target_path(self):
        return os.path.join(self.base_path, self.target_dir)

    def save(self, cname='config.yaml'):
        ''' Write the config to base_path.yaml '''
        self.logger.info('Saving configuration to: %s'%(cname))
        self.check()
        export = {}
        for k in self.config_text_properties:
            export[k] = getattr(self, k)
        fh = open(os.path.join(self.base_path, cname), 'w')
        yml = yaml.dump(export, default_flow_style=False)
        fh.write(yml)
        fh.close()
        
    def load(self, cpath):
        self.logger.info('Reading configuration from %s'%(cpath))
        if not os.path.exists(cpath):
            raise Exception('Config file: %s not found!'%(cpath))
        
        fh = open(cpath, 'r')
        txt = fh.read()
        fh.close()
        data = yaml.load(txt)
        for k in data:
            if k in self.config_text_properties:
                setattr(self, k, data[k])
        self.check()
        
 

class PageController(object):
     
    _pages = []
    _theme_menu = None
    _theme_options = None
    index_data = {}

    def __init__(self):
        pass
 
    def cache_pages(self, plist=None, force=False):
        if not plist:
            plist = self.get_all_pages()

        for pf in plist:
            pg = Page(pf)
            if not force:
                if pg.source_mtime <= pg.target_mtime:
                    continue
            pg.save()

    def cache_theme(self):
        ''' Cache specific theme files '''

        conf.logger.info('Caching theme files')

        # Page Listing / Search
        html = render_template(conf.pages_tpl)
        out = os.path.join(conf.target_path, conf.pages_tpl)
        u_write(out, html)

        # Home page
        home_page = os.path.join(conf.source_path, conf.home_page)
        if os.path.exists(home_page):
            conf.logger.info('Writing %s as home page (index.html)'%(home_page))
            pg = Page(conf.home_page)
            html = render_template(conf.page_tpl, page=pg)
            out = os.path.join(conf.target_path, 'index.html')
            u_write(out, html)

        # Static files
        stat_src = os.path.join(conf.theme_path, 'static/')
        stat_dest = os.path.join(conf.target_path, 'static/')
        if os.path.exists(stat_src):
            if os.path.exists(stat_dest):
                shutil.rmtree(stat_dest)
            shutil.copytree(stat_src, stat_dest)

    @property
    def theme_options(self):
        if self._theme_options:
            return self._theme_options
        opt_path = os.path.join(conf.theme_path, 'options.yaml')
        if os.path.exists(opt_path):
            data = u_read(opt_path)
            self._theme_options = yaml.load(data)
            return self._theme_options

        return {}

    @property                
    def theme_menu(self):
        if self._theme_menu:
            return self._theme_menu

        link_path = os.path.join(conf.base_path, conf.link_file)
        if not os.path.exists(link_path):
            return 'Unable to locate %s'%(link_path)
        
        def get_clean_links(dlist):
            ll = []
            for d in dlist:
                key = d.keys()[0]
                new_d = d[key]
                new_d['label'] = key
                if new_d.get('page'):
                    new_d['href'] = conf.web_prefix + '/' +\
                        new_d['page'].replace(conf.source_ext, conf.target_ext)
                    new_d['rel'] = 'internal'
                else:
                    new_d['rel'] = 'external'

                if new_d.get('children'):
                    new_d['children'] = get_clean_links(new_d['children'])
                ll.append(new_d)
            return ll
            
        ltxt = u_read(link_path)
        links = yaml.load(ltxt)
        menu_links = get_clean_links(links)
        self._theme_menu = render_template(conf.menu_tpl, links=menu_links)
        
        return self._theme_menu


    def index_pages(self, plist=None, search_index=True):
    
        if not plist:
            plist = self.get_all_pages()

        if self.index_data:
            return

        conf.logger.info('Indexing pages: %s'%(plist))

        data = {}
        tags = {}
        ids = {}
        info = {}
        this_id = 1
        for pf in plist:
            pg = Page(pf)
            if pg.conf.get('private'):
                continue
            ids[this_id] = pg.target_fname
            info[pg.target_fname] = dict(
                title=pg.conf.get('title'),
                blurb=pg.blurb,
                mepoch=int(pg.mtime)
            )

            # Tags
            for tag in pg.conf.get('tags',[]):
                if tags.has_key(tag):
                    if this_id in tags[tag]:
                        continue
                    tags[tag].append(this_id)
                else:
                    tags[tag] = [this_id]

            # Search Index
            if search_index:
                s_text = '%s %s'%(pg.conf.get('title',''), pg.source_text)
                s_text = s_text.replace("'",'').lower()
                s_text = re.sub('[^a-z0-9\-\ ]', ' ', s_text)
                for word in s_text.split():
                    if len(word) < 3:
                        continue
                    if word in conf.stop_words:
                        continue
                    if data.has_key(word):
                        if data[word].has_key(this_id):
                            data[word][this_id] += 1
                        else:
                            data[word][this_id] = 1
                    else:
                        data[word] = {this_id: 1}

            this_id += 1

        for k in data:
            data[k] = sorted(data[k], key=data[k].get, reverse=True)

        self.index_data = {
            'ids':ids, 
            'index':data, 
            'info':info, 
            'tags':tags,
            'updated':int(time.time()),
        }

        index_path = os.path.join(conf.target_path, conf.index_file)
        conf.logger.info('Writing search index to %s'%(index_path))
        fh = open(index_path, 'w')
        json.dump(self.index_data, fh)
        fh.close()
        

    def get_all_pages(self):

        if self._pages:
            return self._pages

        for root, dirs, files in os.walk(conf.source_path):
            for f in files:
                if not f.endswith(conf.source_ext):
                    continue
                fullpath = os.path.join(root, f)
                fname = fullpath.replace(conf.source_path+'/', '')
                self._pages.append(fname)

        return self._pages

class Page(object):
    ''' Page object (str:source_fname)
        loads, saves, and caches pages '''    

    source_fname = None
    source_path = None
    target_fname = None
    target_path = None
    _source_text = None
    _target_text = None
    _conf = {}
    _author = None
    _tags = []
    _blurb = None
    _description = None
    _keywords = None
    _title = None
    _mtime = None

    def __init__(self, source_fname):
        conf.check()
        self.source_fname = source_fname

    def save(self):

        full_dir = os.path.split(self.target_path)[0]
    
        if not os.path.exists(full_dir):
            try:
                conf.logger.info('Making directory: %s'%(full_dir))
                os.makedirs(full_dir)
            except(Exception),e:
                raise Exception('Cannot create directory: %s'%(full_dir))


        pc = self.conf
        tt = self.target_text
        conf.logger.info('Saving to: %s'%(self.target_path))        
        html = render_template(conf.page_tpl, page=self)        
        u_write(self.target_path, html)


    @property
    def author(self):
        if self._author:
            return self._author
        if self.conf.get('author'):
            self._author = self.conf['author']
            return self._author
        self._author = conf.site_author
        return self._author

    @property
    def conf(self):

        if self._conf:
            return self._conf

        m = conf.page_conf_re.search(self.source_text)
        if not m:
            conf.logger.warning('No page config specified') 
            return
        
        try:
            self._conf = yaml.load(m.group(1))
            self._source_text = self.source_text.replace(m.group(0), '')
        except(Exception),e:
            conf.logger.exception('Invalid page configuration found!')
        
        return self._conf

    @property
    def source_path(self):
        return os.path.join(conf.source_path, self.source_fname)

    @property
    def target_path(self):
        return os.path.join(conf.target_path, self.target_fname)

    @property
    def target_fname(self):
        return self.source_fname.replace(
            conf.source_ext, conf.target_ext)

    @property
    def source_text(self):
        if self._source_text:
            return self._source_text

        if not os.path.exists(self.source_path):
            raise Exception('Cannot locate file: %s'%(self.source_path))
            
        self._source_text = u_read(self.source_path)
        return self._source_text
   
    @property
    def tags(self):
        if self._tags:
            return self._tags
        self._tags = self.conf.get('tags',[])
        return self._tags

    @property
    def title(self):
        if self._title:
            return self._title
        if self.conf.get('title'):
            self._title = self.conf['title']
            return self._title
        self._title = self.target_fname.replace(conf.target_ext, '')
        return self._title

    @property
    def target_text(self):
        if self._target_text:
            return self._target_text
        conf.logger.info('Caching: %s'%(self.source_fname))
        html = markdown.markdown(self.source_text, 
            extensions=conf.markdown_exts)
        self._target_text = html   
        return self._target_text

    @property
    def mtime(self):
        if self._mtime:
            return self._mtime
        self._mtime = self.source_mtime
        return self._mtime

    @property
    def target_mtime(self):
        return os.path.getmtime(self.target_path)

    @property
    def source_mtime(self):
        return os.path.getmtime(self.source_path)
 
    @property
    def blurb(self):
        if self._blurb:
            return self._blurb
        elif self.conf.get('blurb'):
            if self.conf['blurb'].lower() != 'auto':
                self._blurb = self.conf['blurb']
                return self._blurb
        elif self.conf.get('description'):
            self._blurb = self.conf['description']
            return self._blurb

        words = self.source_text.split()
        blurb = ' '.join(words[0:conf.blurb_max]) + '...'
        # @todo clean to blurb to remove HTML and MarkDown stuff
        blurb = re.sub(r'[<#>]','', blurb)

        self._blurb = blurb
        return self._blurb

    @property 
    def keywords(self):
        if self._keywords:
            return self._keywords
        if self.conf.get('keywords'):
            self._keywords = self.conf['keywords']
            return self._keywords
        if self.conf.get('tags'):
            self._keywords = ','.join(self.conf['tags'])
            return self._keywords
        if conf.site.get('keywords'):
            self._keywords = conf.site['keywords']
            return self._keywords
        return ''

    @property
    def description(self):
        if self._description:
            return self._description
        if self.conf.get('description'):
            self._description = self.conf['description']
            return self._description
        if conf.site.get('description'):
            self._description = conf.site['description']
            return self._description
        return ''

conf = Config()
ctrl = PageController()
