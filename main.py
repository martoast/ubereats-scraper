from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException

import time
import csv
import os
import argparse
import re

# Create the output folder if it doesn't exist
if not os.path.exists("output"):
    os.makedirs("output")

parser = argparse.ArgumentParser(description="Search uber eats by location")
parser.add_argument("--location", "--l", "-l", "-location", type=str, nargs="+")

args = parser.parse_args()


location_args = args.location
location = " ".join(location_args)


csv_urls_filename = f"output/pizzas_sandiego.csv"

csv_filename = "output/data.csv"


# Set up the Chrome browser driver
driver = webdriver.Chrome()


# Navigate to the search page
url = "https://www.ubereats.com/mx-en/search"
driver.get(url)

# Wait for the search box to load
try:
    search_box = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "location-typeahead-home-input"))
    )

    # Type the search query and press Enter
    search_location = f"{location}"
    search_box.send_keys(search_location)
    search_box.send_keys(Keys.RETURN)

    time.sleep(5)

    search_result = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "location-typeahead-home-item-0"))
    )

    search_result.click()

    time.sleep(5)


except:
    print(f"error searching for page")


try:
    with open(csv_urls_filename, "r") as csvfile:
        urls = csv.reader(csvfile)
        with open(csv_filename, "w", newline="", encoding="utf-8") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(
                [
                    "name",
                    "cuisine_type",
                    "rating",
                    "reviews",
                    "price_band",
                    "url",
                    "menu_items"
                ]
            )
            for row in urls:
                url = row[0]
                if url and isinstance(url, str):
                    driver.get(url)

                    time.sleep(3)

                    try:
                        name = (
                            WebDriverWait(driver, 2)
                            .until(EC.presence_of_element_located((By.CSS_SELECTOR, "h1[data-testid='store-title-summary']")))
                            .text
                        )

                    except Exception as e:
                        print("no name found")
                        name = ""

                    try:
                        business_info = (
                            WebDriverWait(driver, 2)
                            .until(EC.presence_of_element_located((By.XPATH, "//*[@id='main-content']/div[3]/div/div[1]/div[2]/div/div[1]/div")))
                            .text
                        )

                        info_list = business_info.split("•")

                        if len(info_list) == 3:
                            cuisine_type = info_list[1].strip()
                            price_band = info_list[2].strip()
                        else:
                            price_band = info_list[1].strip()
                            cuisine_type = ""


                        if price_band == "$":
                            price_band = "$30 and under"
                        elif price_band == "$$":
                            price_band = "$31 to $50"
                        else:
                            price_band = "$50 and over"

                        
                        rating = re.search(r"\d\.\d", info_list[0]).group()
                        reviews = re.search(r"\((\d+).*\)", info_list[0]).group(1)

                    except Exception as e:
                        print("error with business_info")
                        business_info = ""


                    try:
                        menu_items = []
                        # Scrape the menu items
                        menu_items_elements = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.CLASS_NAME, "gx")))
                        
                        # data-test="store-item-

                        if menu_items_elements:
                            for element in menu_items_elements:

                                menu_item = {
                                    "name": "",
                                    "is_popular": False
                                }

                                try:
                                    menu_item["name"] = element.find_element(By.TAG_NAME, "span").text
                                except Exception:
                                    menu_item["name"] = ""
                                
                                try:
                                    popular_tag = element.find_element(By.CLASS_NAME, "jp").text
                                    print(popular_tag)
                                    if popular_tag == "Popular":
                                        print("Popular tag found")
                                        menu_item["is_popular"] = True
                                except NoSuchElementException:
                                    pass

                                if menu_item["name"]:             
                                    menu_items.append(menu_item)
                                                    
                    except Exception as e:
                        print("error with menu items")
                        print(e)

                    if name and cuisine_type and rating and reviews and price_band and len(menu_items):
                        writer = csv.writer(csvfile)
                        writer.writerow([name, cuisine_type,rating, reviews, price_band, url, *menu_items])
                        
                else:
                    print(f"Invalid URL format: {url}")

except Exception as e:
        print("Error getting data")

finally:
    # Close the driver
    driver.quit()
    exit()
