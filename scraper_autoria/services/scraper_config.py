"""Module store all CSS, XPATH, and CLASS selectors for scraper."""

XPATH_PAGINATION = "//*[@id='pagination']/nav/span[8]/a"
XPATH_PAGINATION_2 = "/html/body/div[8]/section/div[3]/div/div/div[121]/div/nav/span[9]/a"
XPATH_CAR_ODOMETER = "/html/body/div[7]/div[10]/div[4]/aside/section[1]/div[3]"
XPATH_CAR_PHONE_BTN = '//*[@id="phonesBlock"]/div[1]/span/span'
XPATH_CAR_PHONE = "//*[@id='show-phone']/div[2]/div[2]/a"
XPATH_CAR_PHONE_2 = '//*[@id="phonesBlock"]/div/span'
XPATH_CAR_IMAGE_URL = "//*[@id='photosBlock']/div[1]/div[1]/div[1]/picture/source"
XPATH_CAR_IMAGE_URL_2 = "/html/body/div[7]/div[10]/div[4]/main/div[1]/div[2]/div[1]/a[2]/picture/img"
XPATH_CAR_IMG_COUNT = "//*[@id='photosBlock']/div[1]/div[2]/span/span[2]"
XPATH_CAR_VIN = "/html/body/div[7]/div[10]/div[4]/main/div[2]/div[2]/div[1]/dl/dd[1]/div[2]/span[3]"
XPATH_TITLE = "/html/body/div[7]/div[10]/div[4]/main/div[2]/h3"


CLASS_CAR_LINKS = "m-link-ticket"
CLASS_NOTICE_HEAD = "notice_head"
CLASS_CAR_TITLE = "auto-content_title"
CLASS_CAR_PRICE = "price_value"
CLASS_CAR_USERNAME = "seller_info_name"
CLASS_VIN_1 = "vin-code"
CLASS_VIDEO = "ytp-cued-thumbnail-overlay"

CSS_SELECTOR_COOKIES_BUTTON = "#gdpr-notifier > div.c-notifier-container.c-notifier-start > div.c-notifier-btns > label.js-close.c-notifier-btn"
CSS_SELECTOR_CAR_NUMBER = "body > div:nth-child(20) > div.ticket-status-0 > div.auto-wrap > main > div.m-padding > div.vin-checked.mb-15.full > div:nth-child(2) > dl > dd:nth-child(1) > div.t-check > span.state-num.ua"
CSS_SELECTOR_VIN2 = ".label-vin"
CSS_SELECTOR_PHONE_1 = ".popup-successful-call"
CSS_SELECTOR_PHONE_2 = "a.popup-successful-call:nth-child(2)"
CSS_SELECTOR_PHONE_3 = "#show-phone > div.modal-body > div.list-phone > a:nth-child(2)"
CSS_SELECTOR_PHONE_4 = "div.popup-successful-call-desk:nth-child(4)"
CSS_SELECTOR_TITLE = ".auto-content_title"
CSS_SELECTOR_USERNAME = "#userInfoBlockMobile > div:nth-child(1) > span:nth-child(1) > img:nth-child(1)"
CSS_SELECTOR_USERNAME_2 = "#userInfoBlock > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > a:nth-child(1)"
