# StreetEasy WebScraper
This python script scans the pages of StreetEasy's list of apartments and returns them in a pandas dataframe. This makes it easier to look through all the apartment options in a specific area without having to click through dozens of pages. You can also use this data to do other forms of analysis like average apartment pricing, distribution graph, etc.

# Purpose
Looking for an apartment is a very long and tedious process and StreetEasy definitely make it easier. However, looking through all the apartments in a specific area can be a challenge in itself. For example, there might be 200 apartment listings alone in the Lower East Side and if StreetEasy only shows 10 per page, you're going to have to go through 20 pages. This script helps display all the apartments in a specific neighborhood and their prices without any of the filler information. This list of apartments can be used for lots of different purposes such as data analysis (distributions, averages, price ranking, etc). This data can also be used to help someone looking for an apartment find apartments in his budget in a more digestable format.

# Features
- Uses BeautifulSoup to scan the HTML code that makes up the StreetEasy results page
- Finds all apartments
- Cleans data by removing excess words like "for" and "at" and extracts solely address and price
- Puts list of apartments collected into a Pandas Dataframe
- Displays apartment list

# Packages and Libraries used
- BeautifulSoup4 - https://pypi.org/project/beautifulsoup4/
- Pandas - https://pandas.pydata.org/
- Python built-in libraries: requests, time, datetime, re, random

# Instructions:

1. Choose the neighborhood on StreetEasy
2. Run the code
3. Enter the neighborhood into the console when prompted
4. Get output of apartment listings

# Code Explanation:
```python
def scrape(streeteasy_url):
  headers = {'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36"}

  response = requests.get(streeteasy_url, headers=headers)
  soup = BeautifulSoup(response.text, 'html.parser')
  listings = []

  for listing in soup.find_all('span', class_='u-displayNone'):
    info = listing.get_text(strip=True)
    if info:
      try:
        address = info.split(' at ')[1].split(' for ') [0]
        price = info.split(' for ') [1]
        listings.append ({'Address': address, 'Price': price})
      except IndexError:
        continue
    return listings
```
- This function scrapes real estate listings from a given Streeteasy URL and extracts key details such as the address and price of each listing.
- The "headers" variable uses `User-Agent` to mimic a browser request
- The function sends a GET request to the `streeteasy_url` using the `requests` library, passing in the headers.
- The HTML content of the page is then parsed with `BeautifulSoup`
- The function searches the parsed HTML content for all `span` elements with the class `'u-displayNone'`. This class holds all the real estate listing details.
  - For each matching element, the function extracts the text, strips any surrounding whitespace, and attempts to split the information into two parts: the address and the price.
  - If successful, this information is stored in a dictionary with keys `Address` and `Price`, which is added to the `listings` list.
- Uses the `try-except` block to handle cases where the text might not be in the right format
- Returns a list of dictionaries containing the address and price of the apartments


```python
def format_neighborhood(neighborhood):
    # Convert the neighborhood name into a format suitable for the StreetEasy URL
    return neighborhood.lower().replace(" ", "-")
```
- This function takes a `neighborhood` name as input and converts it into a URL-friendly format.
- It uses the `.lower()` method to convert all characters in the neighborhood name to lowercase, ensuring consistency with StreetEasy URL formatting.
- The `.replace(" ", "-")` method replaces any spaces in the neighborhood name with hyphens (`-`), since StreetEasy uses hyphenated names for URLs (e.g., "East Village" becomes "east-village").
- The formatted neighborhood name is returned, ready to be appended to the StreetEasy base URL for scraping listings in that specific neighborhood.


```python
streeteasy_url = "https://streeteasy.com/for-rent/east-village"
all_listings = []

page = 1
while True:
    print(f"Scraping page {page}...")
    url = f'{streeteasy_url}?page={page}'
    listings = scrape(url)

    if not listings:
        break

    all_listings.extend(listings)
    page += 1

    time.sleep(random.uniform(1, 3))

df = pd.DataFrame(all_listings)
print("Scraping Complete")
```
- This part uses the previous function to scrape the Streeteasy URL and saves the results into a Pandas DataFrame.
- Variables initialized:
  - `streeteasy_url`: Stores the base URL for the Streeteasy rental listings in the East Village.
  - `all_listings`: An empty list initialized to hold all the listings scraped from multiple pages.
- The `While` loop scrapes the listings page by page and runs indefinitely until no more listings are found. Also updates on what page it's on
- Url is formatted the way it's on the StreetEasy site and key information is replaced to change from page to page
- If `listings` is an empty list, the loop breaks
- Listings from the current page are appended to `all_listings`
- `time.sleep(random.uniform(1, 3))` is to mimic human behavior
- Pandas Dataframe is created from the `all_listings` list