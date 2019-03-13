import scrapy
from scrapy.utils.log import configure_logging
import logging
import pandas as pd

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

        urls = pd.read_json(self.filename, orient="records", lines=True)["url"].unique().tolist()
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):

        outfile = response.url.replace("/", "_")
        outfile = outfile.replace(":", "_")

        with open("tmp/htmls/%s" %outfile , 'wb') as f:
            f.write(response.body)
