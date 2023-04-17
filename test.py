import argparse
import os
from time import sleep

import requests
from selenium.webdriver import Chrome, ChromeOptions
from selenium.webdriver.common.by import By


class WebsiteImgDownloader:
    def __init__(self):
        arg_parser = argparse.ArgumentParser()
        arg_parser.add_argument("--url", default="https://24h.pchome.com.tw/store/DSAR0S", help="Target website url")
        arg_parser.add_argument("--format", "-f", default=None, help="Target image format, or no constraint by default")
        arg_parser.add_argument("--output", "-o", default="output", help="Output image directory path")

        self.args = arg_parser.parse_args()
        self.url = self.args.url
        self.img_format = self.args.format
        self.output_path = self.args.output

        os.makedirs(self.output_path, exist_ok=True)

        options = ChromeOptions()
        options.add_argument("--window-size=1920,1080")
        self.driver = Chrome(chrome_options=options)
        self.driver.get(url=self.url)

    def download(self):
        file_names = []
        while True:
            file_names += [name for name in self.download_page_img()]
            button_next_page = self.driver.find_elements(by=By.CSS_SELECTOR, value="div#PaginationContainer li")[-1]
            if button_next_page.get_attribute("class") != "sp":
                break

            button_next_page.click()
            sleep(2)

        return file_names;

    def download_page_img(self):
        for img_element in self.driver.find_elements(by=By.CSS_SELECTOR, value="img"):
            img_url = img_element.get_property("src") or None
            if img_url:
                img_name = img_url.split("/")[-1]
                if (self.img_format is None) or (img_name.split(".")[-1] == self.img_format):
                    img_data = requests.get(img_url)
                    with open(f"{self.output_path}/{img_name}", "wb") as f:
                        f.write(img_data.content)
                        yield img_name


if __name__ == '__main__':
    downloader = WebsiteImgDownloader()
    img_names = downloader.download()
    print(img_names)
