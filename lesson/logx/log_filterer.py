class LogFilter(object):
    """
    Filter instances are used to perform arbitrary filtering of LogRecords.
    """

    def __init__(self, name):
        self.name = name
        self.nlen = len(name)

    def filter(self, record):
        if self.nlen == 0:
            return True
        elif self.name == record.name:
            return True
        elif record.name.find(self.name, 0, self.nlen) != 0:
            return False
        else:
            return (record.name[self.nlen] == ".")


class LogFilterer(object):
    """
     A base class for loggers and handlers which allows them to share common code.
     定义个列表 添加 删除 过滤
    """

    def __init__(self):
        self.filters = []

    def addFilter(self, filter):
        if not (filter in self.filters):
            self.filters.append(filter)

    def removeFiler(self, filter):
        if filter in self.filters:
            self.filters.remove(filter)

    def filter(self, recond):
        """
        Determine if a record is loggable by consulting all the filters.

        The default is to allow the record to be logged; any filter can veto
        this and the record is then dropped. Returns a zero value if a record
        is to be dropped, else non-zero.
        """
        rv = True
        for f in self.filters:
            if hasattr(f, 'filter'):
                result = f.filter(recond)
            else:
                result = f(recond)
            if not result:
                rv = False
                break
        return rv
