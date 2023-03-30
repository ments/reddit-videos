from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromiumService
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.core.utils import ChromeType
from selenium.webdriver.common.by import By

def init_webdriver():
    options = Options()
    options.add_experimental_option("detach", True)
    service = ChromiumService(ChromeDriverManager(chrome_type=ChromeType.CHROMIUM).install())
    driver = webdriver.Chrome(
        service=service,
        options=options
    )
    return driver

def take_screenshots(submission_id, comments_id):
    driver = init_webdriver()
    url = f"https://www.reddit.com/r/AskReddit/comments/{submission_id}"
    driver.get(url)
    submission_element = driver.find_element(By.ID, f"t3_{submission_id}")
    submission_element.screenshot("title.png")
    for index, id in enumerate(comments_id):
        comment_element = driver.find_element(By.ID, f"t1_{id}")
        comment_element.screenshot(f"comment{index}.png")