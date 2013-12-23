#!/usr/bin/env python
# vim:fileencoding=utf-8
from __future__ import (unicode_literals, division, absolute_import,
                        print_function)

__license__ = 'GPL v3'
__copyright__ = '2013, Kovid Goyal <kovid at kovidgoyal.net>'

from multiprocessing.pool import ThreadPool
from functools import partial

from calibre import detect_ncpus as cpu_count

DEBUG, INFO, WARN, ERROR, CRITICAL = xrange(5)

class BaseError(object):

    HELP = ''
    INDIVIDUAL_FIX = ''
    level = ERROR

    def __init__(self, msg, name, line=None, col=None):
        self.msg, self.line, self.col = msg, line, col
        self.name = name

    def __str__(self):
        return '%s:%s (%s, %s):%s' % (self.__class__.__name__, self.name, self.line, self.col, self.msg)

    __repr__ = __str__

class Worker(object):

    def __init__(self, func):
        self.func = func
        self.result = None
        self.tb = None

def worker(func, args):
    try:
        result = func(*args)
        tb = None
    except:
        result = None
        import traceback
        tb = traceback.format_exc()
    return result, tb

def run_checkers(func, args_list):
    num = cpu_count()
    pool = ThreadPool(num)
    ans = []
    for result, tb in pool.map(partial(worker, func), args_list):
        if tb is not None:
            raise Exception('Failed to run worker: \n%s' % tb)
        ans.extend(result)
    return ans

