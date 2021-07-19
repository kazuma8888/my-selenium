import os
import time
from datetime import date
from typing import Union

import selenium
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait


class MySelenium:
    """
    Seleniumを自分が使いやすいようにしたラッパー
    使うときはこのクラスを継承して使うことを想定している。
    # TODO : デバッグ用の機能をつける!
    """

    def __init__(
        self,
        chromedriver_path: str = "./chromedriver",
        download_folder: Union[str, None] = None,
        headless: bool = True,
        remote: bool = True,
    ) -> None:
        """
        webdriverの初期設定を行う
        Parameters
        ----------
        chromedriver_path : str
            chromedriverまでのパス
            remote = Trueのときは関係ない
        download_folder : str
            白紙答案のpdfがダウンロードしてあるパス
        headless : bool
            headlessモードにするかどうか
        remote : bool
            ブラウザをリモートで動かすかどうか
        """
        options = webdriver.ChromeOptions()
        if headless:
            options.add_argument("--headless")
        options.add_argument("--no-sandbox")
        # ダウンロード先の設定
        # TODO: ダウンロードがリモート先になってしまうので、ホストにダウンロードできるように改良したい。マウントとか使える?
        self.download_folder = download_folder
        if self.download_folder:
            options.add_experimental_option(
                "prefs", {"download.default_directory": self.download_folder}
            )

        # リモートで別コンテナ上のブラウザを起動
        if remote:
            self.driver = webdriver.Remote(
                command_executor=os.environ["SELENIUM_URL"],
                desired_capabilities=DesiredCapabilities.FIREFOX.copy(),
                options=options,
            )
        # ホストでブラウザを起動
        else:
            options.binary_location = "/usr/bin/chromium-browser"
            self.driver = webdriver.Chrome(
                executable_path=chromedriver_path, options=options
            )
        self.driver.file_detector = LocalFileDetector()
        self.wait = WebDriverWait(self.driver, 2000)

    def css_click(self, css_selector: str) -> None:
        """
        cssセレクタで要素を指定してクリックする
        Parameters
        ----------
        css_selector : str
            クリックしたい要素のCSSセレクタ
        """
        try:
            self.wait.until(ec.element_to_be_clickable((By.CSS_SELECTOR, css_selector)))
            self.driver.find_element_by_css_selector(css_selector).click()
        except:
            assert False, f"Cannot click this element : {css_selector}"

    def xpath_click(self, x_path: str) -> None:
        """
        x_pathで要素を指定してクリックする
        Parameters
        ----------
        x_path: str
            クリックしたい要素のx_path
        """
        try:
            self.wait.until(ec.element_to_be_clickable((By.XPATH, x_path)))
            self.driver.find_element_by_xpath(x_path).click()
        except:
            assert False, f"Cannot click this element : {x_path}"

    def location_click(self, xpath_to_location: str) -> None:
        """
        x_pathで要素を指定してその位置をクリックする
        Parameters
        ----------
        xpath_to_location: str
            クリックしたい位置にある要素のx_path
        """
        self.wait.until(ec.presence_of_all_elements_located)
        elements = self.driver.find_element_by_xpath(xpath_to_location)
        loc = elements.location
        x, y = loc["x"], loc["y"]
        actions = ActionChains(self.driver)
        actions.move_by_offset(x, y)
        actions.click()
        actions.perform()

    def send_keys(self, css_selector: str, value: str) -> None:
        """
        値を入力する
        Parameters
        ----------
        css_selector: str
            入力ボックスのCSS_SELECTOR
        value: str
            入力したい値
        """
        self.wait.until(
            ec.visibility_of_element_located((By.CSS_SELECTOR, css_selector))
        )
        self.driver.find_element_by_css_selector(css_selector).clear()
        self.driver.find_element_by_css_selector(css_selector).send_keys(value)
