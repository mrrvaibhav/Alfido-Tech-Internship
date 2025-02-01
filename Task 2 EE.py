import requests
from bs4 import BeautifulSoup
import pandas as pd
import csv


def fetch_webpage_content(target_url):
    """Fetch HTML content from a given URL"""
    headers = {'User-Agent': 'Mozilla/5.0'}
    response = requests.get(target_url, headers=headers)
    if response.status_code == 200:
        return response.text
    else:
        print(f"Failed to retrieve page: {response.status_code}")
        return None


def extract_information(target_url, content_type):
    """Scrape specific data based on user input, handling pagination"""
    collected_data = []
    while target_url:
        page_content = fetch_webpage_content(target_url)
        if not page_content:
            break

        soup = BeautifulSoup(page_content, 'html.parser')

        if content_type == "headlines":
            items = soup.find_all('h2')  # Adjust based on site structure
            collected_data.extend([item.get_text(strip=True) for item in items])
        elif content_type == "product details":
            items = soup.find_all(class_='product')  # Adjust based on site structure
            collected_data.extend([item.get_text(strip=True) for item in items])
        elif content_type == "job listings":
            items = soup.find_all(class_='job-title')  # Adjust based on site structure
            collected_data.extend([item.get_text(strip=True) for item in items])

        next_link = soup.find('a', text='Next')  # Adjust based on site structure
        target_url = next_link['href'] if next_link else None

    return collected_data


def store_data_in_csv(data, file_name="scraped_output.csv"):
    """Save scraped data to a CSV file"""
    with open(file_name, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(["Extracted Information"])
        for record in data:
            writer.writerow([record])
    print(f"Data saved to {file_name}")


if __name__ == "__main__":
    target_url = input("Enter the URL: ")
    content_type = input("Enter the type of data to scrape (headlines, product details, job listings): ")
    retrieved_data = extract_information(target_url, content_type)
    if retrieved_data:
        store_data_in_csv(retrieved_data)
    else:
        print("No data found.")
