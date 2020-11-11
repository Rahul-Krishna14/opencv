# -*- coding: utf-8 -*-
"""
Created on Fri Oct 23 20:07:56 2020

@author: Rahul K
"""

import selenium 
from selenium import webdriver
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
import pandas as pd
import time
import datetime

options = Options()
options.add_argument("--window-size=1920,1080")
options.add_argument("--incognito")
DRIVER_PATH = "D:/chrome_driver/chromedriver.exe"
driver = webdriver.Chrome(options=options,executable_path=DRIVER_PATH)


book_my_show = pd.DataFrame(columns=['Movie Name','Venue','Timings'])

movie_show = {}
count = 0


link = 'https://www.showbizcinemas.com/locations/'

driver.get(link)

locations = driver.find_elements_by_css_selector('div.cinemaItemImage > div.cinemaItemLinks > div:nth-child(2) > a')

url_list=[]
for loc in locations:
    link = loc.get_attribute('href')
    url_list.append(link)

def get_amenities():
    amentite_list = []
    amentities = driver.find_elements_by_css_selector('div > div.cinemaItemContent > p')
    for ametitie in amentities:
        amentite_list.append(ametitie.text)
    
    amentites_dict = {'BAYTOWN': amentite_list[0], 'EDMOND': 'N/A', 'FALL CREEK': amentite_list[2], 'HOMESTEAD': amentite_list[3], 'KINGWOOD': amentite_list[4], 'LIBERTY LAKES':amentite_list[5],'WAXAHACHIE':amentite_list[6]}
    return amentites_dict

amenities = get_amenities()



def get_theater_data(url_link):   
    N = []
    M = []
    O = []
    P = []
    Q = []
    
    driver.get(url_link)
    name = driver.find_elements_by_css_selector('div.gridCol-l-12.gridCol-m-12.gridCol-s-12 > div > div:nth-child(3)')
    name = name[0].text
    name = name.split('\n')
    name.remove('SEE MAP & DIRECTIONS')
    if len(name) < 3:
        a = name[1][-8:]
        name.append(a)
        name[1] = name[1] = name[1].rstrip(name[1][-8:])
    elif len(name) == 3 and name[2][0] == '(':
        del name[2]
        a = name[1][-8:]
        name.append(a)
        name[1] = name[1].rstrip(name[1][-8:])
    pin_code = name[2][-5:]
    name.append(pin_code)
    name[2] = name[2].rstrip(name[2][-5:])
    city = name[1].split(',')
    city.remove('')
    city = city[len(city)-1]
    name.append(city)



    N.append(name[0])
    M.append(name[1])
    O.append(name[2])
    P.append(name[3])
    Q.append(name[4])


    dict1 = {'Name': N, "Address" : M,'City': Q ,'State' : O, 'PIN Code' : P}
    
    return dict1

def get_date(details):
    
    dict1 = {'January' : '01-', 'February': '02-','March':'03-','April':'04','May':'05-','June':'06-','July':'07-','August':'08-','September':'09-','October': '10-','November':'11-', 'December':'12-'}
    
    date =  details[2].rstrip(' ')
    date = date.split(',')
    date = date[1]
    date = date.split(' ')
    date.remove('')
    x = datetime.datetime.now()
    x = str(x.year) + '-'
    date.insert(0, x)
    date[1] = dict1[date[1]]
    date[2] = date[2][:-2]
    date = ''.join(date)
    
    
    return date

'''def Get_show_time_url(urls):
    driver.get(urls)
    show_time_link = driver.find_elements_by_css_selector('a:nth-child(2)')
    ticket_link_list = []
    for show_link in show_time_link:
        ticket_link = show_link.get_attribute('href')
        ticket_link_list.append(ticket_link)
    ticket_link_new = []
    
    for none in ticket_link_list:
        if none == None:
            ticket_link_list.remove(none)
            
    for booking in ticket_link_list:
        if 'booking' in booking:
            ticket_link_new.append(booking)
    
    if ticket_link_new != []:
        return ticket_link_new
    else:
         driver.get(urls)
         
             
         show_time_link = driver.find_elements_by_css_selector('a:nth-child(2)')
         ticket_link_list = []
         for show_link in show_time_link:
             ticket_link = show_link.get_attribute('href')
             ticket_link_list.append(ticket_link)
         ticket_link_new = []
        
         for none in ticket_link_list:
            if none == None:
                ticket_link_list.remove(none)
         return ticket_link_new'''
        
        
    
    



