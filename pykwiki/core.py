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
import math
import scss

def set_jinja_filters(env):
    """ Used to add custom Jinja2 filters to the env """
    import pykwiki.jinja_filters as jinja_filters
    env.filters['idsafe'] = jinja_filters.idsafe
    return env

def render_theme_template(f, **kwargs):
    """ Renders a theme template using a cascading FilySystemLoader

    All theme templates include sopt, topt, ctrl, and conf
    """
    env = jinja2.Environment(loader=jinja2.FileSystemLoader(
        [conf.theme_path, conf.default_theme_path]))
    env = set_jinja_filters(env)
    tpl = env.get_template(f)
    return tpl.render(conf=conf, ctrl=ctrl,
        topt=ctrl.theme_options, sopt=ctrl.social_options,
        **kwargs)

def render_text(text, **kwargs):
    """ Jinja-fies plain text """
    env = set_jinja_filters(jinja2.Environment())
    tpl = env.from_string(text)
    return tpl.render(**kwargs)

def u_read(fname):
    """ Unicode read

    @param fname [str] - full path to the file to read
    """
    fh = codecs.open(fname, encoding='utf-8')
    txt = fh.read()
    fh.close()
    return txt

def u_write(fname, data):
    """ Unicode write

    @param fname [str] - full path to the file to write to
    @param data [str] - data to write to fname
    """
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
    style_file = 'style.scss'
    link_json_file = 'links.json'
    theme_dir = 'themes'
    style_dir = 'styles'
    theme = None
    style = 'default'
    logger = None
    site = {
        'title':'Example Site',
        'description':'Example Site Description',
        'author':'Example Author',
        'keywords':'example, pykwiki',
        'base_url':''
    }
    postlist = {
        'per_page':2,
        'post_type':'preview', #blurb, full, preview
        'max_pages':5,
        'order_field':'mtime',
        'order_type':'descending',
    }
    post_tpl = 'post.html'
    docroot_index = 'index.html'
    search_tpl = 'search.html'
    postlist_tpl = 'postlist.html'
    posts_tpl = 'posts.html'
    e404_tpl = '404.html'
    menu_tpl = 'menu.html'
    rss_tpl = 'rss.xml'
    rss_max_entries = 20
    source_ext = '.md'
    target_ext = '.html'
    template_ext = '.tpl'
    time_format = '%H:%M:%S'
    timestamp_format = '%Y-%m-%d %H:%M'
    date_format = '%Y-%m-%d'
    index_file = 'idx.json'
    post_data_file = 'posts.json'
    stop_words = ['the','and']
    upload_exts = ['.gif','.jpg','.jpeg','.png','.tiff','.pdf']
    markdown_exts = [
        'codehilite','toc',
        'pykwiki.ext.tpl',
        'pykwiki.ext.post',
    ]
    # The regex to grab post data blocks
    post_conf_re = re.compile('^\[\[(.*?)\]\]', re.DOTALL)
    post_conf_re2 = re.compile('^---(.*?)\\n---', re.DOTALL)
    post_toc_re = re.compile('^\s{0,3}\[TOC\]', re.MULTILINE)
    blurb_max = 50
    home_page = 'index'
    version = None

    # These properties will be written to/read from
    # the config.yaml file.
    config_text_properties = [
        'web_prefix',
        'home_page',
        'theme',
        'blurb_max',
        'site',
        'base_path',
        'markdown_exts',
        'time_format',
        'date_format',
        'timestamp_format',
        'source_ext',
        'postlist',
        'rss_max_entries',
        'style',
        'upload_exts',
        'version',
        'target_dir',
        'source_dir'
    ]

    def __init__(self):
        if not self.logger:
            self.logger = logging.getLogger("pykwiki")
        if not self.logger.handlers:
            self.logger.addHandler(logging.StreamHandler())

    def __repr__(self):
        return '<Config() base: %s; source: %s; target: %s;>'\
            %(self.base_path, self.source_dir, self.target_dir)

    def check(self):
        """ Verify that the current configuration isn't broken """
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

        if not self.version:
            raise Exception('conf.version does not exist')

        if self.version < 2 or self.version >= 3:
            raise Exception('conf.version is incorrect')

    @property
    def default_theme_path(self):
        self_dir = os.path.split(os.path.abspath(__file__))[0]
        return os.path.join(self_dir, 'data', 'default_theme')

    @property
    def link_path(self):
        return os.path.join(self.base_path, self.link_file)

    @property
    def link_json_path(self):
        return os.path.join(self.target_path, self.link_json_file)

    @property
    def theme_path(self):
        if self.theme:
            return os.path.join(self.base_path, self.theme_dir, self.theme.lower())
        return self.default_theme_path

    @property
    def style_head(self):
        hd_path = os.path.join(self.style_path, 'head.html')
        if os.path.exists(hd_path):
            with open(hd_path, 'r') as fh:
                return fh.read()
        return "<!-- no style head.html found -->"

    @property
    def style_post(self):
        path = os.path.join(self.style_path, 'post.html')
        if os.path.exists(path):
            with open(path, 'r') as fh:
                return fh.read()
        return "<!-- no style post.html found -->"

    @property
    def style_footer(self):
        ft_path = os.path.join(self.style_path, 'footer.html')
        if os.path.exists(ft_path):
            with open(ft_path, 'r') as fh:
                return fh.read()
        return "<!-- no style footer.html found -->"

    @property
    def style_path(self):
        return os.path.join(self.base_path, self.style_dir, self.style.lower())

    @property
    def style_web_path(self):
        return self.web_prefix + "/" + os.path.join('static', self.style.lower())

    @property
    def style_file_path(self):
        return os.path.join(self.style_path, self.style_file)

    @property
    def source_path(self):
        return os.path.join(self.base_path, self.source_dir)

    @property
    def target_path(self):
        return os.path.join(self.base_path, self.target_dir)

    def save(self, cname='config.yaml'):
        """ Write the config to base_path.yaml

        @param cname [str] - The name of the config file
        """
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
        """ Load the config file into the object

        @param cpath [str] - The full path to the config to read
        """
        self.logger.debug('Reading configuration from %s...'%(cpath))
        if not os.path.exists(cpath):
            raise Exception('Config file: %s not found!'%(cpath))

        fh = open(cpath, 'r')
        txt = fh.read()
        fh.close()
        data = yaml.load(txt)
        for k in data:
            if k in self.config_text_properties:
                setattr(self, k, data[k])
        #self.check()



