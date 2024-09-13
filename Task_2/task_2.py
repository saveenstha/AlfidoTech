import requests
from bs4 import BeautifulSoup
import pandas as pd

url = input("Enter the URL of the website you want to scrape: ")

try:
    response = requests.get(url)

    if response.status_code == 200:
        html_content = response.text
        print("Successfully fetched the HTML content. ")
        soup = BeautifulSoup(html_content, 'html.parser')
        headlines = soup.find_all('h1')
        for i, headline in enumerate(headlines, 1)
            print(f"Headline: {i}: {headline.get_text(strip=True)}")
    else:
        print(f"Failed to retrieve the webpage. Status code: {response.status_code}")

except requests.exceptions.RequestException as e:
    print(f"An error occurred: {e}")