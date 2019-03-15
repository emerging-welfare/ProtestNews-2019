from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import os
import sys
import pandas as pd

browser = webdriver.PhantomJS("/usr/local/bin/phantomjs")
browser.set_page_load_timeout(30)

filename = sys.argv[1]

urls = pd.read_json(filename, orient="records", lines=True)["url"].unique().tolist()
for url in urls:

    if "scmp" not in url:
        continue

    print(url)
    outfile = url.replace("/", "_")
    outfile = outfile.replace(":", "_")
    outfile = "tmp/htmls/" + outfile
    if os.path.isfile(outfile):
        continue

    try:
        browser.get(url)
    except TimeoutException:
        # print("Couln't load page : " + url)
        continue

    delay = 5 # seconds
    try:
        myElem = WebDriverWait(browser, delay).until(EC.staleness_of(browser.find_element_by_tag_name("html")))
        # print("Page is ready!")
    except TimeoutException:
        # print("Loading took too much time!")
        pass

    with open(outfile, "w", encoding="utf-8") as f:
        f.write(browser.page_source)