class PostController(object):

    _posts = []
    _source_files = []
    _theme_menu = None
    _theme_options = None
    _social_options = None
    _post_info = None
    index_data = {}

    def __init__(self):
        pass

    def cache_posts(self, plist=None, force=False):
        """ Cache posts and return the number of changes

        @param plist [list] - A list of source filenames to cache
        @param force [bool] - Cache regardless of file mtimes
        @returns [int] - Number of files changed
        """

        cached = 0;
        if not plist:
            plist = self.source_files

        for pf in plist:
            pg = Post(pf)
            if not force:
                if pg.source_mtime <= pg.target_mtime:
                    continue
            cached += 1
            pg.save()

        return cached

    def cache_uploads(self):
        """ Find file differences (mtime) and copy them to docroot

        @returns [bool] - True if successful, false otherwise
        """


        conf.logger.info('Caching uploads')
        cnt = 0
        for root, dirs, files in os.walk(conf.source_path):
            for f in files:
                fnoe, ext = os.path.splitext(f)
                if ext not in conf.upload_exts:
                    continue
                src_path = os.path.join(root, f)
                tgt_path = src_path.replace(conf.source_path, conf.target_path)
                if os.path.exists(tgt_path):
                    src_mt = os.path.getmtime(src_path)
                    tgt_mt = os.path.getmtime(tgt_path)
                    if src_mt < tgt_mt:
                        continue
                tgt_dir, tgt_fname = os.path.split(tgt_path)
                if not os.path.exists(tgt_dir):
                    os.makedirs(tgt_dir)
                conf.logger.debug('Copying %s to %s'%(src_path, tgt_path))
                shutil.copy(src_path, tgt_path)
                cnt += 1

        conf.logger.info('Copied %s new uploads'%(cnt))
        return True


    def cache_postlist(self):

        order_field = conf.postlist['order_field']
        order_type = conf.postlist['order_type']
        max_pages = conf.postlist['max_pages']
        per_page = conf.postlist['per_page']
        post_type = conf.postlist['post_type']

        posts = self.get_posts(sort_key=order_field, private=False,
            direction=order_type, filters=None, limit=(max_pages*per_page))

        post_count = len(posts)
        if post_count > max_pages * per_page:
            post_count = max_pages * per_page
        page_count = int(math.ceil(float(post_count) / float(per_page)))

        for page_num in range(1, max_pages+1):
            if len(posts) < 1:
                break
            this_posts = []
            for i in range(per_page):
                if len(posts) < 1:
                    break
                this_posts.append(posts.pop(0))

            html = render_theme_template(conf.postlist_tpl,
                this_page_num=page_num, posts=this_posts,
                page_count=page_count, post_count=post_count,
                post_type=post_type, per_page=per_page)
            out = os.path.join(conf.target_path, 'postlist-%s.html'%(page_num))
            u_write(out, html)

        html = render_theme_template(conf.posts_tpl,
            post_count=post_count, page_count=page_count,
            post_type=post_type, per_page=per_page)
        out = os.path.join(conf.target_path, conf.posts_tpl)
        u_write(out, html)


    def cache_theme(self):
        """ Cache specific theme files """

        conf.logger.info("Caching theme files")
        conf.logger.debug('Using theme files from %s'%(conf.theme_path))

        # Post 404
        html = render_theme_template(conf.e404_tpl)
        out = os.path.join(conf.target_path, conf.e404_tpl)
        u_write(out, html)

        # Post Search
        html = render_theme_template(conf.search_tpl)
        out = os.path.join(conf.target_path, conf.search_tpl)
        u_write(out, html)

        # Post Listing
        self.cache_postlist()

        # Home post
        home_page = conf.home_page
        if home_page in [conf.posts_tpl, conf.search_tpl]:
            html = render_theme_template(home_page)
            out = os.path.join(conf.target_path, conf.docroot_index)
            u_write(out, html)
        else:
            if not home_page.endswith(conf.source_ext):
                home_page = home_page + conf.source_ext
            home_page_path = os.path.join(conf.source_path, home_page)
            if os.path.exists(home_page_path):
                conf.logger.info('Writing %s as home post (%s)'\
                    %(home_page, conf.docroot_index))
                pg = Post(home_page)
                html = render_theme_template(conf.post_tpl, post=pg)
                out = os.path.join(conf.target_path, conf.docroot_index)
                u_write(out, html)

        # Static files
        stat_src = os.path.join(conf.theme_path, 'static/')
        stat_dest = os.path.join(conf.target_path, 'static/')
        style_src = os.path.join(conf.style_path, 'static')
        style_dest = os.path.join(conf.target_path, 'static', 'style')
        if os.path.exists(stat_src):
            if os.path.exists(stat_dest):
                shutil.rmtree(stat_dest)
            shutil.copytree(stat_src, stat_dest)
            if os.path.exists(style_src):
                shutil.copytree(style_src, style_dest)

        # In case source doesn't have a static/ directory
        if not os.path.exists(style_dest):
            os.makedirs(style_dest)

        # Cache scss
        conf.logger.debug("Compiling scss to static/styles/style.css")
        style_data = scss.Compiler().compile(conf.style_file_path)
        with open(os.path.join(style_dest, 'style.css'), 'w') as fh:
            fh.write(style_data)


    def cache_rss_feed(self):

        """ Builds an RSS feed for the posts """

        conf.logger.info('Caching RSS feed')
        rss_tpl = os.path.join(conf.theme_path, conf.rss_tpl)
        if not os.path.exists(rss_tpl):
            conf.logger.warning('No rss template found in theme')
            return False

        posts = self.get_posts(limit=conf.rss_max_entries)
        xml = render_theme_template(conf.rss_tpl, posts=posts)
        outf = os.path.join(conf.target_path, conf.rss_tpl)
        u_write(outf, xml)


    @property
    def social_options(self):
        if self._social_options:
            return self._social_options
        opt_path = os.path.join(conf.base_path, 'social.yaml')
        if os.path.exists(opt_path):
            data = u_read(opt_path)
            self._social_options = yaml.load(data)
            return self._social_options
        return {}


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

        if os.path.exists(conf.link_json_path):
            if os.path.getmtime(conf.link_path) \
                    <= os.path.getmtime(conf.link_json_path):
                js = u_read(conf.link_json_path)
                links = json.loads(js)
                self._theme_menu = render_theme_template(conf.menu_tpl,
                    links=links)
                return self._theme_menu

        conf.logger.info('Generating theme menu from %s'%(conf.link_file))
        link_path = conf.link_path
        if not os.path.exists(link_path):
            return 'Unable to locate %s'%(link_path)

        def get_clean_links(dlist):
            ll = []
            for d in dlist:
                if not isinstance(d, dict):
                    ll.append({'label':d})
                    continue
                key = list(d.keys())[0]
                new_d = d[key]
                new_d['label'] = key
                new_d['rel'] = 'internal'
                if new_d.get('post'):
                    if not new_d['post'].endswith(conf.source_ext):
                        new_d['post'] = new_d['post'] + conf.source_ext
                    new_d['href'] = conf.web_prefix + '/' +\
                        new_d['post'].replace(conf.source_ext, conf.target_ext)
                else:
                    if new_d.get('href') and '://' in new_d['href']:
                        new_d['rel'] = 'external'

                if new_d.get('children'):
                    new_d['children'] = get_clean_links(new_d['children'])
                ll.append(new_d)
            return ll

        ltxt = u_read(link_path)
        links = yaml.load(ltxt)
        menu_links = get_clean_links(links)
        self._theme_menu = render_theme_template(conf.menu_tpl, links=menu_links)
        u_write(conf.link_json_path, json.dumps(menu_links))
        return self._theme_menu

    @property
    def post_info(self, plist=None):

        if self._post_info:
            return self._post_info

        if not plist:
            plist = self.source_files



    def index_posts(self, plist=None, search_index=True):
        """ Build a search index and post data JSON file

        @param plist [list] - A list of source file names
        @search_index [bool] - Whether or not to build a search index
        """
        if not plist:
            plist = self.source_files

        if self.index_data:
            return

        conf.logger.info("Building search index")
        conf.logger.debug('Indexing posts: %s'%(plist))

        data = {}
        tags = {}
        ids = {}
        info = {}
        this_id = 1
        for pf in plist:
            pg = Post(pf)
            if pg.conf.get('private'):
                continue
            ids[this_id] = pg.target_fname
            info[pg.target_fname] = dict(
                title=pg.title,
                blurb=pg.blurb,
                url=pg.url,
                mtime=int(pg.mtime),
                mtimestamp=pg.mtimestamp,
                mtime_string=pg.mtime_string,
                mdate_string=pg.mdate_string,
                author=pg.author,
            )

            # Tags
            for tag in pg.conf.get('tags',[]):
                if tag in tags:
                    if this_id in tags[tag]:
                        continue
                    tags[tag].append(this_id)
                else:
                    tags[tag] = [this_id]

            # Search Index
            if search_index:
                s_text = '%s %s'%((pg.conf.get('title','')+' ')*10, pg.source_text)
                s_text = s_text.replace("'",'').lower()
                s_text = re.sub('[^a-z0-9\-\ ]', ' ', s_text)
                for word in s_text.split():
                    if len(word) < 3:
                        continue
                    if word in conf.stop_words:
                        continue
                    if word in data:
                        if this_id in data[word]:
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
            'tags':tags,
            'updated':int(time.time()),
        }

        post_info = {
            'info':info,
            'ids':ids,
        }

        post_info_path = os.path.join(conf.target_path, conf.post_data_file)
        conf.logger.debug('Writing post info to %s'%(post_info_path))
        u_write(post_info_path, json.dumps(post_info))

        index_path = os.path.join(conf.target_path, conf.index_file)
        conf.logger.debug('Writing search index to %s'%(index_path))
        u_write(index_path, json.dumps(self.index_data))


    def get_posts(self, sort_key='mtime', private=False, direction='desc',
            filters=None, limit=0):
        """ Get a sorted and filtered list of posts

        @param sort_key [str] - The post property to sort on, default: mtime
        @param private [bool] - Include private posts if true
        @param direction [str] - Either ascending or descending
        @param filters [list] - A multi-dimensional list of filters like
            [ ['field', 'op', 'value'], ['mtime', '>', '1234567890']]
        @param limit [int] - Maximum number of posts to return
        """
        direction = direction.lower()
        rev = False
        if direction == 'desc' or direction == 'descending':
            rev = True

        # Set the limit to something crazy, like 10K
        if not limit:
            limit = 10000

        plist = self.posts
        if not private:
            plist = [p for p in plist if not p.conf.get('private')]

        if filters:
            for f in filters:
                try:
                    k, o, v = f
                except:
                    raise Exception('Invalid filter found: %s'%(f))

                if o == '==':
                    plist = [p for p in plist if getattr(p, k) == v]
                elif o == '>':
                    plist = [p for p in plist if getattr(p, k) > v]
                elif o == '>=':
                    plist = [p for p in plist if getattr(p, k) >= v]
                elif o == '<':
                    plist = [p for p in plist if getattr(p, k) < v]
                elif o == '<=':
                    plist = [p for p in plist if getattr(p, k) <= v]
                elif o == '!=':
                    plist = [p for p in plist if getattr(p, k) != v]
                else:
                    raise Exception('Invalid filter operator found: %s'%(o))

        if sort_key:
            plist.sort(key=lambda x: getattr(x, sort_key), reverse=rev)

        if len(plist) > limit:
            plist = plist[0:limit]

        return plist

    def get_post_dates(self, private=False, direction='desc', limit=0):
        """ Return a list of post dates in mdate_string format

        @param private [bool] - Include private posts if True
        @param direction [str] - Either ascending or descending
        @param limit [int] - Maximum number of post dates to return
        """
        direction = direction.lower()
        rev = False
        if direction == 'desc' or direction == 'descending':
            rev = True

        if not limit:
            limit = 10000

        plist = self.posts

        if not private:
            plist = [p for p in plist if not p.conf.get('private')]

        plist.sort(key=lambda x: x.mtime, reverse=rev)
        dlist = []
        for p in plist:
            if p.mdate_string not in dlist and len(dlist) < limit:
                dlist.append(p.mdate_string)
        return dlist

    @property
    def post_dates(self):
        return self.get_post_dates(direction='desc')

    @property
    def posts(self):
        if self._posts:
            return self._posts
        plist = self.source_files
        posts = []
        for pf in plist:
            posts.append(Post(pf))
        self._posts = posts
        return self._posts

    @property
    def tags(self):
        tags = []
        for p in self.posts:
            for t in p.tags:
                tags.append(t)
        return sorted(list(set(tags)))

    @property
    def source_files(self):

        if self._source_files:
            return self._source_files

        for root, dirs, files in os.walk(conf.source_path):
            for f in files:
                if not f.endswith(conf.source_ext):
                    continue
                fullpath = os.path.join(root, f)
                fname = fullpath.replace(conf.source_path+'/', '')
                self._source_files.append(fname)

        return self._source_files

