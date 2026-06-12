#scrape the site in .env

import os
import re
from dotenv import load_dotenv
import nltk
from nltk.corpus import stopwords
from bs4 import BeautifulSoup
import requests

env_path = os.path.join(os.path.dirname(__file__), '..', '.env')
load_dotenv(dotenv_path=env_path)

scrape_url = os.getenv("scrape_url")

#create the headers 
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

#read text from the url
def read_text_from_url(url):
      
        response = requests.get(url, headers=headers,timeout=20)
        if response.status_code == 200:
            return response.text
        else:
            raise Exception(f"Failed to fetch data from {url}. Status code: {response.status_code}")
    


if __name__ == "__main__":
    try:
        text = read_text_from_url(scrape_url)
        #print(text[:500])  # Print the first 500 characters of the fetched text
        #html parsing
        soup = BeautifulSoup(text, 'html.parser')
        #extracting the quotes
        quotes = soup.find_all('div', class_='quote')
        for quote in quotes:
            text = quote.find('span', class_='text').get_text()
            author = quote.find('small', class_='author').get_text()
            print(f"{text} - {author}")

    except Exception as e:
        print(str(e))
    