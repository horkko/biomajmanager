from __future__ import print_function
from nose.tools import *
from nose.plugins.attrib import attr

import shutil
import os
import sys
import tempfile
import time
import unittest
from pymongo import MongoClient
from datetime import datetime

from biomajmanager.utils import Utils
from biomajmanager.news import News
from biomajmanager.manager import Manager


__author__ = 'tuco'


class UtilsForTests(object):
    """
    Copy properties files into a temporary directory and update properties
    to use a temp directory
    """

    def __init__(self):
        '''
        Setup the temp dirs and files.
        '''
        self.global_properties = None
        self.manager_properties = None
        self.db_test = 'bm_db_test'
        self.col_test = 'bm_col_test'
        self.test_dir = tempfile.mkdtemp('biomaj-manager_tests')

        # Global part
        self.conf_dir = os.path.join(self.test_dir, 'conf')
        if not os.path.exists(self.conf_dir):
            os.makedirs(self.conf_dir)
        self.data_dir = os.path.join(self.test_dir, 'data')
        if not os.path.exists(self.data_dir):
            os.makedirs(self.data_dir)
        self.log_dir = os.path.join(self.test_dir, 'log')
        if not os.path.exists(self.log_dir):
            os.makedirs(self.log_dir)
        self.process_dir = os.path.join(self.test_dir, 'process')
        if not os.path.exists(self.process_dir):
            os.makedirs(self.process_dir)
        self.lock_dir = os.path.join(self.test_dir, 'lock')
        if not os.path.exists(self.lock_dir):
            os.makedirs(self.lock_dir)
        self.cache_dir = os.path.join(self.test_dir, 'cache')
        if not os.path.exists(self.cache_dir):
            os.makedirs(self.cache_dir)
        # Manager part
        self.template_dir = os.path.join(self.test_dir, 'templates')
        if not os.path.exists(self.template_dir):
            os.makedirs(self.template_dir)
        self.news_dir = os.path.join(self.test_dir, 'news')
        if not os.path.exists(self.news_dir):
            os.makedirs(self.news_dir)
        self.prod_dir = os.path.join(self.test_dir,'production')
        if not os.path.exists(self.prod_dir):
            os.makedirs(self.prod_dir)
        self.plugins_dir = os.path.join(self.test_dir,'plugins')
        if not os.path.exists(self.plugins_dir):
            os.makedirs(self.plugins_dir)
        self.tmp_dir = os.path.join(self.test_dir, 'tmp')
        if not os.path.exists(self.tmp_dir):
            os.makedirs(self.tmp_dir)

        if self.global_properties is None:
            self.__copy_test_global_properties()

        if self.manager_properties is None:
            self.__copy_test_manager_properties()

        # Set a mongo client
        self.mongo_client = MongoClient('mongodb://localhost:27017')

    def copy_file(self, file=None, todir=None):
        """
        Copy a file from the test dir to temp test zone
        :param file: File to copy
        :param todir: Destinatin directory
        :return:
        """
        curdir = self.__get_curdir()
        fromdir = os.path.join(curdir, file)
        todir = os.path.join(todir, file)
        shutil.copyfile(fromdir, todir)

    def copy_news_files(self):
        """
        Copy news file from test directory to 'news' testing directory
        :return:
        """
        curdir = self.__get_curdir()
        for news in ['news1.txt', 'news2.txt', 'news3.txt']:
            from_news = os.path.join(curdir, news)
            to_news = os.path.join(self.news_dir, news)
            shutil.copyfile(from_news, to_news)

    def copy_plugins(self):
        """
        Copy plugins from test directory to 'plugins' testing directory
        :return:
        """
        dsrc = 'tests/plugins'
        for file in os.listdir(dsrc):
            shutil.copyfile(os.path.join(dsrc, file),
                            os.path.join(self.plugins_dir, file))

    def clean(self):
        '''
        Deletes temp directory
        '''
        shutil.rmtree(self.test_dir)

    def drop_db(self):
         """
         Drop the mongo database after using it and close the connection
         :return:
         """
         self.mongo_client.drop_database(self.db_test)
         self.mongo_client.close()

    def print_err(self, msg):
        """
        Prints message on sys.stderr
        :param msg:
        :return:
        """
        print(msg, file=sys.stderr)

    def __get_curdir(self):
        """
        Get the current directory
        :return:
        """
        return os.path.dirname(os.path.realpath(__file__))

    def __copy_test_manager_properties(self):

        self.manager_properties = os.path.join(self.conf_dir, 'manager.properties')
        curdir = self.__get_curdir()
        manager_template = os.path.join(curdir, 'manager.properties')
        mout = open(self.manager_properties, 'w')
        with open(manager_template, 'r') as min:
            for line in min:
                if line.startswith('template.dir'):
                    mout.write("template.dir=%s\n" % self.template_dir)
                elif line.startswith('news.dir'):
                    mout.write("news.dir=%s\n" % self.news_dir)
                elif line.startswith('production.dir'):
                    mout.write("production.dir=%s\n" % self.prod_dir)
                elif line.startswith('plugins.dir'):
                    mout.write("plugins.dir=%s\n" % self.plugins_dir)
                else:
                    mout.write(line)
        mout.close()

    def __copy_test_global_properties(self):

        self.global_properties = os.path.join(self.conf_dir, 'global.properties')
        curdir = os.path.dirname(os.path.realpath(__file__))
        global_template = os.path.join(curdir, 'global.properties')
        fout = open(self.global_properties, 'w')
        with open(global_template, 'r') as fin:
            for line in fin:
                if line.startswith('cache.dir'):
                    fout.write("cache.dir=%s\n" % self.cache_dir)
                elif line.startswith('conf.dir'):
                    fout.write("conf.dir=%s\n" % self.conf_dir)
                elif line.startswith('log.dir'):
                    fout.write("log.dir=%s\n" % self.log_dir)
                elif line.startswith('data.dir'):
                    fout.write("data.dir=%s\n" % self.data_dir)
                elif line.startswith('process.dir'):
                    fout.write("process.dir=%s\n" % self.process_dir)
                elif line.startswith('lock.dir'):
                    fout.write("lock.dir=%s\n" % self.lock_dir)
                else:
                    fout.write(line)


