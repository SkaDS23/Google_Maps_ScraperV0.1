from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from modules import scroll_page, scrape, export_data 
from queries import queries
import time

"""This code has been updated on 31/01/2024"""

def main():
    start_time = time.time()
    print("Start running...")

    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--lang=en-US")
    driver = webdriver.Chrome(options=options)

    for query in queries:
        print(f"Scraping Data for {query}")
        driver.get("https://www.google.com/maps")

        search_box = driver.find_element(By.ID,'searchboxinput')
        search_box.send_keys(query)
        search_box.send_keys(Keys.RETURN)

        time.sleep(5)

        scroll_js= "document.querySelector('#QA0Szd > div > div > div.w6VYqd > div.bJzME.tTVLSc > div > div.e07Vkf.kA9KIf > div > div > div.m6QErb.DxyBCb.kA9KIf.dS8AEf.ecceSd > div.m6QErb.DxyBCb.kA9KIf.dS8AEf.ecceSd').scrollTop=40000"

        scroll_page(driver, scroll_js)

        time.sleep(5)

        data_scraped = scrape(driver)

        elapsed_time = time.time() - start_time
        print(f'Time elapsed: {round(elapsed_time/60, 2)} minutes')

        #Exporting data to CSV
        export_data(data_scraped, file_name = f'{query}')

    driver.quit()

if __name__ == "__main__":
    main()

