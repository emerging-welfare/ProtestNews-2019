#!/usr/bin/env python3

import sys
import requests
from lxml import html
from urllib.parse import urlparse


def is_scmp_url(original_url):
    """
    Checks whether given url is a scmp url
    """
    url = urlparse(original_url)
    return 'scmp' in url.netloc


def convert(original_url):
    """
    Converts the given scmp url by fetching the site and getting the amphtml link
    """
    try:
        res = requests.get(original_url)
        tree = html.fromstring(res.content)
        if tree is None:
            raise Exception()
        amp_link = tree.xpath('//link[@rel="amphtml"]/@href')
        if amp_link == None or len(amp_link) < 1:
            raise Exception()
        return amp_link[0]
    except Exception as _:
        return convert_fallback(original_url)
    


def convert_fallback(original_url):
    """
    Fallback for converter that uses the amphtml link, this one directly changes www -> amp
    """
    url = urlparse(original_url)
    netloc = url.netloc.replace('www', 'amp')
    url = url._replace(netloc=netloc)
    return url.geturl()


def main(argc, argv):
    if argc < 2:
        print("This script required the original url for the file")
        print("Usage: ./convert_scmp_url.py input_scmp_url")
        return
    url = argv[1]
    if not is_scmp_url(url):
        print("Incorrect url!")
        return
    print(convert(url))


if __name__ == "__main__":
    main(len(sys.argv), sys.argv)