class TestBiomajManagerUtils(unittest.TestCase):

    def setUp(self):
        self.utils = UtilsForTests()

    def tearDown(self):
        self.utils.clean()

    @attr('utils')
    def test_deepest_dir_ErrorNoPath(self):
        """
        Check methods checks are OK
        :return:
        """
        with self.assertRaises(SystemExit):
            Utils.get_deepest_dirs()

    @attr('utils')
    def test_deepest_dir_ErrorPathNotExists(self):
        """
        Check methods checks are OK
        :return:
        """
        with self.assertRaises(SystemExit):
            Utils.get_deepest_dirs(path='/not_found')

    @attr('utils')
    def test_deepest_dir(self):
        """
        Check we get the right deepest dir from a complete path
        :return:
        """
        dir = os.path.join(self.utils.tmp_dir, 'a', 'b', 'c')
        if not os.path.exists(dir):
            os.makedirs(dir)
        deepest = Utils.get_deepest_dir(dir)
        self.assertEqual(deepest, 'c')
        shutil.rmtree(self.utils.tmp_dir)

    @attr('utils')
    def test_deepest_dir_full(self):
        """
        Check we get the right full deepest dir
        :return:
        """
        dir = os.path.join(self.utils.tmp_dir, 'a', 'b', 'c', 'd')
        if not os.path.exists(dir):
            os.makedirs(dir)
        deepest = Utils.get_deepest_dir(dir, full=True)
        self.assertEqual(deepest, dir)
        shutil.rmtree(self.utils.tmp_dir)

    @attr('utils')
    def test_deepest_dirs(self):
        """
        Check we get the right list of deepest dir
        :return:
        """
        dir = os.path.join(self.utils.tmp_dir, 'a', 'b')
        dir1 = os.path.join(dir, 'c')
        dir2 = os.path.join(dir, 'd')
        for d in [dir1, dir2]:
            if not os.path.exists(d):
                os.makedirs(d)
        deepest = Utils.get_deepest_dirs(dir)
        c = deepest[0]
        d = deepest[1]
        self.assertEqual(c, 'c')
        self.assertEqual(d, 'd')
        shutil.rmtree(self.utils.tmp_dir)

    @attr('utils')
    def test_deepest_dirs_full(self):
        """
        Check we get the right list of deepest dir
        :return:
        """
        dir = os.path.join(self.utils.tmp_dir, 'a', 'b')
        dir1 = os.path.join(dir, 'c')
        dir2 = os.path.join(dir, 'd')
        for d in [dir1, dir2]:
            if not os.path.exists(d):
                os.makedirs(d)
        deepest = Utils.get_deepest_dirs(dir, full=True)
        c = deepest[0]
        d = deepest[1]
        self.assertEqual(c, dir1)
        self.assertEqual(d, dir2)
        shutil.rmtree(self.utils.tmp_dir)

    @attr('utils')
    def test_get_files(self):
        """
        Check we get the right file list from a directory
        :return:
        """
        tmp_file1 = os.path.join(self.utils.tmp_dir, '1foobar.tmp')
        tmp_file2 = os.path.join(self.utils.tmp_dir, '2foobar.tmp')
        open(tmp_file1, mode='a').close()
        open(tmp_file2, mode='a').close()
        files = Utils.get_files(self.utils.tmp_dir)
        b_tmp_file1 = os.path.basename(tmp_file1)
        b_tmp_file2 = os.path.basename(tmp_file2)
        self.assertEqual(b_tmp_file1, files[0])
        self.assertEqual(b_tmp_file2, files[1])
        shutil.rmtree(self.utils.tmp_dir)

    @attr('utils')
    def test_get_files_ErrorNoPath(self):
        """
        Check we get an error when omitting args
        :return:
        """
        with self.assertRaises(SystemExit):
            Utils.get_files()

    @attr('utils')
    def test_get_files_ErrorPathNotExists(self):
        """
        Check we get an error when omitting args
        :return:
        """
        with self.assertRaises(SystemExit):
            Utils.get_files(path='/not_found')

    @attr('utils')
    def test_elapsedTime_Error(self):
        """
        Check this method throw an error
        :return:
        """
        with self.assertRaises(SystemExit):
            Utils.elapsed_time()

    @attr('utils')
    def test_elapsedtime_NoTimerStop(self):
        """
        Check we go deeper in method setting time_stop to None
        :return:
        """
        Utils.timer_stop = None
        Utils.start_timer()
        self.assertIsInstance(Utils.elapsed_time(), float)

    @attr('utils')
    def test_local2utc(self):
        """
        Check local2utc returns the right time according to local time
        :return:
        """
        now = datetime.now()
        utc_now = Utils.local2utc(now)
        self.assertEquals(utc_now.hour + 1, now.hour)

    @attr('utils')
    def test_local2utc_WrongArgsType(self):
        """
        We check the args instance checking throws an error
        :return:
        """
        with self.assertRaises(SystemExit):
            Utils.local2utc(int(2))

    @attr('utils')
    def test_time2date_NoArgs(self):
        """
        Check the method throws an error if no args given
        :return:
        """
        with self.assertRaises(TypeError):
            Utils.time2date()

    @attr('utils')
    def test_time2date_ReturnedOK(self):
        """
        Check value returned is right object
        :return:
        """
        self.assertIsInstance(Utils.time2date(time.time()), datetime)

    @attr('utils')
    def test_time2datefmt_NoArgs(self):
        """
        Check the method throws an error if no args given
        :return:
        """
        with self.assertRaises(TypeError):
            Utils.time2datefmt()

    @attr('utils')
    def test_time2datefmt_ReturnedOK(self):
        """
        Check value returned is right object
        :return:
        """
        self.assertIsInstance(Utils.time2datefmt(time.time(), Manager.DATE_FMT), str)

    @attr('utils')
    def test_userOK(self):
        """
        Check the testing user is ok
        :return:
        """
        user = os.getenv("USER")
        self.assertEqual(Utils.user(), user)

    @attr('utils')
    def test_userNOTOK(self):
        """
        Check the testing user is ok
        :return:
        """
        user = "fakeUser"
        self.assertNotEqual(Utils.user(), user)


