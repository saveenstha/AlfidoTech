import requests
from bs4 import BeautifulSoup
import pandas as pd

url = input("Enter the URL of the website you want to scrape: ")

try:
    current_url = url
    all_headlines = []
    while current_url:
        response = requests.get(url)

        if response.status_code == 200:
            html_content = response.text
            print(f"Successfully fetched the HTML content from: {current_url} ")

            soup = BeautifulSoup(html_content, 'html.parser')
            headlines = soup.find_all('h1')

            for headline in headlines:
                all_headlines.append(headline.get_text(strip=True))

            next_page = soup.find('a', text='Next')
            if next_page and 'href' in next_page.attrs:
                current_url = next_page['href']
        else:
            print(f"Failed to retrieve the webpage. Status code: {response.status_code}")

except requests.exceptions.RequestException as e:
    print(f"An error occurred: {e}")