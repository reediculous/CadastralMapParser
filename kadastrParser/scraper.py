from selenium import webdriver
from selenium.webdriver.common.by import By
from time import sleep

class KadastrScraper():
    "Selenium-based cadastral map parser"
    is_more_info_clicked = False
    def __init__(self):
        self.browser = webdriver.Chrome()
        self.browser.get("https://публичная-кадастровая-карта.рф/")
        map = self.browser.find_element_by_css_selector("div.entry-content")
        map = map.find_element_by_css_selector("iframe")
        self.browser.switch_to_frame(map)

    def get_data(self, id):
        '''

        :param id: cadastral plot number
        :return: full address and coordinates of cadastral plot
        '''
        try:
            input = self.browser.find_element_by_css_selector("input.form-control")
            input.send_keys(id)
            btn = self.browser.find_element_by_id("button_kadSearch")
            btn.click()
            sleep(1)
            panel = self.browser.find_element_by_css_selector("div.main-kad-block")
            block = panel.find_element_by_id("main_info_block")
            form = block.find_element_by_id("map_order_form")
            block_content = form.find_element_by_css_selector("div.main_info_block-content")
            info = block_content.find_elements(By.CLASS_NAME, "info__info-item")
            a = ""
            for item in info:
                header = item.find_element_by_css_selector("strong.info__info-item-header")
                if header.text == "Земельный участок по адресу:":
                    a = item.find_element_by_css_selector("a.info__info-item-text").text
            if not self.is_more_info_clicked:
                block_content.find_element_by_class_name("more-info__show").click()
                self.is_more_info_clicked = True
            block_more_content = block_content.find_element_by_class_name("more-info__info")
            more_info = block_content.find_elements(By.CLASS_NAME, "more-info__info-item")
            c = "-1"
            sleep(1)
            for item in more_info:
                header = item.find_element_by_css_selector("strong.more-info__info-item-header")
                if header.text == "Координаты:":
                    c = item.find_element_by_css_selector("a.more-info__info-item-text").text
            input.clear()
            return a, c
        except Exception:
            return "Не нашел :(", ""

    def refresh(self):
        self.browser.refresh()

    def close(self):
        self.browser.close()