class TestBiomajManagerNews(unittest.TestCase):

    def setUp(self):
        self.utils = UtilsForTests()

    def tearDown(self):
        self.utils.clean()

    @attr('manager')
    @attr('manager.news')
    def test_NewsDirNotADirectory(self):
        """
        Check the dir given is not a directory
        :return:
        """
        dir = "/foorbar"
        with self.assertRaises(SystemExit):
            sys.stderr = open(os.devnull, 'w')
            News(news_dir=dir)

    @attr('manager')
    @attr('manager.news')
    def test_FileNewsContentEqual(self):
        """
        Check the content of 2 generated news files are identical
        :return:
        """

        self.utils.copy_news_files()
        data = []
        for i in range(1, 4):
            data.append({'type': 'type' + str(i),
                         'date': str(i) + '0/12/2015',
                         'title': 'News%s Title' % str(i),
                         'text': 'This is text #%s from news%s' %  (str(i), str(i)),
                         'item': i-1})
        news = News(news_dir=self.utils.news_dir)
        news_data = news.get_news()
        # Compare data
        data.reverse()

        if 'news' in news_data:
            for d in news_data['news']:
                n = data.pop()
                for k in ['type', 'date', 'title', 'text', 'item']:
                    self.assertEqual(d[k], n[k])
        else:
            raise(unittest.E)
        shutil.rmtree(self.utils.news_dir)

class TestBioMajManagerDecorators(unittest.TestCase):

    def setUp(self):
        self.utils = UtilsForTests()
        # Make our test global.properties set as env var
        os.environ['BIOMAJ_CONF'] = self.utils.global_properties

    def tearDown(self):
        self.utils.clean()

    @attr('manager')
    @attr('manager.decorators')
    def test_DecoratorBankRequiredOK(self):
        """
        Test we've got a bank name set
        :return:
        """
        self.utils.copy_file(file='alu.properties', todir=self.utils.conf_dir)
        manager = Manager(bank='alu')
        sections = manager.get_dict_sections('blast2')
        expected = {'nuc': {'dbs': ['alunuc']}, 'pro': {'dbs': ['alupro']}}
        self.assertDictContainsSubset(expected, sections)
        self.utils.drop_db()

    @attr('manager')
    @attr('manager.decorators')
    def test_DecoratorBankRequiredNotOK(self):
        """
        Test we've got a bank name set
        :return:
        """
        self.utils.copy_file(file='alu.properties', todir=self.utils.conf_dir)
        manager = Manager()
        with self.assertRaises(SystemExit):
            manager.get_dict_sections('blast2')
        self.utils.drop_db()

    @attr('manager')
    @attr('manager.decorators')
    def test_DecoratorsUserGrantedOK(self):
        """
        Test the user is granted
        :return:
        """
        self.utils.copy_file(file='alu.properties', todir=self.utils.conf_dir)
        manager = Manager(bank='alu')
        manager.save_banks_version(file=self.utils.test_dir + '/saved_versions.txt')
        self.utils.drop_db()

    @attr('manager')
    @attr('manager.decorators')
    def test_DecoratorsUserGrantedNotOK(self):
        """
        Test the user is granted
        :return:
        """
        self.utils.copy_file(file='alu.properties', todir=self.utils.conf_dir)
        manager = Manager(bank='alu')
        # Just change the env LOGNAME do misfit with db user
        cuser = os.environ.get('LOGNAME')
        os.environ['LOGNAME'] = "fakeuser"
        with self.assertRaises(SystemExit):
            manager.save_banks_version(file=self.utils.test_dir + '/saved_versions.txt')
        # Reset to the right user name as previously
        os.environ['LOGNAME'] = cuser
        self.utils.drop_db()

    @attr('manager')
    @attr('manager.decorators')
    def test_DecoratorsUserGrantedAdminNotSet(self):
        """
        Test the user is granted
        :return:
        """
        self.utils.copy_file(file='alu.properties', todir=self.utils.conf_dir)
        manager = Manager(bank='alu')
        # Unset admin from config file and owner from the bank just created
        manager.config.set('GENERAL', 'admin', None)
        manager.bank.bank['properties']['owner'] = None
        with self.assertRaises(SystemExit):
            manager.save_banks_version(file=self.utils.test_dir + '/saved_versions.txt')
        self.utils.drop_db()


