biomaj-manager
==============

This project intends to be a contrib around BioMAJ3 (https://github.com/genouest/biomaj).
It is a kind of swiss knife extending BioMAJ3 by adding some methods helping you to have
extra information about your banks like pending bank(s), information about a bank, history
of a banks (updated releases) plus some more.

Installation
============

* Install required packages
 * `pip install -r requirements.txt`
* Now go to the biomaj-manager directory and type
 * `python setup.py install`

Configuration file
==================

A configuration file is required to work. This file called `manager.properties` must be located
in the same location as `global.properties` from BioMAJ3.
It must start with a section called `[MANAGER]` and at least have the following properties defined to work.

```
[MANAGER]
root.dir=/path/to/config/directory
template.dir=%(root.dir)s/templates
news.dir=%(root.dir)s/news
production.dir=%(root.dir)s/production
plugins.dir=%(root.dir)s/plugins
```

Usage
=====
```
usage: biomaj-manager.py [-h] [-A [Max release]] [-D] [-H] [-i] [-I] [-J] [-l]
                         [-L] [-N] [-n] [-P] [-R] [-s] [-X] [-U] [-v]
                         [-V] [--test] [-Z] [-b BANK] [-B [path to check]]
                         [-C [path to clean]] [-c CONFIG] [--db_type DB_TYPE]
                         [-E [session id]] [-o OUT] [-F OFORMAT] [-r RELEASE]
                         [-S [blast2|golden]] [-T TEMPLATE_DIR]
                         [--vdbs [blast2|golden]]
                         [--visibility all|public|private] [-w file:seq_num]

BioMAJ Manager adds some functionality around BioMAJ.

optional arguments:
  -h, --help            show this help message and exit
  -A [Max release], --check_prod_release [Max release]
                        Look for bank having stored releases greater than [Max
                        release, default to 'keep.old.version']. [-b
                        available]
  -D, --save_versions   Prints info about all banks into version file.
                        (Requires permissions)
  -H, --history         Prints banks releases history. [-b] available.
  -i, --info            Print info about a bank. [-b REQUIRED]
  -I, --remote-info     Print remote info for a bank remote connection. [-b
                        REQUIRED]
  -J, --check_links     Check if the bank required symlinks to be created
                        (Permissions required). [-b REQUIRED]
  -l, --links           Just (re)create symlink, don't do any bank switch.
                        (Permissions required). [-b REQUIRED]
  -L, --bank_formats    List supported formats and index for each banks. [-b]
                        available.
  -N, --news            Create news to display at BiomajWatcher. [Default
                        output txt]
  -n, --simulate        Simulate action, don't do it really.
  -P, --show_pending    Show pending release(s). [-b] available
  -R, --rss             Create RSS feed. [-o available]
  -s, --switch          Switch a bank to its new version. [-b REQUIRED]
  -X, --synchronize_db  Synchronize database and bank data on disk
  -U, --show_update     If -b passed prints if bank needs to be updated.
                        Otherwise, prints all bank that need to be updated.
                        [-b and --visibility] available.
  -v, --version         Show version
  -V, --verbose         Activate verbose mode
  --test                Test method. [-b REQUIRED]
  -Z, --clean_sessions  Clean dead sessions from the database. [-b REQUIRED]
  -b BANK, --bank BANK  Bank name
  -B [path to check], --broken_links [path to check]
                        Check for broken symlinks in production directory.
  -C [path to clean], --clean_links [path to clean]
                        Remove old/broken links (Permissions required)
  -c CONFIG, --config CONFIG
                        BioMAJ global.properties configuration file
  -E [session id], --failed-process [session id]
                        Get failed process(es) for a bank. Session id can be
                        used. [-b REQUIRED]
  -o OUT, --out OUT     Output file
  -F OFORMAT, --format OFORMAT
                        Output format. Supported [csv, html, json]
  -S [blast2|golden], --section [blast2|golden]
                        Prints [blast2|golden] section(s) for a bank. [-b
                        REQUIRED]
  -T TEMPLATE_DIR, --templates TEMPLATE_DIR
                        Template directory. Overwrites template_dir
  --vdbs [blast2|golden]
                        Create virtual database HTML pages for tool. [-b
                        available]
  --visibility all|public|private
                        Banks visibility. Use with --show_update.
```

Plugins support
===============

Biomaj Manager is able to work plugins. To do so, a `plugins` directory is here to put your own developed
plugins. Plugins support is based on Yapsy (http://yapsy.sourceforge.net/) package. In order to plug you
plugin into Biomaj Manager, create a python package youplugin.py and a description file yourplugin.yapsy-plugin
in the `plugins` directory. To describe your plugin, see http://yapsy.sourceforge.net/PluginManager.html for
more information.
Once this is done, fill file `manager.properties` within the `[PLUGINS]` section as follow:
```
...
plugins.dir=/path/to/biomaj-manager/plugins

[PLUGINS]
plugins.list=yourplugin

[YouPlugin]
yourplugin.var=value
yourplugin.anothervar=anothervalue
...
``` 
The way the plugin system is working, it requires that the plugin class you created in `yourplugin.py`
must match the `[YouPlugin]` and must inherit from `BMPlugin` (`biomajmanager.plugin`) section to work.
For example `yourplugin.py`:
```
import os
import sys

from biomajmanager.plugins import BMPlugin

class YouPlugin(BMPlugin):
    """
    My first Biomaj Manager plugin
    """
    def __init__(self, ...)

```

Tests
=====

You can run tests by typing `nosetests`

It is also possible to clone this repo into gitlab and run tests using gitlab-ci. There's a `.gitlab-ci.yml` available for
this as well as a `Dockerfile` to run gitlab tests inside Docker.

Status
======
[![Build Status](https://travis-ci.org/horkko/biomaj-manager.svg?branch=master)](https://travis-ci.org/horkko/biomaj-manager)
[![Coverage Status](https://coveralls.io/repos/github/horkko/biomaj-manager/badge.svg?branch=master)](https://coveralls.io/github/horkko/biomaj-manager?branch=master)
[![Code Health](https://landscape.io/github/horkko/biomaj-manager/master/landscape.svg?style=flat)](https://landscape.io/github/horkko/biomaji-manager/master)
[![Code Climate](https://codeclimate.com/github/horkko/biomaj-manager/badges/gpa.svg)](https://codeclimate.com/github/horkko/biomaj-manager)
[![Documentation Status](https://readthedocs.org/projects/biomaj-manager/badge/?version=latest)](http://biomaj-manager.readthedocs.io/en/latest/?badge=latest)
