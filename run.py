import yaml

from utils.example import Example

with open("settings.yml", "r") as yml:
    config = yaml.safe_load(yml)

CHROEMDRIVER_PATH = config["chromedriver_path"]
REMOTE_SELENIUM = config["remote_selenium"]
HEADLESS = config["headless"]


def run():
    example = Example(
        chromedriver_path=CHROEMDRIVER_PATH,
        remote=REMOTE_SELENIUM,
        headless=HEADLESS
    )
    example.login()
    example.move()


if __name__ == "__main__":
    run()