class TestBioMajManagerManager(unittest.TestCase):

    def setUp(self):
        self.utils = UtilsForTests()
        # Make our test global.properties set as env var
        os.environ['BIOMAJ_CONF'] = self.utils.global_properties

    def tearDown(self):
        self.utils.clean()

    @attr('manager')
    def test_ManagerNoConfigRaisesException(self):
        """
        Check an exception is raised while config loading
        :return:
        """
        with self.assertRaises(SystemExit):
            manager = Manager(cfg="/no_manager_cfg", global_cfg="/no_global_cfg")

    @attr('manager')
    def test_ManagerGlobalConfigException(self):
        """
        Check an exception is raised config loading
        :return:
        """
        with self.assertRaises(SystemExit):
            manager = Manager(global_cfg="/no_global_cfg")

    @attr('manager')
    def test_ConfigNoManagerSection(self):
        """
        Check we don't have a 'MANAGER' section in our config
        :return:
        """
        no_sec = 'manager-nomanager-section.properties'
        self.utils.copy_file(file=no_sec, todir=self.utils.conf_dir)
        cfg = Manager.load_config(cfg=os.path.join(self.utils.conf_dir, no_sec))
        self.assertFalse(cfg.has_section('MANAGER'))

    @attr('manager')
    def test_ManagerLoadConfig(self):
        """
        Check we can load any configuration file on demand
        :return:
        """
        for file in ['m1.properties', 'm2.properties', 'm3.properties']:
            self.utils.copy_file(file=file, todir=self.utils.test_dir)
            cfg = Manager.load_config(cfg=os.path.join(self.utils.test_dir, file))
            self.assertTrue(cfg.has_section('MANAGER'))
            self.assertEqual(cfg.get('MANAGER', 'file.name'), file)

    @attr('manager')
    def test_ManagerBankPublishedTrue(self):
        """
        Check a bank is published or not (True)
        :return:
        """
        self.utils.copy_file(file='alu.properties', todir=self.utils.conf_dir)
        # at begining, biomaj create an empty bank entry into Mongodb
        manager = Manager(bank='alu')
        # If we do update we need to change 'bank_is_published' call find and iterate over the cursor to do the same test
        manager.bank.bank['current'] = True
        self.assertTrue(manager.bank_is_published())
        self.utils.drop_db()

    @attr('manager')
    def test_ManagerBankPublishedFalse(self):
        """
        Check a bank is published or not (False)
        :return:
        """
        self.utils.copy_file(file='alu.properties', todir=self.utils.conf_dir)
        # at begining, biomaj create an empty bank entry into Mongodb
        manager = Manager(bank='alu')
        # If we do update we need to change 'bank_is_published' call find and iterate over the cursor to do the same test
        manager.bank.bank['current'] = None
        self.assertFalse(manager.bank_is_published())
        self.utils.drop_db()

    @attr('manager')
    def test_ManagerLastSessionFailedFalseNoPendingFalse(self):
        """
        Check we have a failed session and no pending session(s)
        :return:
        """
        self.utils.copy_file(file='alu.properties', todir=self.utils.conf_dir)
        now = time.time()
        data = {'name': 'alu',
                'sessions': [{'id': 0, 'status': {'over': True}}, {'id': now, 'status':{'over': True}}],
                'last_update_session': now,
                }
        manager = Manager(bank='alu')
        manager.bank.bank = data
        self.assertFalse(manager.last_session_failed())
        self.utils.drop_db()

    @attr('manager')
    def test_ManagerLastSessionFailedTrueNoPendingTrue(self):
        """
        Check we have a failed session and no pending session(s)
        :return:
        """
        self.utils.copy_file(file='alu.properties', todir=self.utils.conf_dir)
        now = time.time()
        data = {'name': 'alu',
                'sessions': [{'id': 0, 'status': {'over': True}}, {'id': now, 'status':{'over': True}}],
                'last_update_session': now,
                'pending': {'12345': now}
                }
        manager = Manager(bank='alu')
        manager.bank.bank = data
        Utils.show_warn = False
        self.assertTrue(manager.last_session_failed())
        self.utils.drop_db()

    @attr('manager')
    def test_ManagerLastSessionFailedTrueNoPendingFalse(self):
        """
        Check we have a failed session and no pending session(s)
        :return:
        """
        self.utils.copy_file(file='alu.properties', todir=self.utils.conf_dir)
        now = time.time()
        data = {'name': 'alu',
                'sessions': [{'id': 0, 'status': {'over': True}}, {'id': now, 'status':{'over': False}}],
                'last_update_session': now,
                }
        manager = Manager(bank='alu')
        manager.bank.bank = data
        Utils.show_warn = False
        self.assertTrue(manager.last_session_failed())
        self.utils.drop_db()

    @attr('manager')
    def test_ManagerBankHasFormatNoFormat(self):
        """
        Check missing arg raises error
        :return:
        """
        self.utils.copy_file(file='alu.properties', todir=self.utils.conf_dir)
        manager = Manager(bank='alu')
        with self.assertRaises(SystemExit):
            manager.has_formats()
        self.utils.drop_db()

    @attr('manager')
    def test_ManagerBankHasFormatsTrue(self):
        """
        Check if the bank has a specific format (True)
        :return:
        """
        self.utils.copy_file(file='alu.properties', todir=self.utils.conf_dir)
        manager = Manager(bank='alu')
        self.assertTrue(manager.has_formats(fmt='blast'))
        self.utils.drop_db()

    @attr('manager')
    def test_ManagerBankHasFormatsFalse(self):
        """
        Check if the bank has a specific format (False)
        :return:
        """
        self.utils.copy_file(file='alu.properties', todir=self.utils.conf_dir)
        manager = Manager(bank='alu')
        self.assertFalse(manager.has_formats(fmt='unknown'))
        self.utils.drop_db()

    @attr('manager')
    def test_ManagerGetSessionFromIDNotNone(self):
        """
        Check we retrieve the right session id (Not None)
        :return:
        """
        self.utils.copy_file(file='alu.properties', todir=self.utils.conf_dir)
        data = {'name': 'alu',
                'sessions': [{'id': 1, 'status': { 'over': True}},
                             {'id': 2, 'status': { 'over': True}},]}
        manager = Manager(bank='alu')
        manager.bank.bank = data
        self.assertIsNotNone(manager.get_session_from_id(1))
        self.utils.drop_db()

    @attr('manager')
    def test_ManagerGetSessionFromIDNone(self):
        """
        Check we retrieve the right session id (None)
        :return:
        """
        self.utils.copy_file(file='alu.properties', todir=self.utils.conf_dir)
        data = {'name': 'alu',
                'sessions': [{'id': 1, 'status': { 'over': True}},
                             {'id': 2, 'status': { 'over': True}},]}
        manager = Manager(bank='alu')
        manager.bank.bank = data
        self.assertIsNone(manager.get_session_from_id(3))
        self.utils.drop_db()

    @attr('manager')
    def test_ManagerGetPublishedReleaseNotNone(self):
        """
        Check we get a the published release (NotNone)
        :return:
        """
        self.utils.copy_file(file='alu.properties', todir=self.utils.conf_dir)
        now = time.time()
        release = 'R54'
        data = {'name': 'alu',
                'current': now,
                'sessions': [{'id': 1, 'remoterelease': 'R1'}, {'id': now, 'remoterelease': release}]
                }
        manager = Manager(bank='alu')
        manager.bank.bank = data
        rel = manager.get_published_release()
        self.assertIsNotNone(rel)
        self.utils.drop_db()

    @attr('manager')
    def test_ManagerGetPublishedReleaseNone(self):
        """
        Check we get a the published release (None)
        :return:
        """
        self.utils.copy_file(file='alu.properties', todir=self.utils.conf_dir)
        now = time.time()
        release = 'R54'
        data = {'name': 'alu',
                'sessions': [{'id': 1, 'remoterelease': 'R1'}, {'id': now, 'remoterelease': release}]
                }
        manager = Manager(bank='alu')
        manager.bank.bank = data
        rel = manager.get_published_release()
        self.assertIsNone(rel)
        self.utils.drop_db()

    @attr('manager')
    @attr('manager.sections')
    def test_ManagerGetDictSections(self):
        """
        Get sections for a bank
        :return:
        """
        self.utils.copy_file(file='alu.properties', todir=self.utils.conf_dir)
        manager = Manager(bank='alu')
        dsections = manager.get_dict_sections(tool='blast2')
        expected = {'pro': {'dbs': ['alupro']}, 'nuc': {'dbs': ['alunuc']}}
        self.assertDictContainsSubset(expected, dsections)
        self.utils.drop_db()

    @attr('manager')
    @attr('manager.sections')
    def test_ManagerGetListSections(self):
        """
        Check we get rigth sections for bank
        :return:
        """
        self.utils.copy_file(file='alu.properties', todir=self.utils.conf_dir)
        manager = Manager(bank='alu')
        lsections = manager.get_list_sections(tool='golden')
        self.assertListEqual(lsections, ['alunuc', 'alupro'])
        self.utils.drop_db()

    @attr('manager')
    @attr('manager.sections')
    def test_ManagerGetDictSectionsNoTool(self):
        """
        Get sections for a bank
        :return:
        """
        self.utils.copy_file(file='alu.properties', todir=self.utils.conf_dir)
        manager = Manager(bank='alu')
        with self.assertRaises(SystemExit):
            manager.get_dict_sections()
        self.utils.drop_db()

    @attr('manager')
    @attr('manager.sections')
    def test_ManagerGetListSectionsNoTool(self):
        """
        Get sections for a bank
        :return:
        """
        self.utils.copy_file(file='alu.properties', todir=self.utils.conf_dir)
        manager = Manager(bank='alu')
        with self.assertRaises(SystemExit):
            manager.get_list_sections()
        self.utils.drop_db()

    @attr('manager')
    @attr('manager.currentrelease')
    def test_ManagerGetCurrentRelease_CurrentANDSessions(self):
        """
        Check we get the right current release
        :return:
        """
        self.utils.copy_file(file='alu.properties', todir=self.utils.conf_dir)
        now = time.time()
        release = 'R54'
        data = {'name': 'alu',
                'current': now,
                'sessions': [{'id': 1, 'remoterelease': 'R1'}, {'id': now, 'remoterelease': release}]
                }
        manager = Manager(bank='alu')
        manager.bank.bank = data
        self.assertEqual(release, manager.current_release())
        self.utils.drop_db()

    @attr('manager')
    @attr('manager.currentrelease')
    def test_ManagerGetCurrentRelease_ProductionRemoteRelease(self):
        """
        Check we get the right current release
        :return:
        """
        self.utils.copy_file(file='alu.properties', todir=self.utils.conf_dir)
        now = time.time()
        release = 'R54'
        data = {'name': 'alu',
                'production': [{'id': 1, 'remoterelease': 'R1'}, {'id': now, 'remoterelease': release}]
                }
        manager = Manager(bank='alu')
        manager.bank.bank = data
        self.assertEqual(release, manager.current_release())
        self.utils.drop_db()

    @attr('manager')
    @attr('manager.currentrelease')
    def test_ManagerGetCurrentRelease_ProductionRelease(self):
        """
        Check we get the right current release
        :return:
        """
        self.utils.copy_file(file='alu.properties', todir=self.utils.conf_dir)
        now = time.time()
        release = 'R54'
        data = {'name': 'alu',
                'production': [{'id': 1, 'remoterelease': 'R1'}, {'id': now, 'release': release}]
                }
        manager = Manager(bank='alu')
        manager.bank.bank = data
        self.assertEqual(release, manager.current_release())
        self.utils.drop_db()

    @attr('manager')
    @attr('manager.currentlink')
    def test_ManagerGetCurrentLinkNOTOK(self):
        """
        Check get_current_link throws exception
        :return:
        """
        self.utils.copy_file(file='alu.properties', todir=self.utils.conf_dir)
        manager = Manager(bank='alu')
        cur_link = manager.get_current_link()
        self.assertNotEqual(cur_link, '/wrong_curent_link')
        self.utils.drop_db()

    @attr('manager')
    @attr('manager.currentlink')
    def test_ManagerGetCurrentLinkOK(self):
        """
        Check get_current_link throws exception
        :return:
        """
        self.utils.copy_file(file='alu.properties', todir=self.utils.conf_dir)
        manager = Manager(bank='alu')
        cur_link = manager.get_current_link()
        self.assertEqual(cur_link, os.path.join(self.utils.data_dir, manager.bank.name, 'current'))
        self.utils.drop_db()

    @attr('manager')
    @attr('manager.currentproddir')
    def test_ManagerGetCurrentProdDir_Raises(self):
        """
        Check method returns good value for production directory
        :return:
        """
        self.utils.copy_file(file='alu.properties', todir=self.utils.conf_dir)
        manager = Manager(bank='alu')
        with self.assertRaises(SystemExit):
            manager.get_current_proddir()

    @attr('manager')
    @attr('manager.currentproddir')
    def test_ManagerGetCurrentProdDir_RaisesNoCurrentRelease(self):
        """
        Check method returns good value for production directory
        :return:
        """
        self.utils.copy_file(file='alu.properties', todir=self.utils.conf_dir)
        manager = Manager(bank='alu')
        manager.bank.bank['current'] = None
        manager.bank.bank['production'] = []
        with self.assertRaises(SystemExit):
            manager.get_current_proddir()

    @attr('manager')
    @attr('manager.currentproddir')
    def test_ManagerGetCurrentProdDir_OK(self):
        """
        Check method returns good value for production directory
        :return:
        """
        self.utils.copy_file(file='alu.properties', todir=self.utils.conf_dir)
        now = time.time()
        prod_dir = 'alu_54'
        manager = Manager(bank='alu')
        manager.bank.bank['current'] = now
        manager.bank.bank['sessions'].append({'id': now, 'release': '54'})
        manager.bank.bank['production'].append({'session': now, 'release': '54', 'data_dir': self.utils.data_dir,
                                                'prod_dir': prod_dir})
        returned = manager.get_current_proddir()
        expected = os.path.join(self.utils.data_dir, manager.bank.name, prod_dir)
        self.assertEqual(expected, returned)

    @attr('manager')
    @attr('manager.currentproddir')
    def test_ManagerGetCurrentProdDir_RaisesNoProd(self):
        """
        Check method returns good value for production directory
        :return:
        """
        self.utils.copy_file(file='alu.properties', todir=self.utils.conf_dir)
        now = time.time()
        prod_dir = 'alu_54'
        manager = Manager(bank='alu')
        manager.bank.bank['current'] = now
        manager.bank.bank['sessions'].append({'id': now, 'release': '54'})
        with self.assertRaises(SystemExit):
            manager.get_current_proddir()

    @attr('manager')
    def test_ManagerGetVerboseTrue(self):
        """
        Check manager.get_verbose() get True when Manager.verbose = True
        :return:
        """
        Manager.verbose = True
        manager = Manager()
        self.assertTrue(manager.get_verbose())

    @attr('manager')
    def test_ManagerGetVerboseFalse(self):
        """
        Check manager.get_verbose() get False when Manager.verbose = False
        :return:
        """
        Manager.verbose = False
        manager = Manager()
        self.assertFalse(manager.get_verbose())

    @attr('manager')
    @attr('manager.banklist')
    def test_ManagerGetBankListOK(self):
        """
        Check bank list works OK
        :return:
        """
        self.utils.copy_file(file='alu.properties', todir=self.utils.conf_dir)
        self.utils.copy_file(file='minium.properties', todir=self.utils.conf_dir)
        manager = Manager(bank='alu')
        manager2 = Manager(bank='minium')
        manual_list = ['alu', 'minium']
        bank_list = manager.get_bank_list()
        self.assertListEqual(bank_list, manual_list)
        self.utils.drop_db()

    @attr('manager')
    @attr('manager.banklist')
    def test_ManagerGetBankListNOTOK(self):
        """
        Check bank list throws exception
        :return:
        """
        from biomaj.mongo_connector import MongoConnector
        manager = Manager()
        # Unset MongoConnector and env BIOMAJ_CONF to force config relaod and Mongo reconnect
        MongoConnector.db = None
        os.environ['BIOMAJ_CONF'] = ""
        with self.assertRaises(SystemExit):
            manager.get_bank_list()
        self.utils.drop_db()

    @attr('manager')
    def test_ManagerGetConfigRegExpOKWithValuesTrue(self):
        """
        Check method get the right entries from config
        :return:
        """
        manager = Manager()
        my_values = manager.get_config_regex(regex='.*\.dir$', with_values=False)
        self.assertListEqual(my_values, ['lock.dir', 'log.dir', 'process.dir', 'data.dir', 'cache.dir', 'conf.dir'])
        self.utils.drop_db()

    @attr('manager')
    def test_ManagerGetConfigRegExpOKWithValuesFalse(self):
        """
        Check method get the right entries from config
        :return:
        """
        manager = Manager()
        my_values = manager.get_config_regex(regex='^db\.', with_values=True)
        self.assertListEqual(my_values, [self.utils.db_test, 'mongodb://localhost:27017'])
        self.utils.drop_db()

    @attr('manager')
    def test_ManagerGetConfigRegExpNoRegExp(self):
        """
        Check method get the right entries from config
        :return:
        """
        self.utils.copy_file(file='alu.properties', todir=self.utils.conf_dir)
        manager = Manager(bank='alu')
        with self.assertRaises(SystemExit):
            manager.get_config_regex()

    @attr('manager')
    def test_ManagerGetBankPackagesOK(self):
        """
        Check get_bank_packages() is ok
        :return:
        """
        self.utils.copy_file(file='alu.properties', todir=self.utils.conf_dir)
        manager = Manager(bank='alu')
        packs = ['pack@blast@2.2.26', 'pack@fasta@3.6']
        bank_packs = manager.get_bank_packages()
        self.assertListEqual(packs, bank_packs)
        self.utils.drop_db()

    @attr('manager')
    def test_ManagerGetBankPackagesNoneOK(self):
        """
        Check get_bank_packages() is ok
        :return:
        """
        self.utils.copy_file(file='minium.properties', todir=self.utils.conf_dir)
        manager = Manager(bank='minium')
        bank_packs = manager.get_bank_packages()
        self.assertIsNone(bank_packs)
        self.utils.drop_db()

    @attr('manager')
    @attr('manager.history')
    def test_ManagerHistoryNoProductionRaisesError(self):
        """
        Check when no 'production' field in bank, history raises exception
        :return:
        """
        self.utils.copy_file(file='alu.properties', todir=self.utils.conf_dir)
        manager = Manager(bank='alu')
        manager.bank.bank['production'] = None
        with self.assertRaises(SystemExit):
            manager.history()
        self.utils.drop_db()

    @attr('manager')
    @attr('manager.history')
    def test_ManagerHistoryNoSessionsRaisesError(self):
        """
        Check when no 'sessions' field in bank, history raises exception
        :return:
        """
        self.utils.copy_file(file='alu.properties', todir=self.utils.conf_dir)
        manager = Manager(bank='alu')
        manager.bank.bank['sessions'] = None
        with self.assertRaises(SystemExit):
            manager.history()
        self.utils.drop_db()

    @attr('manager')
    @attr('manager.history')
    def test_ManagerMongoHistoryNoProductionRaisesError(self):
        """
        Check when no 'production' field in bank, history raises exception
        :return:
        """
        self.utils.copy_file(file='alu.properties', todir=self.utils.conf_dir)
        manager = Manager(bank='alu')
        manager.bank.bank['production'] = None
        with self.assertRaises(SystemExit):
            manager.mongo_history()
        self.utils.drop_db()

    @attr('manager')
    @attr('manager.history')
    def test_ManagerMongoHistoryNoSessionsRaisesError(self):
        """
        Check when no 'sessions' field in bank, history raises exception
        :return:
        """
        self.utils.copy_file(file='alu.properties', todir=self.utils.conf_dir)
        manager = Manager(bank='alu')
        manager.bank.bank['sessions'] = None
        with self.assertRaises(SystemExit):
            manager.mongo_history()
        self.utils.drop_db()

    @attr('manager')
    def test_ManagerSaveBankVersionsNotOK(self):
        """
        Test excpetions
        :return:
        """
        self.utils.copy_file(file='alu.properties', todir=self.utils.conf_dir)
        manager = Manager(bank='alu')
        with self.assertRaises(SystemExit):
            manager.save_banks_version(file='/root/saved_versions.txt')
        # Reset to the right user name as previously
        self.utils.drop_db()

    @attr('manager')
    def test_ManagerSetBankOK(self):
        """
        Check method checks are ok
        :return:
        """
        self.utils.copy_file(file='alu.properties', todir=self.utils.conf_dir)
        manager = Manager()
        from biomaj.bank import Bank
        b = Bank('alu', no_log=True)
        self.assertTrue(manager.set_bank(bank=b))

    @attr('manager')
    def test_ManagerSetBankNOTOK(self):
        """
        Check method checks are not ok
        :return:
        """
        self.utils.copy_file(file='alu.properties', todir=self.utils.conf_dir)
        manager = Manager()
        self.assertFalse(manager.set_bank(bank=Manager()))

    @attr('manager')
    @attr('manager.switch')
    def test_ManagerBankSwitch_BankIsLocked(self):
        """
        Check manager.can_switch returns False because bank is locked
        :return:
        """
        self.utils.copy_file(file='alu.properties', todir=self.utils.conf_dir)
        manager = Manager(bank='alu')
        lock_file = os.path.join(manager.bank.config.get('lock.dir'), manager.bank.name + '.lock')
        with open(lock_file, 'a'):
            self.assertFalse(manager.can_switch())
        os.remove(lock_file)
        self.utils.drop_db()

    @attr('manager')
    @attr('manager.switch')
    def test_ManagerBankSwitch_BankNotPublished(self):
        """
        Check manager.can_switch returns False because bank not published yet
        :return:
        """
        self.utils.copy_file(file='alu.properties', todir=self.utils.conf_dir)
        manager = Manager(bank='alu')
        # To be sure we set 'current' from MongoDB to null
        manager.bank.bank['current'] = None
        self.assertFalse(manager.can_switch())
        self.utils.drop_db()

    @attr('manager')
    @attr('manager.switch')
    def test_ManagerBankSwitch_BankLastSessionFailed(self):
        """
        Check manager.can_switch returns False because last session failed
        :return:
        """
        self.utils.copy_file(file='alu.properties', todir=self.utils.conf_dir)
        manager = Manager(bank='alu')
        # We set 'current' field to avoid to return False with 'bank_is_published'
        now = time.time()
        manager.bank.bank['current'] = now
        # To be sure we set 'current' from MongoDB to null
        manager.bank.bank['last_update_session'] = now
        manager.bank.bank['sessions'].append({'id': now, 'status': {'over': False}})
        self.assertFalse(manager.can_switch())
        self.utils.drop_db()

    @attr('manager')
    @attr('manager.switch')
    def test_ManagerBankSwitch_SwitchTrue(self):
        """
        Check manager.can_switch returns True
        :return:
        """
        self.utils.copy_file(file='alu.properties', todir=self.utils.conf_dir)
        manager = Manager(bank='alu')
        # We set 'current' field to avoid to return False with 'bank_is_published'
        now = time.time()
        manager.bank.bank['current'] = now
        # To be sure we set 'current' from MongoDB to null
        manager.bank.bank['last_update_session'] = now + 1
        self.assertTrue(manager.can_switch())
        self.utils.drop_db()

    @attr('manager')
    @attr('manager.command')
    def test_ManagerCommandCheckConfigStop(self):
        """
        Check some config values are ok
        :return:
        """
        manager = Manager()
        manager.config.remove_option('MANAGER', 'jobs.stop.exe')
        # Grant usage for current user
        os.environ['LOGNAME'] = manager.config.get('GENERAL', 'admin')
        self.assertFalse(manager.stop_running_jobs())

    @attr('manager')
    @attr('manager.command')
    def test_ManagerCommandCheckConfigRestart(self):
        """
        Check some config values are ok
        :return:
        """
        manager = Manager()
        manager.config.remove_option('MANAGER', 'jobs.restart.exe')
        # Grant usage for current user
        os.environ['LOGNAME'] = manager.config.get('GENERAL', 'admin')
        self.assertFalse(manager.restart_stopped_jobs())

    @attr('manager')
    @attr('manager.command')
    def test_ManagerLaunchCommandOK(self):
        """
        Check a command started is OK
        :return:
        """
        manager = Manager()
        self.assertTrue(manager._run_command(exe='ls', args=['/tmp'], quiet=True))

    @attr('manager')
    @attr('manager.command')
    def test_ManagerLaunchCommandError(self):
        """
        Check a wrong return launched command
        :return:
        """
        manager = Manager()
        with self.assertRaises(SystemExit):
            manager._run_command(exe='ls', args=['/notfound'], quiet=True)

