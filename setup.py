#!/usr/bin/python
# -*- coding: utf-8 -*-
from distutils.core import setup

PLUGIN_DIR = 'Extensions.Athantimes'

setup(name='enigma2-plugin-extensions-Athantimes',
       version='1.0',
       author='AbouYacine',
       support='RAED',
       author_email='rrrr53@hotmail.com',
       description='plugin by (AbouYacine - aime-jeux) Update and support by (RAED)',
       packages=[PLUGIN_DIR],
       package_dir={PLUGIN_DIR: 'usr'},
       package_data={PLUGIN_DIR: ['plugin.png', '*/*.png']},
      )
