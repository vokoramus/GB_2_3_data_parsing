from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


s = Service('./chromedriver')
# chrome_options = Options()
# chrome_options.add_argument("--headless")

#
driver = webdriver.Chrome(service=s,
                          # options=chrome_options,
                          # executable_path='C:/chromedriver/chromedriver.exe'
                          )
# driver.implicitly_wait(10)

driver.get('https://5ka.ru/special_offers')

# закрываем окно с предупреждением о куках
button = driver.find_element(By.XPATH, "//span[contains(text(),'Принять')]")
button.click()


while True:
    wait = WebDriverWait(driver, 10)
    button = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "add-more-btn")))
    # button = driver.find_element(By.CLASS_NAME, "add-more-btn")
    button.click()
    # TODO exit from while True


elems = driver.find_elements(By.CLASS_NAME, 'product-card item')
for elem in elems:
    pass









