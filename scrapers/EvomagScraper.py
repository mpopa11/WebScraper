import re
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time

def Scraper(url):
    if url == "https://www.evomag.ro/portabile-laptopuri-notebook/filtru/pagina:42":
        # Return early to avoid errors when 'browser' is not defined
        return False

    options = webdriver.ChromeOptions()
    options.add_argument('--incognito')
    browser = webdriver.Chrome(options=options)
    browser.get(url)

    # Wait for the articles to be present on the page
    try:
        WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'nice_product_container'))
        )
    except Exception as e:
        print(f"Error: {e}")
        browser.quit()
        return False

    soup = BeautifulSoup(browser.page_source, 'html.parser')
    browser.quit()

    articles = soup.find_all('div', class_='nice_product_item')
    file = open("Evomag_database.csv", "a", encoding='utf-8')
    for article in articles:
        try:
            title_element = article.find('div', class_='npi_name').h2.a.text
            price_element = article.find('span', class_='real_price').text

            # Remove extra spaces and newline characters from title and price
            title = re.sub(r'\s+', ' ', title_element).strip()
            title = title.replace(',', '')  # Remove commas
            price = re.sub(r'\s+', ' ', price_element).strip()

            # Remove " Lei" and format the price
            price = float(price.replace(' Lei', '').replace('.', '').replace(',', '.'))

            file.write(f"{title},{price}\n")
        except Exception as e:
            print(f"Error: {e}")
            continue

    return True

def scrape():
    base_url = "https://www.evomag.ro/portabile-laptopuri-notebook/"
    
    flag = True
    i = 1
    file = open("Evomag_database.csv", "w", encoding='utf-8')
    file.close()
    while flag:
        url = f"{base_url}filtru/pagina:{i}"
        i += 1
        flag = Scraper(url)


if __name__ == "__main__":
    scrape()