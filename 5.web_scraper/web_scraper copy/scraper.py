import requests
from bs4 import BeautifulSoup

def scrape_data(url):
    headers = {
        'User-Agent': 'Mozilla/5.0'
    }
    try:
        res = requests.get(url, headers=headers)
        if res.status_code != 200:
            return [f"Error: Status code {res.status_code}"]
        soup = BeautifulSoup(res.text, 'html.parser')
        headlines = soup.find_all('h3')
        return [h.get_text(strip=True) for h in headlines if h.get_text(strip=True)]
    except Exception as e:
        return [f"Error: {str(e)}"]
