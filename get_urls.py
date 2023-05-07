from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import StaleElementReferenceException

import time
import csv
import os
import argparse

# Create the output folder if it doesn't exist
if not os.path.exists("output"):
    os.makedirs("output")

parser = argparse.ArgumentParser(description="Search uber eats by location")
parser.add_argument("--query", "-q", "-query", "--q", type=str, nargs="+")
parser.add_argument("--location", "--l", "-l", "-location", type=str, nargs="+")

args = parser.parse_args()

query_args = args.query
query = " ".join(query_args)

location_args = args.location
location = " ".join(location_args)

print(location)
print(query)

# Set the page number to 1
page_num = 1

# Set the maximum number of pages to scrape
max_pages = 10

csv_filename = f"output/urls.csv"

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

    # Enter the query string
    if query:
        print(f"entering query: {query}")
        try:
            url = f"https://www.ubereats.com/mx-en/feed?q={query}"
            driver.get(url)
            time.sleep(5)
        except:
            print(f"Error: failed to search for {query}")

except:
    print(f"error searching for {query}")


try:
     # Store the URLs of the businesses
    with open(csv_filename, "w", newline="", encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile)
        url_set = set()
        while True:
            try:
                # wait for store cards to load
                time.sleep(3)

                # get store cards in feed
                store_cards = WebDriverWait(driver, 20).until(
                    EC.presence_of_all_elements_located(
                        (By.CSS_SELECTOR, "a[data-testid='store-card']")
                    )
                )

                for business in store_cards:
                    try:
                        url = business.get_attribute("href")
                        if url not in url_set:
                            writer.writerow([url])
                            url_set.add(url)
                    except:
                        print("error getting business url")

                try:
                    show_more_btn = WebDriverWait(driver, 10).until(
                        EC.element_to_be_clickable((By.XPATH, "//button[text()='Show more']"))
                    )
                    driver.execute_script("arguments[0].scrollIntoView();", show_more_btn)
                    show_more_btn.click()
                except StaleElementReferenceException:
                    # If the element becomes stale, wait and try again
                    print("stale element")
                    time.sleep(5)
                    show_more_btn = WebDriverWait(driver, 10).until(
                        EC.element_to_be_clickable((By.XPATH, "//button[text()='Show more']"))
                    )
                    driver.execute_script("arguments[0].scrollIntoView();", show_more_btn)
                    show_more_btn.click()
            except:
                print("Loop completed")
                print(f"Got a total of {len(url_set)} urls")
                break

except Exception as e:
    print("Error:", e)

finally:
    driver.quit()
    exit()
