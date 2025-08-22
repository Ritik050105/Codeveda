from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import time

def scrape_data(url):
    print("Scraping:", url)
    try:
        options = Options()
        options.add_argument("--headless")
        options.add_argument("--disable-gpu")
        options.add_argument("--no-sandbox")
        driver = webdriver.Chrome(options=options)
        driver.get(url)
        time.sleep(4)  # wait for JS content
        html = driver.page_source
        driver.quit()
        soup = BeautifulSoup(html, "html.parser")
        headings = soup.find_all(["h1", "h2", "h3"])
        return [tag.get_text(strip=True) for tag in headings if tag.get_text(strip=True)]
    except Exception as e:
        print("Error:", e)
        return []
