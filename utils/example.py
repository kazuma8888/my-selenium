from typing import Union

from utils.my_selenium import MySelenium


class Example(MySelenium):
    def __init__(
        self,
        chromedriver_path: str = "./chromedriver",
        download_folder: Union[str, None] = None,
        headless: bool = True,
        remote: bool = True,
    ) -> None:
        """
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
        super().__init__(chromedriver_path, download_folder, headless, remote)

    def login(self):
        pass

    def move(self):
        pass
