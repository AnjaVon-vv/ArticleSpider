# -*- coding: utf-8 -*-
__author__ = "Von"

import hashlib

def get_md5(url):
    # 注意报错，unicode→utf-8
    if isinstance(url, str):
        url = url.encode("utf-8")
    m = hashlib.md5()
    m.update(url)
    return m.hexdigest()