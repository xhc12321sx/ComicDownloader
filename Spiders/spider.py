import time
import urllib
from bs4 import BeautifulSoup
import lxml
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
import os
import re


class spider(object):
    def __init__(self, headless=True, dtLoadPicture=True, disableGPU=True):
        self.chrome_option = webdriver.ChromeOptions()

        if dtLoadPicture == True:
            prefs = {"profile.managed_default_content_settings.images":2}
            self.chrome_option.add_experimental_option("prefs",prefs)
        if headless == True:
            self.chrome_option.add_argument("--headless")
        if disableGPU == True:
            self.chrome_option.add_argument("--disable-gpu")

        self.chrome_option.add_argument('user-agent="Mozilla/5.0(X11; U; Linux i686) Gecko/20071127 Firefox/2.0.0.11"')

        self.browser = None

        self.start_browser()

    def boot_up_browser(self):
        self.browser = webdriver.Chrome(options=self.chrome_option)
        self.browser.implicitly_wait(10)

    def start_browser(self):
        self.boot_up_browser()
        pass

    def get_url(self, url):
        pass

    def img_tag(self):
        pass

    def dowoload(self):
        pass


class TencentComicSpider(spider):
    def start_browser(self):
        print("Tencent Spider v 1.0")
        self.boot_up_browser()

    def get_url(self, url):
        print("Getting url...")
        self.browser.get(url)
        soup = BeautifulSoup(self.browser.page_source, "lxml")
        try:
            name = soup.find("span", attrs={"class":"title-comicHeading"}).contents[0]
        except:
            print("Access denied. Accessing from a banned ip")
            return -1

        self.browser.find_element_by_id("crossPage").click()

        soup = BeautifulSoup(self.browser.page_source, "lxml")
        imgs = soup.find_all(self.img_tag)
        # imgs contains urls for imgs

        print("Getting imgs...")
        urls = []
        for img in imgs:
            try:
                urls.append(img.attrs["data-src"])
            except:
                urls.append(img.attrs["src"])
        urls.reverse()

        self.dowoload(name, urls)

    @staticmethod
    def dowoload(name, urls):
        print("Creating ./download/{0}...".format(name))
        if not os.path.exists("./download/"+name):
            os.mkdir("./download/"+name)

        # print(urls)
        
        print("  Totally {0} images".format(len(urls)))
        for i in range(len(urls)):
            print("    Img {0}/{1}".format(i+1, len(urls)))
            file_name = str(i+1)
            if len(file_name) == 1:
                file_name = "0" + file_name
            file_name = file_name + ".jpg" 
            if not os.path.exists("./download/"+name+"/"+file_name):
                print("      Downloading...")
                urllib.request.urlretrieve(urls[i], "./download/"+name+"/"+file_name)
            else:
                print("      File exists")
        pass

    @staticmethod
    def img_tag(tag):
        return tag.name == "img" and tag.has_attr("data-h") and not tag.has_attr("class")

if __name__ == "__main__":
    a = TencentComicSpider()
    pass