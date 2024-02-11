from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service  
from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
import pandas as pd
import time
import csv



# Get the number of user inputs
num_inputs = int(input("Enter the number of locations to search: "))
user_inputs = []

# Collect user inputs
for _ in range(num_inputs):
    user_input = input("Enter the address for search: ")
    user_inputs.append(user_input)


# Create a Service instance
chrome_service = Service(ChromeDriverManager().install())

# set driver with the Service instance
source_page = webdriver.Chrome(service=chrome_service)


source_page.get("https://zola.planning.nyc.gov/about")
time.sleep(5)



data_collected = []
# Perform actions for each user input
for user_input in user_inputs:

    time.sleep(5)
    search_line = source_page.find_element(By.ID,'map-search-input')
    search_line.clear()
    search_line.send_keys(user_input)
    time.sleep(3)

    select_list = source_page.find_element(By.XPATH,'//*[@id="ember17"]/ul')
    select_list.find_element(By.XPATH,'//*[@id="ember17"]/ul/li[2]').click()
    time.sleep(3)

    div_element_for_lot_details = source_page.find_element(By.XPATH,'/html/body/div[2]/div/div[3]')
    get_lot_details = div_element_for_lot_details.find_element(By.CLASS_NAME,'lot-details')
    lot_details = get_lot_details.text.splitlines()

    year_label_scanner = lot_details.index('Year Built')
    year = lot_details[year_label_scanner+1]
    land_use_label_scanner = lot_details.index('Land Use')
    land_use = lot_details[land_use_label_scanner+1]

    try:
        owner_type_label_scanner = lot_details.index('Owner Type')
        owner_type = lot_details[owner_type_label_scanner+1]
    except:
        owner_type = 'No Owner Type on location details'

    data_collected.append([year,land_use,owner_type])


data = data_collected
df = pd.DataFrame(data, columns=['year','land use','owner type'])
df.to_csv("C:\\Users\\user_name\\data.csv" , header=True,index=True,index_label='row_id',mode='w')
print(data)
    