class TestBiomajManagerPlugins(unittest.TestCase):

    def setUp(self):
        self.utils = UtilsForTests()
        self.utils.copy_plugins()
        # Make our test global.properties set as env var
        os.environ['BIOMAJ_CONF'] = self.utils.global_properties

    def tearDown(self):
        pass
        self.utils.clean()

    @attr('plugins')
    def test_PluginLoadErrorNoManager(self):
        """
        Chek we've got an excedption thrown when Plugin Object is build without manager as args
        :return:
        """
        from biomajmanager.plugins import Plugins
        with self.assertRaises(SystemExit):
            plugin = Plugins()

    @attr('plugins')
    def test_PluginsLoadedOK_AsStandAlone(self):
        """
        Check the Plugins Object can be build as a standlone object
        :return:
        """
        from biomajmanager.plugins import Plugins
        manager = Manager()
        plugins = Plugins(manager=manager)
        self.assertIsInstance(plugins, Plugins)

    @attr('plugins')
    def test_PluginsLoaded(self):
        """
        Check a list of plugins are well loaded
        :return:
        """
        manager = Manager()
        manager.load_plugins()
        self.assertEqual(manager.plugins.myplugin.get_name(), 'myplugin')
        self.assertEqual(manager.plugins.anotherplugin.get_name(), 'anotherplugin')

    @attr('plugins')
    def test_PluginsLoadingNoSection(self):
        """
        Check the availability of section 'PLUGINS' is correctly checked
        :return:
        """
        manager = Manager()
        manager.config.remove_section('PLUGINS')
        with self.assertRaises(SystemExit):
            manager.load_plugins()

    @attr('plugins')
    def test_PluginsLoadingNoPLuginsDir(self):
        """
        Check the plugins.dir value is correctly checked
        :return:
        """
        manager = Manager()
        manager.config.remove_option('MANAGER', 'plugins.dir')
        with self.assertRaises(SystemExit):
            manager.load_plugins()

    @attr('plugins')
    def test_PluginsLoadingNoPLuginsList(self):
        """
        Check the plugins.dir value is correctly checked
        :return:
        """
        manager = Manager()
        manager.config.remove_option('PLUGINS', 'plugins.list')
        with self.assertRaises(SystemExit):
            manager.load_plugins()

    @attr('plugins')
    def test_PluginsLoadingNoPLuginsDirExists(self):
        """
        Check the plugins.dir path  is correctly checked
        :return:
        """
        manager = Manager()
        manager.config.set('MANAGER', 'plugins.dir', '/notfound')
        with self.assertRaises(SystemExit):
            manager.load_plugins()

    @attr('plugins')
    def test_PluginsLoadingNoConfig(self):
        """
        Check the plugins.dir value is correctly checked
        :return:
        """
        manager = Manager()
        manager.load_plugins()
        manager.config = None
        from configparser import RawConfigParser
        self.assertIsInstance(manager.plugins.myplugin.get_config(), RawConfigParser)

    @attr('plugins')
    def test_PluginsLoadingNoManager(self):
        """
        Check the plugins.dir value is correctly checked
        :return:
        """
        manager = Manager()
        manager.load_plugins()
        manager.manager = None
        self.assertIsInstance(manager.plugins.myplugin.get_manager(), Manager)


    @attr('plugins')
    def test_PluginsCheckConfigValues(self):
        """
        Check the plugins config values
        :return:
        """
        manager = Manager()
        manager.load_plugins()
        self.assertEqual(manager.plugins.myplugin.get_cfg_name(), 'myplugin')
        self.assertEqual(manager.plugins.myplugin.get_cfg_value(), '1')
        self.assertEqual(manager.plugins.anotherplugin.get_cfg_name(), 'anotherplugin')
        self.assertEqual(manager.plugins.anotherplugin.get_cfg_value(), '2')

    @attr('plugins')
    def test_PluginsCheckMethodValue(self):
        """
        Check the value returned by method is OK
        :return:
        """
        manager = Manager()
        manager.load_plugins()
        self.assertEqual(manager.plugins.myplugin.get_value(), 1)
        self.assertEqual(manager.plugins.myplugin.get_string(), 'test')
        self.assertEqual(manager.plugins.anotherplugin.get_value(), 1)
        self.assertEqual(manager.plugins.anotherplugin.get_string(), 'test')

    @attr('plugins')
    def test_PluginsCheckTrue(self):
        """
        Check boolean returned by method
        :return:
        """
        manager = Manager()
        manager.load_plugins()
        self.assertTrue(manager.plugins.myplugin.get_true())
        self.assertTrue(manager.plugins.anotherplugin.get_true())

    @attr('plugins')
    def test_PluginsCheckFalse(self):
        """
        Check boolean returned by method
        :return:
        """
        manager = Manager()
        manager.load_plugins()
        self.assertFalse(manager.plugins.myplugin.get_false())
        self.assertFalse(manager.plugins.anotherplugin.get_false())

    @attr('plugins')
    def test_PluginsCheckNone(self):
        """
        Check None returned by method
        :return:
        """
        manager = Manager()
        manager.load_plugins()
        self.assertIsNone(manager.plugins.myplugin.get_none())
        self.assertIsNone(manager.plugins.anotherplugin.get_none())

    @attr('plugins')
    def test_PluginsCheckException(self):
        """
        Check exception returned by method
        :return:
        """
        manager = Manager()
        manager.load_plugins()
        self.assertRaises(Exception, manager.plugins.myplugin.get_exception())
        self.assertRaises(Exception, manager.plugins.anotherplugin.get_exception())
