from selenium import webdriver
from selenium.webdriver.chrome.options import Options


def get_web_driver() -> webdriver:
    """Function returns web driver."""
    options = Options()

    prefs = {
        "profile.default_content_setting_values.notifications": 2,
        "profile.managed_default_content_settings.images": 2,
    }
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-infobars")
    options.add_argument("--disable-extensions")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument('--window-size=1024x768')
    options.add_experimental_option("prefs", prefs)

    return webdriver.Chrome(options=options)
