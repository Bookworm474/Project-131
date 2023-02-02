# GOAL: Scraping wikipedia webpage for data on brightest stars

# import required modules
from selenium import webdriver
from bs4 import BeautifulSoup
import time
import csv

# set URL to scrape
start_url = "https://en.wikipedia.org/wiki/List_of_brightest_stars_and_other_record_stars"
# define Chromedriver as browswer
browswer = webdriver.Chrome("/Users/Ashlesha/Documents/WhiteHatJr/Module_3/Projects/Project 127/chromedriver")
# open URL
browswer.get(start_url)
# let program sleep for 10 seconds (to let the webpage load)
time.sleep(10)

def scrape():
    # headers for CSV file
    headers = ["name", "distance_from_earth", "mass", "radius"]
    # array for storing scraped data
    star_data = []
    # initialise soup
    soup = BeautifulSoup(browswer.page_source, "html.parser")
    
    # open the table
    for table_tag in soup.find_all("table", attrs={"class", "wikitable sortable jquery-tablesorter"}):
        # open the teach <tr> tag
        row_tags = table_tag.find_all("tr")
        for row_tag in row_tags:
            # open each "td" tag
            data_tags = row_tag.find_all("td")
            # initialise temporary array used for adding data
            temp_list = []
            for index, data_tag in enumerate(data_tags):
                # for column 2 (Proper name)
                if index == 1:
                    try:
                        # if value contains hyperlink
                        temp_list.append(data_tag.find_all("a")[0].contents[0])
                    except:
                        # if value does not contain hyperlink
                        temp_list.append(data_tag.contents[0])
                else:
                    try:
                        # for column 4 (Distance)
                        if index == 3:
                            if len(data_tag.contents) > 0:
                                # if value contains a <span> tag before the data
                                temp_list.append(data_tag.contents[1])
                            else:
                                # if value does not contain a <span> tag before the data
                                temp_list.append(data_tag.contents[0])
                        # for column 6 (Mass)
                        if index == 5:
                            temp_list.append(data_tag.contents[0])
                        # for column 7 (Radius)
                        if index == 6:
                            temp_list.append(data_tag.contents[0])
                    except:
                        # if there is no given value
                        temp_list.append("")
            # append temporary array to main array
            star_data.append(temp_list)
    
    # create file to store data
    with open("data.csv", "w") as f:
        csvwriter = csv.writer(f)
        csvwriter.writerow(headers)
        csvwriter.writerows(star_data)

# call function to scrape webpage
scrape()