class Post(object):
    """ Post object loads, saves, and caches posts """

    source_fname = None
    toc = None
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
    _has_toc = None
    _hide_author = None

    def __init__(self, source_fname):
        conf.check()
        self.source_fname = source_fname

    def save(self):

        full_dir = os.path.split(self.target_path)[0]

        if not os.path.exists(full_dir):
            try:
                conf.logger.info('Making directory: %s'%(full_dir))
                os.makedirs(full_dir)
            except Exception as e:
                raise Exception('Cannot create directory: %s'%(full_dir))


        pc = self.conf
        tt = self.target_text
        conf.logger.debug('Saving to: %s'%(self.target_path))
        html = render_theme_template(conf.post_tpl, post=self)
        u_write(self.target_path, html)

    def get_section(self, name, raw=True):
        """ Load a post section """

        pat = re.compile(r'\{section:%s\}(.*?)\{endsection\}'%(name), re.DOTALL|re.M)
        m = pat.search(self.source_text)
        if not m:
            return None
        # By default, return raw text
        if raw:
            return m.group(1)
        return markdown.markdown(m.group(1),
            extensions=conf.markdown_exts)

    @property
    def author(self):
        if self._author:
            return self._author
        if self.conf.get('author'):
            self._author = self.conf['author']
            return self._author
        self._author = conf.site.get('author', 'Nobody')
        return self._author

    @property
    def hide_author(self):
        if self._hide_author != None:
            return self._hide_author
        self._hide_author = self.conf.get('hide_author', False)
        return self._hide_author

    @property
    def conf(self):

        if self._conf:
            return self._conf

        m = (
            conf.post_conf_re.search(self.source_text) or
            conf.post_conf_re2.search(self.source_text)
        )
        if not m:
            conf.logger.warning('No post config specified for %s'%(self.source_fname))
            self._conf = {'foo':True}
            return {}

        try:
            self._conf = yaml.load(m.group(1))
            self._source_text = self.source_text.replace(m.group(0), '')
        except Exception as e:
            conf.logger.exception('Invalid post configuration found!')

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
    def url(self):
        url = []
        if conf.site.get('base_url'):
            url.append(conf.site['base_url'])
        if conf.web_prefix:
            url.append(conf.web_prefix)
        url.append(self.target_fname)
        return '/'.join(url)

    @property
    def source_text(self):
        if self._source_text:
            return self._source_text

        if not os.path.exists(self.source_path):
            raise Exception('Cannot locate file: %s'%(self.source_path))

        self._source_text = u_read(self.source_path)

        # Check for table of contents, and extract for theme
        tocm = conf.post_toc_re.search(self._source_text)
        if tocm:
            self._has_toc = True
            self._source_text = conf.post_toc_re.sub('', self._source_text)
            md = markdown.Markdown(extensions=conf.markdown_exts)
            md.convert(self.source_text)
            self.toc = md.toc

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
        conf.logger.debug('Caching: %s'%(self.source_fname))
        md = markdown.Markdown(extensions=conf.markdown_exts)
        html = md.convert(self.source_text)
        #self._toc = md.toc
        #conf.logger.info("Got TOC:%s"%(self._toc))
        self._target_text = html
        return self._target_text

    @property
    def mtime(self):
        if self._mtime:
            return self._mtime

        if self.conf.get('timestamp'):
            self._mtime = time.mktime(time.strptime(self.conf['timestamp'], conf.timestamp_format))
            return self._mtime

        self._mtime = self.source_mtime
        return self._mtime

    @property
    def mtime_tuple(self):
        return time.localtime(self.mtime)

    @property
    def mtimestamp(self):
        return time.strftime(conf.timestamp_format, self.mtime_tuple)

    @property
    def mtimestamp_rfc822(self):

        """ Gets RSS/Email Compatible, RFC 822 based, date """

        return time.strftime('%a, %d %b %Y %H:%M:%S %Z', self.mtime_tuple)

    @property
    def mtime_string(self):
        return time.strftime(conf.time_format, self.mtime_tuple)

    @property
    def mdate_string(self):
        return time.strftime(conf.date_format, self.mtime_tuple)

    @property
    def mtime_hour(self):
        return time.strftime('%H', self.mtime_tuple)

    @property
    def mtime_minute(self):
        return time.strftime('%M', self.mtime_tuple)

    @property
    def mdate_day(self):
        return time.strftime('%d', self.mtime_tuple)

    @property
    def mdate_month(self):
        return time.strftime('%m', self.mtime_tuple)

    @property
    def mdate_year(self):
        return time.strftime('%Y', self.mtime_tuple)

    @property
    def target_mtime(self):
        if os.path.exists(self.target_path):
            return os.path.getmtime(self.target_path)
        return 0

    @property
    def source_mtime(self):
        return os.path.getmtime(self.source_path)

    @property
    def nowrap(self):
        return self.conf.get('nowrap');

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
ctrl = PostController()
