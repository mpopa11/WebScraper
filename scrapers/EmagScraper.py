from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time

def scrape_emag(url):
    options = webdriver.ChromeOptions()
    options.add_argument('--incognito')
    browser = webdriver.Chrome(options=options)
    browser.get(url)

    # Wait for the articles to be present on the page
    try:
        WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'card-item'))
        )
    except Exception as e:
        print(f"Error: {e}")
        browser.quit()
        return False

    current_url = browser.current_url
    if current_url != url and url != "https://www.emag.ro/laptopuri/filter/emag-genius-f9538,livrate-de-emag-v30/p1/c":
        browser.quit()
        return False

    soup = BeautifulSoup(browser.page_source, 'html.parser')
    browser.quit()

    articles = soup.find_all('div', class_='card-item card-standard js-product-data')
    with open("Emag_database.csv", "a", encoding='utf-8') as file:
        for article in articles:
            try:
                title_element = article.get('data-name')
                price_element = article.find('p', class_='product-new-price').text
                # Remove commas followed by a space and replace commas not followed by a space with a space
                title = title_element.replace(', ', ' ').replace(',', '')
                # Remove "de la ", " Lei", and format the price
                price = float(price_element.replace('de la ', '').replace(' Lei', '').replace('.', '').replace(',', '.'))
                file.write(f"{title},{price}\n")
            except Exception as e:
                print(f"Error: {e}")
                continue 
    return True

def scrape():
    base_url = "https://www.emag.ro/laptopuri/filter/emag-genius-f9538,livrate-de-emag-v30/p"
    flag = True
    i = 1
    with open("Emag_Database.csv", "w", encoding='utf-8'):
        pass  # Create an empty file
    while flag:
        url = f"{base_url}{i}/c"
        i += 1
        flag = scrape_emag(url)

if __name__ == "__main__":
    scrape()
