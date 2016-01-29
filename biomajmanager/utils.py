from __future__ import print_function
import pytz
import os
import sys
from time import time, tzname
from datetime import datetime
# from biomajmanager.manager import Manager

class Utils(object):

    timer_start = timer_stop = 0.0
    show_warn = True
    show_debug = True
    show_verbose = True

    @staticmethod
    def elapsed_time():
        '''
        Get the elapsed time between start and stop timer
        Stop timer call is not required. If not set, it is automatically called
        as soon as thie method is called
        :return: Time
        :rtype: float
        '''
        if Utils.timer_start:
            if not Utils.timer_stop:
                Utils.stop_timer()
            etime = Utils.timer_stop - Utils.timer_start
            Utils.reset_timer()
            return etime
        Utils.error("Missing timer value (start/stop")

    @staticmethod
    def error(msg):
        print('[ERROR] %s' % str(msg), file=sys.stderr)
        sys.exit(1)

    @staticmethod
    def get_files(path=None):
        """
        Return the list of file(s) found for a given path
        :param path: Path to search from
        :type path: String
        :return: List of file(s) found
        :rtype: List
        """
        if not path or not os.path.isdir(path):
            Utils.error("Path not found: %s" % str(path))
        return os.listdir(path)

    @staticmethod
    def get_deepest_dirs(path=None, full=False):
        """
        Get the last directories from a path
        :param path: Path to start from
        :type path: String
        :param full: Get the full path otherwise the directory only
        :type full: Boolean
        :return: List of directories
        :rtype: List
        """
        if path is None:
            Utils.error("Path is required")

        if not os.path.exists(path) and not os.path.isdir(path):
            Utils.error("%s does not exists" % str(path))

        dirs = []
        for dirpath, dirnames, filenames in os.walk(path):
            if len(dirnames) == 0:
                if full:
                    dirs.append(dirpath)
                else:
                    dirs.append(os.path.basename(dirpath))
        return dirs

    @staticmethod
    def get_deepest_dir(path=None, full=False):
        """
        Return only one deepest dir from the path
        :param path: Path
        :type path: String
        :param full: Return complete path
        :type full: Boolean
        :return: Director name
        :rtype: String
        """
        dirs = Utils.get_deepest_dirs(path, full=full)
        if len(dirs) > 1:
            Utils.warn("More than one deepest dir found at %s: Only first returned" % str(path))
        return dirs[0]

    # @staticmethod
    # def local2utc(value):
    #     """
    #     Convert a locatime datetime object to UTC
    #     """
    #     if not isinstance(value, datetime):
    #         Utils.error("datetime object required! %s" % value)
    #     time_zone = tzname[0]
    #     local_time_zone = pytz.timezone(time_zone)
    #     local_date_time = local_time_zone.localize(value)
    #     return local_date_time.astimezone(pytz.UTC)

    @staticmethod
    def ok(msg):
        """
        Print a [OK] msg
        :param msg: Message to print
        :type msg: String
        :return:
        """
        if msg:
            print("[OK] %s" % str(msg))

    @staticmethod
    def reset_timer():
        '''

        :return:
        '''
        Utils.timer_start = 0.0
        Utils.timer_stop = 0.0

    @staticmethod
    def start_timer():
        '''

        :return:
        '''
        Utils.timer_start = time()

    @staticmethod
    def stop_timer():
        '''

        :return:
        '''
        Utils.timer_stop = time()

    @staticmethod
    def time2date(id):
        """
        Convert a timestamp into a datetime object
        :param id: Timestamp to convert
        :return: datetime object
        """
        return datetime.fromtimestamp(id)

    @staticmethod
    def time2datefmt(id, fmt):
        """
        Convert a timestamp into a date following the format fmt
        :param id: Timestamp to convert
        :param fmt: Date format to follow for conversion
        :return: date (String)
        """
        return datetime.fromtimestamp(id).strftime(fmt)

    @staticmethod
    def title(msg):
        '''
        Prints a small title banner (message + underlined message)
        :param msg:
        :return:
        '''
        title = "* " + str(msg) + " *"
        print(title)
        print('-' * len(title))

    @staticmethod
    def user():
        '''
        Return the current user running or using the script. Taken from os.env
        :return: User name
        :rtype: String
        '''
        return os.getenv('USER')

    @staticmethod
    def verbose(msg):
        from .manager import Manager
        if Manager.verbose and Utils.show_verbose:
            print('[VERBOSE] %s' % str(msg), file=sys.stdout)

    @staticmethod
    def warn(msg):
        if Utils.show_warn:
            print('[WARNING] %s' % str(msg), file=sys.stderr)
