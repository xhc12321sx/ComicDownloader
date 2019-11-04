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

def img_tag(tag):
    # return tag.name=="li" and not tag.has_attr('class') and tag.has_attr('style')
    return tag.name == "img" and tag.has_attr('src') and re.match(r"https://manhua.qpic.cn", tag.attrs["src"])
    # <img src="https://manhua.qpic.cn/manhua_detail/0/27_15_14_ab3bdc18244b37047f94c9d221e13904_32776.jpg/0" data-pid="32776" data-w="1200" data-h="1752" class="loaded" alt="">
    # <img src="//ac.gtimg.com/media/images/pixel.gif" alt="" data-pid="32784" data-w="1200" data-h="1752">
    # <div style="margin:1px auto 0; width:100px; height:43px; background:transparent url(https://exhentai.org/m/001510/1510427-00.jpg) -0px 0 no-repeat"><a href="https://exhentai.org/s/18e0511c82/1510427-1"><img alt="001" title="Page 1: P000A.jpg" src="https://exhentai.org/img/blank.gif" style="width:100px; height:42px; margin:-1px 0 0 -1px"><br>001</a></div>
    # <img id="img" src="https://ookgnprvpxzeaqywfcbh.hath.network/h/228074c0d23359c0f3fd204362a9ce85c16853fc-240443-1280-550-jpg/keystamp=1572658500-93014ef7c3;fileindex=74442858;xres=1280/P000A.jpg" style="width: 1280px; height: 550px; max-width: 718px; max-height: 309px;" onerror="this.onerror=null; nl('31137-436849')">

if __name__ == "__main__":
    if not os.path.exists("./download"):
        os.mkdir("./download")

    url = "http://www.hanhuazu.cc/comics/detail/11759"
    url = "https://ac.qq.com/ComicView/index/id/505430/cid/977"
    # url = input("URL: ")


    chrome_option = webdriver.ChromeOptions()
    # chrome_option.add_argument("--headless")
    chrome_option.add_argument("--disable-gpu")
    browser = webdriver.Chrome(options=chrome_option)
    browser.implicitly_wait(10)

    if re.search(r"hanhuazu", url):
        print("This is a shuhui url")
        print("Getting url...")
        browser.get(url)
        # time.sleep(5)
        WebDriverWait(browser,10).until(EC.visibility_of_any_elements_located((By.CSS_SELECTOR,'h1')))
        # print(browser.page_source)
        # soup = BeautifulSoup(browser.page_source, "lxml")
        # print(soup.prettify())

        # time.sleep(0.5)
        soup = BeautifulSoup(browser.page_source, "lxml")
        name = soup.find("h1").contents[0]
        print("The name is {0}".format(name))
        # element = browser.find_element_by_css_selector("h1")
        # name = element.text

        print("Into page mode...")
        pattern = re.compile(".?z-page")
        # a = soup.find("span", attrs={"class":pattern})
        # print(soup.prettify())
        while soup.find("span", attrs={"class":pattern}):
            # print(soup.prettify())
            browser.find_element_by_css_selector("span.tips.z-page").click()
            time.sleep(1)
            soup = BeautifulSoup(browser.page_source, "lxml")
        browser.execute_script("window.scrollTo(0,100000)")
        # too slow
        # WebDriverWait(browser,10).until_not(EC.presence_of_all_elements_located((By.CSS_SELECTOR,'span.u-comics-img')))
        time.sleep(1)

        soup = BeautifulSoup(browser.page_source, "lxml")
        # print(soup.prettify())

        print("Getting sources...")
        imgs = soup.find_all("img", attrs={"class":"u-comics-img"})
        if len(imgs)==0:
            print(soup.prettify())
            print("Something went wrong!")
            exit(1)

        print("Creating foulder")
        if not os.path.exists("./download/"+name):
            os.mkdir("./download/"+name)

        print("Start downloading...")
        for img in imgs:
            file_name = img.attrs["alt"]
            file_src = img.attrs["src"]
            if not (re.match(r"00", file_name) or re.match(r"sp", file_name)):
                print("  Downloading {0}".format(file_name))
                urllib.request.urlretrieve(file_src, "./download/"+name+"/"+file_name)

    elif re.search(r"ac.qq.com", url):
        print("This is a Tencent url")
        print("Getting url...")
        browser.get(url)
        soup = BeautifulSoup(browser.page_source, "lxml")
        name = soup.find("span", attrs={"class":"title-comicHeading"}).contents[0]


        browser.execute_script("var q=document.body.scrollTop=10000")
        time.sleep(1)
        soup = BeautifulSoup(browser.page_source, "lxml")
        # print(soup.prettify())
        # comic = soup.find("ul", attrs={"class":"comic-contain"})
        # imgs = soup.find_all("li", attrs={"style":re.compile("width.?")})
        imgs = soup.find_all(img_tag)
        pass
    else:
        print("What the hell is this?")
    pass

