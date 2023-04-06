from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromiumService
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.core.utils import ChromeType
from time import sleep

def init_webdriver():
    options = Options()
    options.add_experimental_option("detach", True)
    options.add_argument("--disable-notifications")
    service = ChromiumService(ChromeDriverManager(chrome_type=ChromeType.CHROMIUM).install())
    driver = webdriver.Chrome(
        service=service,
        options=options
    )
    return driver

def load_images(driver):
    height = int(driver.execute_script("return document.body.scrollHeight"))
    for i in range(1, height, 3):
        driver.execute_script(f"window.scrollTo(0, {i});")
    sleep(2)
    driver.execute_script("window.scrollTo(0, 0)")

def dark_mode(driver):
    dropdown_button = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//button[@id='USER_DROPDOWN_ID']"))
    )
    dropdown_button.click()
    dark_mode_button = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//button[@class='_2KotRmn9DgdA58Ikji2mnV _1zZ3VDhRC38fXLLvVCHOwK']"))
    )
    dark_mode_button.click()
    dropdown_button.click()

def enforce_theme(driver, url):
    run = True
    while run:
        driver.get(url)
        html_tag = driver.find_element(By.TAG_NAME, "html")
        theme = html_tag.get_attribute("class")
        if "theme-light" in theme:
            run = False
        else:
            driver.quit()
            sleep(2)

def expand_comment(comment_element):
    comment_body = comment_element.find_elements(By.TAG_NAME, "p")
    if not comment_body:
        expand_button = WebDriverWait(comment_element, 10).until(
            EC.visibility_of_element_located((By.CLASS_NAME, "icon-expand"))
        )
        expand_button.click()

def take_screenshots(subreddit, submission_id, comments_id):
    driver = init_webdriver()
    url = f"https://www.reddit.com/r/{subreddit}/comments/{submission_id}"
    enforce_theme(driver, url)
    dark_mode(driver)
    load_images(driver)

    submission_element = driver.find_element(By.ID, f"t3_{submission_id}")
    submission_element.screenshot("media/screenshots/title.png")
    
    for id in comments_id:
        comment_element = driver.find_element(By.ID, f"t1_{id}")
        expand_comment(comment_element)
        comment_element.screenshot(f"media/screenshots/{id}.png")
    
    driver.quit()