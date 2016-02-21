#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

AUTHOR = 'Kevin Gullikson'
SITENAME = 'Adventures of the Datastronomer'
SITEURL = ''

PATH = 'content'

TIMEZONE = 'America/Chicago'

DEFAULT_LANG = 'en'

DISPLAY_PAGES_ON_MENU = True
STATIC_PATHS = ['Images', 'Figures', 'Downloads', 'Javascript', 'static']
PAGE_EXCLUDES = ['Javascript']
ARTICLE_EXCLUDES = STATIC_PATHS

# Theme and plugins
THEME = 'pelican-octopress-theme/'
PLUGIN_PATH = 'pelican-plugins'
PLUGINS = ['summary', 'liquid_tags.img', 'liquid_tags.video',
           'liquid_tags.include_code', 'liquid_tags.notebook',
           'liquid_tags.literal', 'render_math']

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None

# Blogroll
LINKS = (('My Academic Website', 'http://www.as.utexas.edu/~kgulliks/index.html'),)

# Social widget
SOCIAL = (('Facebook', 'https://www.facebook.com/kevin.gullikson'),
          ('Google+', 'https://plus.google.com/u/0/+KevinGullikson'),
          ('LinkedIn', 'http://www.linkedin.com/in/KevinGullikson'),
          ('Github', 'http://github.com/kgullikson88'),)

DEFAULT_PAGINATION = 10

# Uncomment following line if you want document-relative URLs when developing
#RELATIVE_URLS = True
