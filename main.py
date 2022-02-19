from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.select import Select
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup

def main():
    # Constants
    URL = "https://fdc.nal.usda.gov/fdc-app.html#/food-details/172615/nutrients"

    # Variables
    # Data parsed in csv format
    csv_data = "name,amount,unit\n"
    page = None

    # If you don't use a try except, then the driver might not close if it fails, leaving annoying webpages open
    try:
        # You can also use safari or firefox, but Chrome seems to have the least problems.
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
        driver.get(URL)

        # This just makes sure we got to the right page. If you do other pages, change this to the new title (the name on the tab). You can use only part of the title too (as I did here)
        assert "FoodData Central" in driver.title

        # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        # IMPORTANT: This selects the correct dropdown (in your case, 4oz).
        # select_by_index(1) just choses the second option. You'll probably
        # need to find to edit this code (both the id and index) if you
        # need to select other dropdowns. Otherwise, delete this.
        # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        select_element = driver.find_element(By.ID,'nutrient-per-selection-Survey-or-branded')
        select_object = Select(select_element)
        select_object.select_by_index(1)

        # This sleep was important. It was getting the html too fast, and the page wasn't fully loaded. It was giving me blank results. Sleeping for 1 second fixed it.
        sleep(1)

        page = driver.page_source

        # Closes the webpage
        driver.close()
    except:
        driver.close()

    # Parse page's html
    soup = BeautifulSoup(page, 'html.parser')

    # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    # IMPORTANT: We only care about the table in your case. I found it by its id.
    # BUT, other tables on the site probably won't have the same id. You have a few options:
    # 1. You can try soup.find("table"). This will find the FIRST table on the page.
    # 2. You can try soup.find_all("table"). This will get ALL the tables on the page.
    # Then you can try to print them out and find the one you need.
    # This will probably be annoying.
    # 3. If you know how to do inspect element and find the table's id
    # then this is probably the best option. I would write a function that does this and
    # takes the id as an arugment, so it's easier to change for other tables.
    # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    table = soup.find("table",{"id":"nutrients-table"})

    # Get the actual data and format it
    all_tr = table.tbody.find_all('tr')
    # This gets every row of the table
    for i in all_tr:
        all_td = i.find_all('td')

        # Some of the td's had a 0 length, so I skipped them by adding this if statement
        if(len(all_td) >= 2):
            name = all_td[0].span.text.strip().replace(","," ")
            amount = all_td[1].span.text.strip()
            unit = all_td[2].span.text.strip()
            # This divided the amount by 4. Change this to whatever you need.
            amount = str(float(amount) / 4)

            csv_data += "{0},{1},{2}\n".format(name, amount, unit)

    # Write the data to a csv file
    with open('nutrition.csv','w') as file:
        file.write(csv_data)

if __name__ == "__main__":
    main()