from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait,Select
from selenium.webdriver.support import  expected_conditions as EC
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import requests
import os

# Top_products = []

def download_image(image_url, save_path):

    try:
        response = requests.get(image_url, timeout=10)
        response.raise_for_status()  # Raise an error for bad status
        with open(save_path, "wb") as f:
            f.write(response.content)
        print(f"Image saved to: {os.path.abspath(save_path)}")
        return True
    except Exception as e:
        print(f"Error downloading image: {e}")
        return False

# options = Options()
# options.add_argument("--headless")
# # options.add_argument("--disable-blink-features=AutomationControlled")
# driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
# driver.get("https://www.amazon.in/gp/bestsellers/beauty")

# time.sleep(3)  


# elements = driver.find_elements(By.ID, "gridItemRoot")


# for ele in elements[:5]:

    
#     title = ele.text
#     # print(title)

#     # anchor = driver.find_element(By.CSS_SELECTOR, "a.a-link-normal.aok-block")
#     anchor=ele.find_element(By.CSS_SELECTOR,"a.a-link-normal.aok-block")
#     href = anchor.get_attribute("href")
#     # print(href)

#     img = ele.find_element(By.TAG_NAME, "img")
#     img_src = img.get_attribute("src")
#     path = img_src[-36:]
#     download_image(img_src,save_path=path)

#     # print(f'src = {img_src}')
#     # print(f'path ={path}')

#     Top_products.append({

#             "title": title,
#             "link": href,
#             "image": img_src,
#     })

#     print(Top_products)

def get_top_products():

    Top_products = []

    options = Options()
    options.add_argument("--headless")
    # options.add_argument("--disable-blink-features=AutomationControlled")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    driver.get("https://www.amazon.in/gp/bestsellers/beauty")

    time.sleep(3)  


    elements = driver.find_elements(By.ID, "gridItemRoot")

    for ele in elements[:5]:

    
        title = ele.text
        # print(title)

        # anchor = driver.find_element(By.CSS_SELECTOR, "a.a-link-normal.aok-block")
        anchor=ele.find_element(By.CSS_SELECTOR,"a.a-link-normal.aok-block")
        href = anchor.get_attribute("href")
        # print(href)

        img = ele.find_element(By.TAG_NAME, "img")
        img_src = img.get_attribute("src")
        path = img_src[-36:]
        # download_image(img_src,save_path=path)

        # print(f'src = {img_src}')
        # print(f'path ={path}')

        Top_products.append({

                "title": title,
                "link": href,
                "image": img_src,
        })

    return Top_products

Top_product = get_top_products()

print(Top_product)

