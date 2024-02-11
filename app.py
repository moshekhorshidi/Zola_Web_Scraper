import streamlit as st
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service  
from webdriver_manager.chrome import ChromeDriverManager
import time


# Create a Service instance
chrome_service = Service(ChromeDriverManager().install())

st.title("New York City Zola Plan Search")

user_input = st.text_input("***Insert address or location to search:*** :badminton_racquet_and_shuttlecock:")

if st.button("Run Search",type="primary"):
        
        
        try:

            
            searching_status = st.info("Search in progress. Please wait for data.  :globe_with_meridians:")

            # Instantiate the Chrome driver with the Service instance
            source_page = webdriver.Chrome(service=chrome_service)


            source_page.get("https://zola.planning.nyc.gov/about")
            
            time.sleep(5)
            search_line = source_page.find_element(By.ID,'map-search-input')
            search_line.send_keys(user_input)
            time.sleep(3)
            select_list = source_page.find_element(By.XPATH,'//*[@id="ember17"]/ul')
            select_list.find_element(By.XPATH,'//*[@id="ember17"]/ul/li[2]')
            get_list_of_serach = select_list.text.splitlines()
            first_value_in_search = get_list_of_serach[1]
            select_list.click()
            time.sleep(5)

            first_search_result = source_page.find_element(By.XPATH,'/html/body/div[2]/div/div[1]/div[1]/div/div[1]/ul/li[2]')
            print(first_search_result.text)
            print(first_search_result)
            
            
            st.success(f"**Search Found** and data will be presented for: ***'{first_value_in_search}'***  :round_pushpin: :heavy_check_mark:")
            time.sleep(5)

            st.caption(f"Web application by :blue[**Moshe Khorshidi**] :sunglasses:")


            st.subheader("Search Result Data", divider='violet') 

            # get data we need

            content_for_lot_number = source_page.find_element(By.XPATH,'/html/body/div[2]/div/div[3]/div/div[3]/p')
            lot_list = content_for_lot_number.text.split()
            lot_number = lot_list[8]

            content_for_block_number = source_page.find_element(By.XPATH,'/html/body/div[2]/div/div[3]/div/div[3]/p')
            lot_list = content_for_block_number.text.split()
            block_number = lot_list[5]

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


            st.write(f":black_medium_small_square: Lot number of this location is: **{lot_number}**")
            st.write(f":black_medium_small_square: Block number of this location is: **{block_number}**")
            st.write(f":black_medium_small_square: The ownership type of this location is: **{owner_type}**")
            st.write(f":black_medium_small_square: The land use of this property is: **{land_use}**")
            st.write(f":black_medium_small_square: The Year Built of this property: **{year}**")

            st.write(':white_check_mark:')

            st.button("Close Search")

        except:

            st.info("""
                 
                **Location search not found**
                 
                ***User guide check:***

                1. Not empty input to search
                1. Try again with **clicking enter key** after insert search
                2. Check your address/location are properly writen in the search input 
                3. Example for a correct search address: "1281 St Johns PL Brooklyn, NY 11213"
    
                :round_pushpin: :heavy_multiplication_x: 
                 """)
            
            st.button("Close user check")
