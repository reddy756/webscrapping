from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import pandas as pd
import time

# Automatically manage ChromeDriver
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

# Base URL (search for laptops on Amazon India)
base_url = "https://www.amazon.in/s?k=laptop"

# Lists to store scraped data
product_names = []
prices = []
ratings = []
stock_statuses = []

# Function to parse and extract product data
def parse_page():
    # Get the page source and create BeautifulSoup object
    soup = BeautifulSoup(driver.page_source, "html.parser")

    # Locate each product item in the search result
    products = soup.find_all("div", {"data-component-type": "s-search-result"})

    for product in products:
        # Product Name
        name = product.find("span", class_="a-size-medium a-color-base a-text-normal")
        product_name = name.text.strip() if name else "N/A"

        # Price
        price_whole = product.find("span", class_="a-price-whole")
        price_fraction = product.find("span", class_="a-price-fraction")
        if price_whole and price_fraction:
            price = f"{price_whole.text.strip()}.{price_fraction.text.strip()}"
        else:
            price_whole = product.find("span", class_="a-price")
            price = price_whole.text.strip() if price_whole else "N/A"

        # Rating
        rating = product.find("span", class_="a-icon-alt")
        product_rating = rating.text.strip() if rating else "N/A"

        # Stock Status
        stock_status = "In Stock"  # Assuming availability unless specified otherwise
        availability = product.find("span", class_="a-declarative")
        if availability and "Currently unavailable" in availability.text:
            stock_status = "Out of Stock"


        # Append data to lists
        product_names.append(product_name)
        prices.append(price)
        ratings.append(product_rating)
        stock_statuses.append(stock_status)


# Open Amazon and scrape multiple pages
driver.get(base_url)
time.sleep(3)  # Wait for the page to load

# Define the number of pages to scrape
num_pages = 8

for page in range(1, num_pages + 1):
    print(f"Scraping page {page}...")
    parse_page()

    # Move to the next page if available
    try:
        next_button = driver.find_element(By.XPATH, "//a[contains(@class, 's-pagination-next')]")
        driver.execute_script("arguments[0].scrollIntoView();", next_button)
        next_button.click()
        time.sleep(3)  # Wait for the next page to load
    except Exception as e:
        print("No more pages or unable to navigate.", e)
        break

# Close the browser
driver.quit()

# Save data to CSV
data = {
    "Product Name": product_names,
    "Price": prices,
    "Rating": ratings,
    "Stock Status": stock_statuses
}
df = pd.DataFrame(data)
df.to_csv("amazon_products.csv", index=False)
print("Data has been saved to amazon_products.csv")
