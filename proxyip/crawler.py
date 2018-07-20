all_funcs = []


def collect_funcs(func):
    """
    装饰器
    """
    all_funcs.append(func)
    return func


class Crawler(object):

    @staticmethod
    def run():
        for func in all_funcs:
            for proxy in func():
                pass

    @staticmethod
    @collect_funcs
    def crawl_66_ip():
        pass


crawler = Crawler()
