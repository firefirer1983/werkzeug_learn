# @Author  : xy.zhang
# @Email   : zhangxuyi@wanshare.com
# @Time    : 18-11-17


# !/usr/bin/python3.6

# -*- coding: utf-8 -*-
import re
import sys

from gunicorn.app.wsgiapp import run


if __name__ == '__main__':
	sys.argv[0] = re.sub(r'(-script\.pyw?|\.exe)?$', '', sys.argv[0])
	sys.exit(run())
