import requests
from bs4 import BeautifulSoup
import pandas as pd
from urllib.parse import urljoin

def get_user_input():
    url = input("Enter the URL of the website you want to scrape: ")
    tag = input("Enter the HTML tag you want to scrape (e.g., 'h1', 'p'): ")
    save_csv = input("Do you want to save the scraped data into a CSV file? (yes/no): ").strip().lower()
    return url, tag, save_csv == 'yes'

def scrape_data(url, tag):
    try:
        current_url = url
        all_data = []
        while current_url:
            response = requests.get(current_url)

            if response.status_code == 200:
                html_content = response.text
                print(f"Successfully fetched the HTML content from: {current_url} ")

                soup = BeautifulSoup(html_content, 'html.parser')
                elements = soup.find_all(tag)

                for element in elements:
                    all_data.append(element.get_text(strip=True))

                next_page = soup.find('a', string='Next')
                if next_page and 'href' in next_page.attrs:
                    current_url = urljoin(current_url, next_page['href'])
                else:
                    break
            else:
                print(f"Failed to retrieve the webpage. Status code: {response.status_code}")
                break

    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
    return all_data

def save_to_csv(data, filename='scraped_data.csv'):
    df = pd.DataFrame(data, columns=['Content'])
    df.to_csv(filename, index=False)
    print(f"Data successfully saved to {filename}")

def main():
    url, tag, save_csv  = get_user_input()
    data = scrape_data(url, tag)

    # Print collected data
    print("\nCollected Data:")
    for item in data:
        print(item)

    if save_csv:
        save_to_csv(data)


if __name__ == '__main__':
    main()