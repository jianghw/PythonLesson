import os
import sys
import threading

import collections
import time

from logx import getLevelName, getLogStarTime, logThreads, logMultiprocessing, logProcesses


class LogRecord(object):
    """
     A LogRecord instance represents an event being logged.
    LogRecord instances are created every time something is logged. They
    contain all the information pertinent to the event being logged. The
    main information passed in is in msg and args, which are combined
    using str(msg) % args to create the message field of the record. The
    record also includes information such as when the record was created,
    the source line where the logging call was made, and any exception
    information to be logged.
    """

    def __init__(self, name, level, pathname, lineno, msg, args, exc_info, func=None, sinfo=None,
                 **kwargs):
        ct = time.time()
        self.name = name
        self.msg = msg
        if args and len(args) == 1 and isinstance(args[0], collections.Mapping) and args[0]:
            args = args[0]
        self.args = args

        self.levelname = getLevelName(level)
        self.levelno = level
        self.pathname = pathname
        try:
            self.filename = os.path.basename(pathname)
            self.module = os.path.splitext(self.filename)[0]
        except(TypeError, ValueError, AttributeError):
            self.filename = pathname
            self.module = 'no such module'
        self.exc_info = exc_info
        self.exc_txt = None
        self.stack_info = sinfo
        self.lineno = lineno
        self.funcname = func
        self.created = ct
        self.msecs = (ct - int(ct)) * 1000
        self.relativeCreate = (self.created - getLogStarTime()) * 1000

        if logThreads and threading:
            self.thread = threading.get_ident()
            self.threadName = threading.current_thread().name
        else:
            self.thread = None
            self.threadName = None

        if not logMultiprocessing:
            self.processName = None
        else:
            self.processName = 'MainProcess'
            mp = sys.modules.get('multiprocessing')
            if mp is not None:
                try:
                    self.processName = mp.current_process().name
                except Exception:
                    pass
        if logProcesses and hasattr(os, 'getpid'):
            self.process = os.getpid()
        else:
            self.process = None

    def __str__(self):
        return '<LogRecord : {},{},{},{},{}>'.format(self.name, self.levelno, self.pathname,
                                                     self.lineno, self.msg)

    def getMessage(self):
        """
        Return the message for this LogRecord after merging any user-supplied arguments with the message.
        """
        msg = str(self.msg)
        if self.args:
            msg = msg % self.args
        return msg
