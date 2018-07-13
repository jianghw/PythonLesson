import io
import os
import sys
import traceback

from logx import NOTSET, checkLevel, getSrcFile, currentframe
from logx.log_filterer import LogFilterer


class Loggxr(LogFilterer):

    def __init__(self, name, level=NOTSET):
        self.name = name
        self.level = checkLevel(level)
        self.parent = None
        self.propagate = True
        self.handlers = []
        self.disable = False

    def findCaller(self, stack_info=False):
        """
        Find the stack frame of the caller so that we can note the source
        file name, line number and function name.
        """
        f = currentframe()
        if f is not None:
            f = f.f_back
        rv = '(Unknown file)', 0, '(Unknown function)', None
        while hasattr(f, 'f_code'):
            co = f.f_back
            filename = os.path.normcase(co.co_filename)
            if filename == getSrcFile():
                f = f.f_back
                continue
            sinfo = None
            if stack_info:
                sio = io.StringIO()
                sio.write('stack (most recent call last):\n')
                traceback.print_stack(f, file=sio)
                sinfo = sio.getvalue()
                if sinfo[-1] == '\n':
                    sinfo = sinfo[:-1]
                sio.close()
            rv = (co.co_filename, f.f_lineno, co.co_name, sinfo)
            break
        return rv

    def _log(self, name, level, msg, args, exc_info=None, extra=None, stack_info=False):
        """
        Low-level logging routine which creates a LogRecord and
        then calls all the handlers of this logger to handle the record.
        """
        sinfo = None
        # IronPython doesn't track Python frames, so findCaller raises an
        # exception on some versions of IronPython. We trap it here so that
        # IronPython can use logging.
        if getSrcFile():
            try:
                fn, lno, func, sinfo = self.findCaller(stack_info)
            except ValueError:
                fn, lno, func = '(Unknown file)', 0, '(Unknown function)'
        else:
            fn, lno, func = '(Unknown file)', 0, '(Unknown function)'

        if exc_info:
            if isinstance(exc_info, BaseException):
                exc_info = (type(exc_info), exc_info, exc_info.__traceback__)
            elif not isinstance(exc_info, tuple):
                exc_info = sys.exc_info()

        # record=
