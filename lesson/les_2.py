import os
import sys
import time

import requests

CC_LIST = 'CN IN US ID BR PK NG BD RU JP MX PH VN ET EG DE IR TR CD FR'.split()
BASE_URL = 'http://flupy.org/data/flags'
FILE_DIR = 'downloads/'


def get_flag(arg):
    url = '{}/{arg}/{arg}.gif'.format(BASE_URL, arg=arg.lower())
    resp = requests.get(url)
    return resp.content


def show(arg):
    print(arg, end='')
    sys.stdout.flush()


def save_flag(img, filename):
    path = os.path.join(FILE_DIR, filename)
    print('path -- > {}'.format(path))
    with open(path, 'wb') as f:
        f.write(img)


def download_many(args):
    for arg in sorted(args):
        img = get_flag(arg)
        show(arg)
        save_flag(img, arg.lower() + '.gif')


def main_it(download):
    start = time.time()
    count = download(CC_LIST)
    t = time.time() - start
    print('{} download in {:.2f}s'.format(count, t))


if __name__ == "__main__":
    main_it(download_many)
