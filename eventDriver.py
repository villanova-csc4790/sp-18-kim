import logging
import os
from random import randint
from flask import Flask, render_template, json, jsonify, request
from flask_ask import Ask, statement, question, session
import smtplib #email
from random import randint
from selenium import webdriver
from events import getEvents

app = Flask(__name__)
ask = Ask(app, "/")
logging.getLogger("flask_ask").setLevel(logging.DEBUG)
code = [randint(0, 9) for _ in range(6)] #randomly generate 6-digit authentication code
access = False

@ask.launch
def new_game():
    global driver 
    driver = webdriver.Chrome()
    welcome_msg = render_template('welcome')
    return question(welcome_msg)

#User says their Villanova Banner ID number. JSON is opened and read to find  Banner ID and store corresponding email and username.
@ask.intent("IdentificationIntent", convert={'first': int, 'second': int, 'third': int, 'fourth': int, 'fifth': int, 'sixth': int})
def identify(first, second, third, fourth, fifth, sixth, seventh, eighth):
    idNum = [str(first), str(second), str(third), str(fourth), str(fifth), str(sixth), str(seventh), str(eighth)]
    with open('C:/Users/I861728/Documents/villanovaCampusEvents/users.json') as json_file:  
        data = json.load(json_file)
        for item in data['users']:
            if list(item['id']) == idNum:
                global userEmail, username
                userEmail = (item['email'])
                username = (item['name'])
                msg = render_template('email')
                return question(msg)
        else:
            msg = render_template('notFound')
            return statement(msg)

#When user responds with "yes", an email with the authentication code is sent to their sap email.
@ask.intent("YesIntent")
def authenticate():
    global userEmail
    server = smtplib.SMTP_SSL('smtp.gmail.com', 465) 
    SUBJECT = "Villanova Campus Events Authentication Code"
    TEXT = "Please repeat this code back to Alexa:\n "+('-'.join(map(str,code)))
    message = "Subject: {}\n\n{}".format(SUBJECT, TEXT)
    server.sendmail(
        "villanovacampusevents@gmail.com", #FROM
        userEmail, #TO
        message)
    server.quit()
    round_msg = render_template('authenticate')
    return question(round_msg)

#if user says no, they will not be sent an email and will not have access.
@ask.intent("NoIntent")
def no_access():
    msg = render_template('prohibited')
    return statement(msg)

#user must repeat back their 6-digit authorization code
@ask.intent("RepeatIntent", convert={'first': int, 'second': int, 'third': int, 'fourth': int, 'fifth': int, 'sixth': int})
def verify(first, second, third, fourth, fifth, sixth):
    global access
    global username
    if [first, second, third, fourth, fifth, sixth] == code:
        msg = render_template('correct', username=username) 
        access = True
        return question(msg)
    else:
        msg = render_template('wrong') 
        access = False
        return statement(msg)

@ask.intent("EventIntent")
def event_round():
    global access
    if access == False:
        msg = render_template('unauthorized')
        return question(msg)
    else:
        eventOutput = getEvents(driver)
        round_msg = render_template('events', eventOutput=eventOutput)
        return question(round_msg)

@ask.intent("AMAZON.StopIntent")
def bye_round():
    round_msg = render_template('bye')
    return statement(round_msg)

if __name__ == '__main__':
    app.run(debug=True)
