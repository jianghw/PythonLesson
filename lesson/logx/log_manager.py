class PlaceHolder(object):
    def __init__(self, aloger):
        self.loggerMap = {aloger: None}

    def append(self, aloger):
        if aloger not in self.loggerMap:
            self.loggerMap[aloger] = None


class Manager(object):

    def __init__(self, rootnode):
        self.root = rootnode
        self.disable = 0
        self.emittedNoHandlerWarning = False
        self.logRecordFactory = None
        self.logClass = None
        self.logDict = {}

    def getLogger(self, name):
        rv = None
        if not isinstance(name, str):
            raise TypeError('logger name must str')
        if name in self.logDict:
            rv = self.logDict[name]
            if isinstance(rv, PlaceHolder):
                ph = rv
                rv = (self.logClass)(name)
                rv.manager = self
                self.logDict[name] = rv
                self._fixupChildren = (ph, rv)
                self._fixupParents(rv)

    def setLoggerClass(self):
        pass

    def getLoggerFactory(self):
        pass

    def _fixupChildren(self, ph, aloger):
        name = aloger.name
        namelen = len(name)
