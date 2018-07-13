import os
import sys
import threading
import time

#
# time of it start
#
_startTime = time.time()


def getLogStarTime():
    return _startTime


#
# If you don't want threading information in the log, set this to zero
#

logThreads = True
#
# If you don't want multiprocessing information in the log, set this to zero
#
logMultiprocessing = True
#
# If you don't want process information in the log, set this to zero
#
logProcesses = True

# -----------------------------------
# thread lock
# -----------------------------------
if threading:
    _lock = threading.RLock()
else:
    _lock = None


def log_acquireLock():
    if _lock:
        _lock.acquire()


def log_releaseLock():
    if _lock:
        _lock.release()


CRITICAL = 50
FATAL = CRITICAL
ERROR = 40
WARNING = 30
WARN = WARNING
INFO = 20
DEBUG = 10
NOTSET = 0

_levelToName = {
    CRITICAL: 'CRITICAL',
    ERROR: 'ERROR',
    WARNING: 'WARNING',
    INFO: 'INFO',
    DEBUG: 'DEBUG',
    NOTSET: 'NOTSET',
}

_nameToLevel = {
    'CRITICAL': CRITICAL,
    'FATAL': FATAL,
    'ERROR': ERROR,
    'WARN': WARNING,
    'WARNING': WARNING,
    'INFO': INFO,
    'DEBUG': DEBUG,
    'NOTSET': NOTSET,
}


def getLevelName(level):
    result = _levelToName.get(level)
    if result is not None:
        return result
    result = _nameToLevel.get(level)
    if result is not None:
        return result
    return "Level %s" % level


def checkLevel(level):
    if isinstance(level, int):
        rv = level
    elif str(level) == level:
        if level not in _nameToLevel:
            raise TypeError('Unknown level %s' % level)
        rv = _nameToLevel[level]
    else:
        raise TypeError('level is not str or int')
    return rv


def addLevelName(level, levelName):
    log_acquireLock()
    try:
        _levelToName[level] = levelName
        _nameToLevel[levelName] = level
    finally:
        log_releaseLock()


if hasattr(sys, '_getframe'):
    currentframe = lambda: sys._getframe(3)
else:
    def currentframe():
        try:
            raise Exception
        except Exception:
            return sys.exc_info()[2].tb_frame.f_back

_srcfile = os.path.normcase(addLevelName.__code__.co_filename)


def getSrcFile():
    return _srcfile


_loggerClass = Logxr


# ---------------------------------------------------------------------------
# Utility functions at module level.
# Basically delegate everything to the root logger.
# ---------------------------------------------------------------------------

def getLogUtil(name=None):
    if name:
        return
