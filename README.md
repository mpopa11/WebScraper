# WebScraper Documentation

## Preliminary: Install Required Modules

Before running the scripts, make sure to install the required Python modules by running the following command:

```bash
pip install selenium beautifulsoup4 pandas python-Levenshtein
```
## Scraping Process

To initiate the scraping process, run the `RunScrapers.py` script. This script orchestrates the scraping of data from various vendors, including Emag, Evomag, and PC Garage.

### Execution Flow:

1. **RunScrapers.py Script:**
   - Executes scraping scripts for each vendor.
   - Opens Chrome pages in Incognito mode to fetch HTML content.
   - Parses the HTML to extract product names, specifications, and prices.
   - Saves the collected data in CSV files corresponding to each vendor.

## Search Functionality

Once the databases are created, you can utilize the search functionality by running the `Search.py` script.

### Execution Flow:

1. **Search.py Script:**
   - Prompts the user to input a partial product name.
   - Considers these terms as required for the search.
   - Calculates the average Levenshtein distance for products containing the required terms.
   - Identifies the best match and displays the results.

### Search Results:

- If the product is not found, a corresponding message is shown.
- If the product is found in any database, the script searches for the vendor with the minimum price for the product.
- The details of the best match, including the vendor and price, are displayed in the console.

## Notes:

- The scraping process uses Chrome in Incognito mode to ensure clean sessions.
- The resulting CSV files store product details and prices for each vendor.
- The search functionality helps users find the best-matching product across vendors based on their input.
