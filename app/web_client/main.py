import os
import time

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

import constants
import settings

os.environ["WDM_SSL_VERIFY"] = "0"


def infinite_loop():
    while True:
        time.sleep(10)


def main() -> None:

    client = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

    if os.path.exists("./example.env"): #and not settings.DEVELOPER:
        # first time launching the application
        client.get(f"{constants.SERVER_URL}/onboarding")
    else:
        client.get(f"{constants.SERVER_URL}/home")

    infinite_loop()


main()
