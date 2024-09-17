import pandas as pd
from bs4 import BeautifulSoup
import requests, time, datetime, re, random

def scrape(streeteasy_url):
    headers = {'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36"}
    response = requests.get(streeteasy_url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    listings = []

    for listing in soup.find_all('span', class_='u-displayNone'):
        info = listing.get_text(strip=True)
        if info:
            try:
                address = info.split(' at ')[1].split(' for ')[0]
                price = info.split(' for ')[1]
                listings.append({'Address': address, 'Price': price})
            except IndexError:
                continue

    return listings

def format_neighborhood(neighborhood):
    # Convert the neighborhood name into a format suitable for the StreetEasy URL
    return neighborhood.lower().replace(" ", "-")

# Ask the user for the neighborhood input
neighborhood = input("Enter the NYC neighborhood you want to search for (e.g., 'East Village'): ").strip()
formatted_neighborhood = format_neighborhood(neighborhood)

# Construct the URL for the specific neighborhood
streeteasy_url = f"https://streeteasy.com/for-rent/{formatted_neighborhood}"
all_listings = []

page = 1
while True:
    print(f"Scraping page {page} of {neighborhood}...")
    url = f'{streeteasy_url}?page={page}'
    listings = scrape(url)

    if not listings:
        break

    all_listings.extend(listings)
    page += 1

    time.sleep(random.uniform(1, 3))  # Sleep to avoid overwhelming the server

# Convert the results into a DataFrame
df = pd.DataFrame(all_listings)

if df.empty:
    print(f"No listings found for {neighborhood}.")
else:
    print("Scraping Complete")
    print(df)