def Get_Movie_details(url_list):
    count = 0
    for url in url_list:
        count += 1
        driver.get(url)
        show_time_link = driver.find_elements_by_css_selector('a:nth-child(2)')
        ticket_link_list = []
        for show_link in show_time_link:
            ticket_link = show_link.get_attribute('href')
            ticket_link_list.append(ticket_link)
        ticket_link_new = []
        for none in ticket_link_list:
            if none == None:
                ticket_link_list.remove(none)
                
        for booking in ticket_link_list:
            if 'booking' in booking:
                ticket_link_new.append(booking)
    
 
            
        Movie_details_list = pd.DataFrame()
        Address_info = get_theater_data(url)
        theater_name = Address_info['Name'][0]
        Amenities_ = amenities[theater_name]
        location_address = Address_info['Address'][0]
        city = Address_info['City'][0]
        state = Address_info['State'][0]
        zipcode = Address_info['PIN Code'][0]
       
        Movie_details = driver.find_elements_by_css_selector('div > div.gridCol-l-9.gridCol-m-9.gridCol-s-7')
        if Movie_details == []:
            tomorrow = driver.find_element_by_class_name('active')
            tomorrow.click()
            time.sleep(2)
            Movie_details = driver.find_elements_by_css_selector('div > div.gridCol-l-9.gridCol-m-9.gridCol-s-7')
        #print(Movie_details)
        
        
        
        for i in range(len(Movie_details)):
            details = Movie_details[i].text
            details = details.split('\n')
            Movie_name = []
            t2_time = []
            Movie_rating = []
            date_in_format = get_date(details)
            Movie_data = []
            Movie_time = []
            Theater_name = []
            Theater_location = []
            Theater_city = []
            Theater_state = []
            Theater_zipcode = []
            Movie_duration = []
            features_list = []
            show_time_link_list = []
            details[1] = details[1].rstrip('MORE DETAILS')
            rate_index = details[1].split(' ')
            rating = rate_index.pop(0)
            duration = ' '.join(rate_index)
            print('Done')
    
    
            for j in range(len(details)):
                
                
                if details[j][-2:] == 'PM' or details[j][-2:] == 'AM':
                    Movie_time.append(details[j])
            t2_time = []
            for im in Movie_time:
                b1 = []
                if im[-2:] =='PM' and im[0:2] != '12':
                    im = im.rstrip(' PM')
                    timeconv = im.split(':')
                    b = timeconv[0]
                    b = int(b)
                    b += 12
                    b1.append(str(b))
                    b1.append(':')
                    b1.append(timeconv[1])
                    c = ''.join(b1)
                    t2_time.append(c)
                elif im[-2:] =='PM' and im[0:2] == '12':
                     im = im.rstrip(' PM')
                     t2_time.append(im)
                elif im[-2:] =='AM' and im[0:2] == '12':
                     im = im.rstrip(' AM')
                     timeconv = im.split(':')
                     b = '00'
                     b1.append(b)
                     b1.append(':')
                     b1.append(timeconv[1])
                     c = ''.join(b1)
                     t2_time.append(c)
                elif im[-2:] =='AM' and im[0:2] != '12':
                     im = im.rstrip(' AM')
                     t2_time.append(im)
                #print(t2_time)
                
                        
                    

                    
            for k in range(len(t2_time)):
                Movie_name.append(details[0])
                Movie_rating.append(rating)
                Movie_data.append(date_in_format)
                Theater_name.append(theater_name)
                Theater_location.append(location_address)
                Theater_city.append(city)
                Theater_state.append(state)
                Theater_zipcode.append(zipcode)
                Movie_duration.append(duration)
                features_list.append(Amenities_)
                if ticket_link_new != []:
                    booking_link = ticket_link_new.pop(0)
                    show_time_link_list.append(booking_link)
                else:
                    booking_link = 'N/A'
                    show_time_link_list.append(booking_link)
                    
                
                
    
            Show_time_dictionary = {'Theater':Theater_name,'Address':Theater_location,'City':Theater_city,'State':Theater_state,'Zip Code':Theater_zipcode ,'Movie Title': Movie_name, 'Movie Details': Movie_rating,'Duration': Movie_duration, 'Movie Date/Day': Movie_data, 'Show Timings' : t2_time, 'Amenities': features_list, 'Booking_link': show_time_link_list}
            if i == 0:
                Movie_details_list =  pd.DataFrame(Show_time_dictionary)
            else:
                df = pd.DataFrame(Show_time_dictionary)
                frames = (Movie_details_list, df)
                Movie_details_list = pd.concat(frames, sort=False, ignore_index = True)
        if count == 1:
                Movie_det =  Movie_details_list
        else:
            frames = (Movie_det,Movie_details_list)
            Movie_det = pd.concat(frames, sort=False, ignore_index = True)
        
        print(f'{count} completed')
    return Movie_det

Movie_details_list = Get_Movie_details(url_list)