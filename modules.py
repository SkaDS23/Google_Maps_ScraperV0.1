from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import pandas as pd
import time
import requests
from requests.exceptions import ConnectTimeout, TooManyRedirects, ConnectionError, ContentDecodingError,ChunkedEncodingError,HTTPError,RetryError
from bs4 import BeautifulSoup
import re

"""This code has been updated on 31/01/2024"""

def scroll_page(driver, scroll_js, scroll_times=10, scroll_interval=2):
    """Scrolls the page multiple times."""
    for _ in range(scroll_times):
        driver.execute_script(scroll_js)
        time.sleep(scroll_interval)
    print("Scrolling done successfully!")
    
#This function is not executable unless you activate it in the scrape function    
def extract_emails_from_url(url):
    """Scraping e-mail adresses from each source website (only the 1st page)"""
    try:
        response = requests.get(url, allow_redirects=True)
        soup = BeautifulSoup(response.content, 'html.parser')
        text = soup.get_text()
        emails = re.findall(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', text)
        for email in emails:
            return email
        
    except (TooManyRedirects,
            ConnectTimeout,
            ConnectionError,
            ContentDecodingError,
            ChunkedEncodingError,
            HTTPError,
            RetryError):
        print("Error requesting the website for e-mail")

def scrape(driver):
    """Scrapes Data Logic"""
    elements = driver.find_elements(By.CLASS_NAME, "hfpxzc")
    data_scraped = []
    for i, element in enumerate(elements):
        driver.execute_script("arguments[0].click();", element)
        time.sleep(2)
        try:
            title = element.find_element(By.XPATH, "//h1[contains(@class, 'DUwDvf')]").text
            address = element.find_element(By.XPATH, "//div[@class='Io6YTe fontBodyMedium kR99db ']").text
            rating = element.find_element(By.XPATH, "//div[@class='F7nice ']").text.split('\n')[0]
            phone = element.find_element(By.XPATH, "//button[contains(@class, 'CsEnBe') and starts-with(@data-item-id, 'phone:tel:')]").text
            url = element.find_element(By.XPATH,"//a[@class='CsEnBe']")
            url_link = url.get_attribute("href")
            #email = extract_emails_from_url(url_link)

                
        except NoSuchElementException:
            print(f"Skipping element {i+1}: Required information not found")
            continue
        
        time.sleep(2)  
        
        data = {
            'Title' : title,
            'Address' : address,
            'Rating' : rating,
            'Phone_Number' : phone,
            'URL' : url_link,
            #'Mail' : email
        }
        data_scraped.append(data)
        print(f'Element {i+1} scraped successfully')
    print(f'You have scraped a total of {len(data_scraped)} items')
    return data_scraped


def export_data(data = list, file_name = str):
    """Export data into CSV ! you can change the format below according to your needs (xlsx)"""
    df = pd.DataFrame(data)
    df.to_csv(f"{file_name}.csv")