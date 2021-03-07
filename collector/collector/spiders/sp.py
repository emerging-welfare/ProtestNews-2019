import scrapy
from scrapy.utils.log import configure_logging
import logging
import os
import json
# . is important here, it is a relative import
from .convert_scmp_url import is_scmp_url, convert

class HtmlSpider(scrapy.Spider):
    name = "sp"

    configure_logging(install_root_handler=False)
    logging.basicConfig(
        filename='log.txt',
        format='%(levelname)s: %(message)s',
        level=logging.INFO
    )

    def __init__(self, filename="", **kwargs):
        self.filename = filename
        super().__init__(**kwargs)

    def start_requests(self):
        with open(self.filename, "r", encoding="utf-8") as f:
            lines = f.read().splitlines()

        urls = [json.loads(line)["url"] for line in lines]

        for url in urls:
            outfile = url.replace("/", "_").replace(":", "_")
            outfile = "./tmp/htmls/" + outfile
            if os.path.isfile(outfile): # Already downloaded
                continue

            # TODO: Does this work? If not we can call selenium here
            if is_scmp_url(url):
                url = convert(url)

            yield scrapy.Request(url=url, callback=self.parse, meta={"outfile":outfile})

    def parse(self, response):
        with open(response.meta["outfile"] , 'wb') as f:
            f.write(response.body)
