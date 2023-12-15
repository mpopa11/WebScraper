from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time
import csv
import os

def clean_value(value):
    if value is not None:
        cleaned_value = str(value).replace(',', '').replace('(', '').replace(')', '').replace('"', '').replace('®', '').replace('™', '')
        return cleaned_value
    else:
        return ''

# Function to write in a CSV file
def write_to_csv(product, filename='PCGarage_database.csv'):
    file_exists = os.path.exists(filename)

    with open(filename, 'a', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        
        specs = clean_value(product.get("specs", ""))
        price = product["price"].replace(".", "").replace(",", ".").replace(" RON", "")
        writer.writerow([specs, price])

def extract_parameters(product_description):
    parameters = {}

    start_index = product_description.find("Ultrabook ") + len("Ultrabook ")
    end_index = product_description.find(" ", start_index)
    if product_description[end_index + 1] == "G":
        end_index = product_description.find(" ", end_index + 1)
    brand = product_description[start_index:end_index].strip()

    start_index = end_index + 2
    end_index = product_description.find(" ", start_index)
    screen_size = product_description[start_index:end_index].strip()

    start_index = end_index + 1
    end_index = product_description.find(",", start_index)
    model = product_description[start_index:end_index].strip()

    start_index = end_index + 2
    end_index = product_description.find(",", start_index)
    display = product_description[start_index:end_index].strip()

    start_index = product_description.find("Procesor") + len("Procesor")
    end_index = product_description.find(")", start_index)
    processor = product_description[start_index:end_index].strip()

    start_index = end_index + 2
    end_index = product_description.find(",", start_index)
    ram = product_description[start_index:end_index].strip()

    start_index = end_index + 2
    end_index = product_description.find(",", start_index)
    storage = product_description[start_index:end_index].strip()

    start_index = end_index + 2
    end_index = product_description.find(",", start_index)
    graphics = product_description[start_index:end_index].strip()

    start_index = end_index + 2
    end_index = min(product_description.find(",", start_index), product_description.find("\n", start_index))
    operating_system = product_description[start_index:end_index].strip()

    # Concatenate parameters into a single string
    parameters["specs"] = f"{brand} {screen_size} {model} {display} {processor} {ram} {storage} {graphics} {operating_system}"

    return parameters

def scrape():
    options = Options()
    options.add_argument("--incognito")

    driver = webdriver.Chrome(keep_alive=True, options=options) 

    driver.get("https://www.pcgarage.ro/ultrabook/")
        
    time.sleep(1)


    # Loop through the elements and write to CSV
    for product_box, price_element in zip(driver.find_elements(By.CLASS_NAME, 'product_box'), driver.find_elements(By.CLASS_NAME, "price")):
        result = extract_parameters(product_box.text)
        result["price"] = price_element.text
        write_to_csv(result)

    driver.quit()

    for i in range(2, 26):
        options = Options()
        options.add_argument("--incognito")

        driver = webdriver.Chrome(keep_alive=True, options=options)

        driver.get(f"https://www.pcgarage.ro/ultrabook/pagina{i}/")
        
        time.sleep(1)
        
        # Loop through the elements and write to CSV
        for product_box, price_element in zip(driver.find_elements(By.CLASS_NAME, 'product_box'), driver.find_elements(By.CLASS_NAME, "price")):
            result = extract_parameters(product_box.text)
            result["price"] = price_element.text
            write_to_csv(result)
        
        driver.quit()

    time.sleep(10)

if __name__ == "__main__":
    scrape()