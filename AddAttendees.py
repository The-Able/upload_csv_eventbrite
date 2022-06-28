import sys, time
import webbrowser
import csv
from csv import DictReader
import codecs
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager


try:
    from selenium import webdriver
    from selenium.webdriver.common.keys import Keys
except:
    msg = "Please install Selenium"
    print(msg)
    sys.exit(msg)

login = "angelprodev@gmail.com"
pwd = "@Pasture8"
attendeeList = "1.txt" #Tab-delimited file containing the firstname, surname and email address of your attendees

eventID = "371407920087" #eg open your event then see the URL to obtain the ID, eg https://www.eventbrite.com.au/myevent?eid=123456
ticketID = "quant_641836459" #Use the Dev Tools inspector to determine the ID of the ticket type you wish to add (http://i.imgur.com/RIYANW1.png)

#Open a browser at the event homepage
options = webdriver.ChromeOptions()
options.add_argument(f"--user-data-dir=C:\\Users\\ladyhand\\AppData\\Local\\Google\\Chrome\\User Data")
options.add_argument("profile-directory=Profile 10")

# chrome_path = 'C:/Program Files (x86)/Google/Chrome/Application/chrome.exe %s'
# fp = webdriver.FirefoxProfile()
# browser = webdriver.Firefox()
# browser = webdriver.Chrome(service=Service("E:\\Python\\AddAttendeesToEventBrite\\chromedriver.exe"))
browser = webdriver.Chrome("./chromedriver.exe")
browser.get("https://www.eventbrite.com.au/attendees-add?eid=" + str(eventID))

username = browser.find_element("id", "email")
password = browser.find_element("id", "password")
username.send_keys(login)
password.send_keys(pwd)
print("1")
loginButton = browser.find_element('xpath', '//*[@id="root"]/div/div[2]/div/div/div/div[1]/div/main/div/div[1]/div/div[2]/div/form/div[4]/div/button')
print("2")
loginButton.click()
print("3")
time.sleep(500)
print("4")
#Iterate through each name in the input file
csvread=csv.reader(codecs.open("Mean Girls Attendees - General Admission.csv", 'rU', 'utf-8'))
index = 0
for line in csvread:
    if (index == 0):
        continue
    index += 1
    # print(line)
    # tokens = line.split(",")
    firstname = line[2]
    lastname = line[3]
    email = line[4]
    print("Adding " + firstname + " " + lastname + " (" + email + ")")
    
    #Add each person to the guest list
    try:
        browser.get("https://www.eventbrite.com.au/attendees-add?eid=" + str(eventID))
        time.sleep(10)
        quantity = browser.find_element_by_id(ticketID)
        quantity.send_keys("1")
        continueBtn = browser.find_element_by_xpath('//*[@id="continue-attendee"]')
        # continueBtn = browser.find_element_by_xpath(".//*[@id='content']/div/div/div[2]/div/section/section/form/div[4]/div/a")
        
        continueBtn.click()
        time.sleep(10)
        browser.find_element_by_id("buyer.N-first_name").send_keys(firstname)
        browser.find_element_by_id("buyer.N-last_name").send_keys(lastname)
        browser.find_element_by_id("buyer.N-email").send_keys(email)
        browser.find_element_by_xpath(".//*[@id='primary_cta']/a").click()
        time.sleep(10)
    except:
        print("There was a problem adding " + firstname + " " + lastname)

browser.close()