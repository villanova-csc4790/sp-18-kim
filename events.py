import logging
from random import randint
from flask import Flask, render_template, json
from flask_ask import Ask, statement, question, session, audio, current_stream
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def getEvents(driver):
    url = 'https://www1.villanova.edu/villanova/studentlife/be_engaged/cat/calendar.html'
    driver.get(url) #The webdriver accesses this URL which is to the Villanova campus events page
    wait = WebDriverWait(driver, 4) #allows 10 seconds for elements of page to be loaded in before throwing a TimeoutException

    events = [] #an array to store the event titles with their event times for output 
    count = 0 #a count to keep track of the number of events at Villanova  

    #wait until the xpath for the calendar's back button is available and then click 
    
    eventItem = 'eventItemContainer'
    for eventNum in range(1,5):
        wait.until(EC.presence_of_element_located((By.ID, eventItem + str(eventNum))))
        event = driver.find_element_by_id(eventItem + str(eventNum))
        eventTitle = event.get_attribute('href').text
        eventTime = event.find_element_by_class_name('datetime').text
        events.append(eventTitle + " is at " + eventTime)
        count += 1
    events.append("There are " + count + " events today at Villanova")
    return events

    # #for every event title found, determine the times for the event and store the title and times in eventOutput array
    # for title in driver.find_elements_by_class_name("fc-event-title"):

    #     time = title.find_element_by_xpath('.//parent::div')

    #     #this determines if there is no time listed with the event, it is an all day event 
    #     if time.get_attribute("textContent") == title.text: 
    #         event.append(title.text + " is an all day event.")
    #     else:
    #         content = time.get_attribute("textContent")
    #         eventTitle = title.text 
    #         event.append(title.text + " is from " + content.replace(eventTitle, ""))
    #     count += 1 

    # # Formats the output to handle if there's 1 event to use "is" otherwise, use "are"
    # if count == 1:
    #     event.append("There is " + str(count) + " event at Villanova today")
    # elif count == 0:
    #     event.append("There are no events at Villanova")
    # else:
    #     event.append("There are " + str(count) + " events at Villanova today")
