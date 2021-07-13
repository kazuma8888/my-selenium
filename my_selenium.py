import os
import time
from datetime import date

import selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities




class MySelenium():
    """
    Seleniumを自分が使いやすいようにしたラッパー
    使うときはこのクラスを継承して使うことを想定している。
    """
    def __init__(self):
        """
        webdriverの初期設定を行う
        別コンテナと通信してスクレイピングを行っている
        """
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')
        download_folder = os.path.abspath(os.path.join(os.path.dirname(__file__), 'download_folder'))
        options.add_experimental_option('prefs', {'download.default_directory': download_folder})
        self.driver = webdriver.Remote(
            command_executor=os.environ["SELENIUM_URL"],
            desired_capabilities=DesiredCapabilities.FIREFOX.copy(),
            options = options
        )
        self.wait = WebDriverWait(self.driver, 120)

    def click(self, css_selector, element=True, location=False):
        if element:
            self.wait.until(ec.element_to_be_clickable((By.CSS_SELECTOR, css_selector)))
            try:
                self.driver.find_element_by_css_selector(css_selector).click()
            except:
                print('Cannot click this element')
        if location:
            self.wait.until(ec.presence_of_all_elements_located)
            elements = self.driver.find_element_by_css_selector(css_selector)
            loc = elements.location
            x, y = loc['x'], loc['y']
            actions = ActionChains(self.driver)
            actions.move_by_offset(x, y)
            actions.click()
            actions.perform()

    def xpath_click(self, x_path):
        self.wait.until(ec.element_to_be_clickable((By.XPATH, x_path)))
        print(x_path)
        try:
            self.driver.find_element_by_xpath(x_path).click()
        except:
            assert False, 'cannot'
        
    def special_click(self, css_selector ):
        self.wait.until(ec.presence_of_all_elements_located)
        try:
            self.driver.find_element_by_css_selector(css_selector).click()
        except:
            elements = self.driver.find_element_by_css_selector(css_selector)
            loc = elements.location
            x, y = loc['x'], loc['y']
            try:
                actions = ActionChains(self.driver)
                actions.move_by_offset(x, y)
                actions.click()
                actions.perform()
            except:
                
                inputLabel=self.driver.find_element_by_css_selector(css_selector)
                self.driver.execute_script("arguments[0].scrollIntoView();", inputLabel)
                loc = elements.location
                x, y = loc['x'], loc['y']
                actions = ActionChains(self.driver)
                actions.move_by_offset(x, y)
                actions.click()
                actions.perform()
                

        
    def send_keys(self, css_selector, value):
        self.wait.until(ec.visibility_of_element_located((By.CSS_SELECTOR, css_selector)))
        self.driver.find_element_by_css_selector(css_selector).clear()
        self.driver.find_element_by_css_selector(css_selector).send_keys(value)
    
    def get_contents(self, css_selector):
        contents = self.driver.find_element_by_css_selector(css_selector).text
        return contents
    
    def quit_driver(self):
        """
        最後に必ず呼び出すようにする
        """
        self.driver.quit()