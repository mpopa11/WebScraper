import pandas as pd
import Levenshtein as lev
import os

def tokenize_string(s):
    return set(s.lower().split())

def calculate_average_distance(tokenized_input, product_name):
    # Calculate the average Levenshtein distance between the input tokens and the product name
    total_distance = sum(lev.distance(token, product_name.lower()) for token in tokenized_input)
    return total_distance / max(len(tokenized_input), len(product_name))

def search(csv_file, vendor_name, search_term):
    df = pd.read_csv(csv_file, delimiter=',', header=None, names=['Product_Name', 'Price'])

    # Tokenize the input string
    tokenized_input = tokenize_string(search_term)

    required_terms = []

    for term in tokenized_input:
        required_terms.append(term.lower())

    # Ensure that the best match must include the entered terms
    df = df[df['Product_Name'].apply(lambda x: all(term in x.lower() for term in required_terms))]

    if df.empty:
        print(f"No matching products found in {vendor_name}.")
        return None

    # Calculate average Levenshtein distance for each product name
    df['Average_Distance'] = df['Product_Name'].apply(lambda x: calculate_average_distance(tokenized_input, x))

    # Find the row with the minimum average Levenshtein distance (best match)
    best_match = df.loc[df['Average_Distance'].idxmin()]

    best_match = df.loc[df['Average_Distance'].idxmin()].copy()
    best_match['Vendor'] = vendor_name

    print(f"Best match found in {vendor_name}:")
    print(best_match[['Product_Name', 'Price']])
    print("Average Levenshtein Distance:", best_match['Average_Distance'])

    return best_match

def search_in_multiple_databases(database_paths, search_term):
    for path in database_paths:
        if not os.path.exists(path):
            print(f"Error: Database file not found at {path}")
            return

    search_results = []

    for index, path in enumerate(database_paths):
        vendor_name = ""
        if index == 0:
            vendor_name = "Emag"
        elif index == 1:
            vendor_name = "Evomag"
        elif index == 2:
            vendor_name = "PCGarage"

        print(f"\nSearching in {vendor_name}:\n")
        search_result = search(path, vendor_name, search_term)
        if search_result is not None:
            search_results.append(search_result)

    return search_results

def find_lowest_price_vendor(search_results):
    if not search_results:
        print("No results to compare.")
        return

    lowest_price_result = min(search_results, key=lambda x: float(str(x['Price'])))

    # Display the vendor with the lowest price
    print("\nVendor with the lowest price:")
    print(f"Vendor: {lowest_price_result['Vendor']}")
    print(lowest_price_result[['Product_Name', 'Price']])

if __name__ == "__main__":
    database_files = ['Emag_database.csv', 'Evomag_database.csv', 'PCGarage_database.csv']

    search_term = input("Enter the product name or a part of it: ")

    results = search_in_multiple_databases(database_files, search_term)

    find_lowest_price_vendor(results)
