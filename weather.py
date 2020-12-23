import requests
import os
from bs4 import BeautifulSoup as BS

# set working directory to this script's directory
if (os.path.dirname(os.path.abspath(__file__)) != os.getcwd()):
    os.chdir(os.path.dirname(os.path.abspath(__file__)))

page = requests.get("http://forecast.weather.gov/MapClick.php?lat=37.7772&lon=-122.4168")

soup = BS(page.content, 'html.parser')
seven_day = soup.find(id='seven-day-forecast')
title = seven_day.select('h2.panel-title')

location = f"Location is {title[0].get_text().strip()}"

file_obj = open("weather.txt", 'w') 
file_obj.write(f"{location}\n")
file_obj.write("----------------------------\n")
forecasts = seven_day.find_all(class_="tombstone-container") # find forecasts data for all  periods

# extract and save forecast data for each periods
for each in forecasts:
    period = each.select('p.period-name')[0].get_text().strip()
    description = each.select('img.forecast-icon')[0]['title']
    short_description = each.select('p.short-desc')[0].get_text().strip()
    temp = each.select('p.temp')[0].get_text().strip()
    
    file_obj.write(f"{period}\n")
    file_obj.write(f"{description}\n")
    file_obj.write(f"{short_description}\n")
    file_obj.write(f"{temp}\n")
    file_obj.write("\n")

file_obj.close()



    
