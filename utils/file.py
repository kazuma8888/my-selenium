class FileExist:
    def __init__(self, path):
        self.__path = path

    def __call__(self, driver):
        if os.path.isfile(self.__path):
            return driver
        else:
            return False