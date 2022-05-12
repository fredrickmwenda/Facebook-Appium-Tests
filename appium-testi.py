
from email import message
from appium import webdriver
from appium.webdriver.common.mobileby import MobileBy
import pandas as pd
from pymongo import MongoClient
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import time

class Action():
    
    """
    Action class
    """
    def __init__(self, driver):
        self.desired_caps = {
            'platformName': 'Android',
            'platformVersion': '10',
            'deviceName': 'Itel A48',
            'appPackage': 'com.facebook.katana',
            #login activity
            'appActivity': 'com.facebook.katana.LoginActivity',
            ''
            'noReset': True,
            'newCommandTimeout': 6000,
            'automationName': 'UiAutomator2'

        }
        # Initialize the remote Webdriver using BrowserStack remote URL
        # and desired capabilities defined above
        self.driver = webdriver.Remote('http://localhost:4723/wd/hub', self.desired_caps)
        self.wait = WebDriverWait(self.driver, 10)
        #input your username and password
        self.username = 'username'
        self.password = 'password'
        # start the login process
        self.login()

  


    def switch_to_context(self, context):
        """
        Switch to context
        :param context:
        :return:
        """
        return self.driver.switch_to.context(context)

    def switch_to_active_wxapp_window(self):
        """
        Switch to active window
        :return:
        """
        return self.driver.switch_to.window(self.driver.window_handles[0])

    def scroll_webview_screens(self, pages):
        """
        Scroll webview screens
        :param pages:
        :return:
        """
        for i in range(pages):
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(3)
    
    def login(self):
        """
        Login to the facebook app
        :return:
        """
        self.driver.find_element(MobileBy.XPATH, '//android.view.ViewGroup[@content-desc="Username"]').send_keys('username')
        self.driver.find_element(MobileBy.XPATH, '//android.view.ViewGroup[@content-desc="Password"]').send_keys('password')
        self.driver.find_element(MobileBy.XPATH, '//android.view.ViewGroup[@content-desc="Log In"]').click()
        time.sleep(5)

       #incase facebook asks for permission to access location so we can get user
        if self.driver.find_element(MobileBy.XPATH, '//android.widget.ViewGroup[@content-desc="Allow"]').is_displayed():
            self.driver.find_element(MobileBy.XPATH, '//android.widget.ViewGroup[@content-desc="Allow"]').click()
            time.sleep(5)
            # save login info
            el1 = self.driver.find_element(MobileBy.XPATH, value="/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.Button")
            el1.click()
            time.sleep(3)


            # allow facebook to access location by mobileby.id
            if self.driver.find_element(MobileBy.ID, 'com.android.permissioncontroller.id./permission_allow_foreground_round_only_button').is_displayed():
                self.driver.find_element(MobileBy.ID, 'com.android.permissioncontroller.id./permission_allow_foreground_only_button').click()
                time.sleep(5)

            #go to recent chants
            
        

    
    


    #Start officially start from here
    #get user current locations from facebook app
    #download user information from facebook app and retrieve the data  and save it in mongo
    #get chats for all users 


    def get_private_messages(self):
    # get private messages in facebook app
        self.driver.find_element(MobileBy.XPATH, '//android.widget.Button[@content-desc="Messaging"]/android.view.View').click()
        time.sleep(5)
        self.driver.find_element(MobileBy.XPATH, '//android.widget.TextView[@text="Private"]').click()
        time.sleep(5)
        self.driver.find_element(MobileBy.XPATH, '//android.widget.TextView[@text="Messages"]').click()
        time.sleep(5)
        self.driver.find_element(MobileBy.XPATH, '//android.widget.TextView[@text="Private"]').click()
        time.sleep(5)
        #get each private message
        message =  []
        messages = self.driver.find_elements(MobileBy.XPATH, '//android.widget.TextView[@resource-id="com.facebook.katana:id/text"]')
        for i in messages:
            message.append(i.text)
        print (message)
        #get each private message sender
        sender = []
        senders = self.driver.find_elements(MobileBy.XPATH, '//android.widget.TextView[@resource-id="com.facebook.katana:id/name"]')
        for i in senders:
            sender.append(i.text)
        print('sender:', sender)
        #get each private message time
        time = []
        times = self.driver.find_elements(MobileBy.XPATH, '//android.widget.TextView[@resource-id="com.facebook.katana:id/timestamp"]')
        for i in times:
            time.append(i.text)
        print('time:', time)
        #get each private message status
        status = []
        statuses = self.driver.find_elements(MobileBy.XPATH, '//android.widget.TextView[@resource-id="com.facebook.katana:id/status"]')
        for i in statuses:
            status.append(i.text)
        print('status:', status)
        #get each private message id
        id = []
        ids = self.driver.find_elements(MobileBy.XPATH, '//android.widget.TextView[@resource-id="com.facebook.katana:id/id"]')
        for i in ids:
            id.append(i.text)
        print('id:', id)

        #get each private message thread id
        thread_id = []
        thread_ids = self.driver.find_elements(MobileBy.XPATH, '//android.widget.TextView[@resource-id="com.facebook.katana:id/thread_id"]')
        for i in thread_ids:
            thread_id.append(i.text)
        print('thread_id:', thread_id)
        # store private messages in mongo
        client = MongoClient('localhost', 27017)
        db = client.test
        collection = db.messages
        for i in range(len(message)):
            collection.insert_one({'message': message[i], 'sender': sender[i], 'time': time[i], 'status': status[i], 'id': id[i], 'thread_id': thread_id[i]})

    
    def get_private_messages_from_mongo(self):
        # get private messages from mongo
        client = MongoClient('localhost', 27017)
        db = client.test
        collection = db.messages
        messages = collection.find({})
        df = pd.DataFrame(list(messages))
        df.to_csv('messages.csv')

    #get contact list from mongo
    def get_contact_list_from_mongo(self):
        client = MongoClient('localhost', 27017)
        db = client.test
        collection = db.contacts
        contacts = collection.find({})
        df = pd.DataFrame(list(contacts))
        df.to_csv('contacts.csv')

    def get_contact_list(self):
        # get contact list from facebook app
        self.driver.find_element(MobileBy.XPATH, '//android.widget.TextView[@text="Messages"]').click()
        time.sleep(5)
        self.driver.find_element(MobileBy.XPATH, '//android.widget.TextView[@text="Contacts"]').click()
        time.sleep(5)
   
   #get user current locations from facebook app
    def get_user_current_locations(self):
        self.driver.find_element(MobileBy.XPATH, '//android.widget.TextView[@text="Messages"]').click()
        time.sleep(5)
        self.driver.find_element(MobileBy.XPATH, '//android.widget.TextView[@text="Locations"]').click()
        time.sleep(5)
        self.driver.find_element(MobileBy.XPATH, '//android.widget.TextView[@text="Current"]').click()
        time.sleep(5)
    
    def get_user_current_locations_from_mongo(self):
        client = MongoClient('localhost', 27017)
        db = client.test
        collection = db.locations
        locations = collection.find({})
        df = pd.DataFrame(list(locations))
        df.to_csv('locations.csv')
    
    #get user all locations and how they were shared from facebook app
    def get_user_all_locations(self):
        self.driver.find_element(MobileBy.XPATH, '//android.widget.TextView[@text="Messages"]').click()
        time.sleep(5)
        self.driver.find_element(MobileBy.XPATH, '//android.widget.TextView[@text="Locations"]').click()
        time.sleep(5)
        self.driver.find_element(MobileBy.XPATH, '//android.widget.TextView[@text="All"]').click()
        time.sleep(5)
        locaton = []
        locations = self.driver.find_elements(MobileBy.XPATH, '//android.widget.TextView[@text="All"]')
        for location in locations:
            locaton.append(location.text)
        print(locaton)       
        df = pd.DataFrame(locaton)
        df.to_csv('locations.csv')
        # store to the Mongo DB
        client = MongoClient('localhost', 27017)
        db = client.test
        collection = db.locations
        collection.insert_many(locations)



    
    #get phone messages and how they were shared from facebook app
    def get_phone_messages(self):
        el3 = self.driver.find_element(MobileBy.CLASS_NAME, value="//android.widget.Button[@content-desc=\"Messaging\"]/android.view.View")
        el3.click()
        time.sleep(3)
        #go to recent chats
        el4 = self.driver.find_element(by=AppiumBy.ACCESSIBILITY_ID, value="The button to take the user to recent chats.")
        el4.click()
        # for each elf in the list of recent chats
        el5 = self.driver.find_element(by=AppiumBy.CLASS_NAME, value="/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.view.ViewGroup/android.view.ViewGroup/androidx.recyclerview.widget.RecyclerView/android.view.ViewGroup[6]/android.widget.FrameLayout/android.view.ViewGroup/android.view.ViewGroup")
        for el5 in el5:
            #click each chat and get the messages
            el5.click()
            time.sleep(3)
            #get the messages
            el6 = self.driver.find_element(by=AppiumBy.CLASS_NAME, value="/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.view.ViewGroup/android.view.ViewGroup/androidx.recyclerview.widget.RecyclerView/android.view.ViewGroup[6]/android.widget.FrameLayout/android.view.ViewGroup/android.view.ViewGroup")
        #el5.click()

        time.sleep(5)
        self.driver.find_element(MobileBy.XPATH, '//android.widget.TextView[@text="Phone"]').click()
        time.sleep(5)
    
    # get leaked phone numbers from facebook app
    def get_phone_numbers(self):
        self.driver.find_element(MobileBy.XPATH, '//android.widget.TextView[@text="Messages"]').click()
        time.sleep(5)
        self.driver.find_element(MobileBy.XPATH, '//android.widget.TextView[@text="Phone"]').click()
        time.sleep(5)
        self.driver.find_element(MobileBy.XPATH, '//android.widget.TextView[@text="Numbers"]').click()
        time.sleep(5)
        # access  the phonumbers and store them in a csv file
        contacts = []
        for i in range(1, 10):
            try:
                contact = self.driver.find_element(MobileBy.XPATH, '//android.widget.TextView[@index=' + str(i) + ']').text
                contacts.append(contact)
            except:
                pass
        df = pd.DataFrame(contacts)
        df.to_csv('phone_numbers.csv')
        # store the csv to mongo
        client = pymongo.MongoClient('localhost', 27017)
        db = client.test
        collection = db.phone_numbers
        collection.insert_many(df.to_dict('records'))

    # get user's friends from facebook app
    def get_user_friends(self):
        self.driver.find_element(MobileBy.XPATH, '//android.widget.TextView[@text="Messages"]').click()
        time.sleep(5)
        self.driver.find_element(MobileBy.XPATH, '//android.widget.TextView[@text="Friends"]').click()
        time.sleep(5)
        friends = []
        for i in range(1, 10):
            try:
                friend = self.driver.find_element(MobileBy.XPATH, '//android.widget.TextView[@index=' + str(i) + ']').text
                friends.append(friend)
            except:
                pass
        df = pd.DataFrame(friends)
        df.to_csv('friends.csv')
        # store the csv to mongo
        client = pymongo.MongoClient('localhost', 27017)
        db = client.test
        collection = db.friends
        collection.insert_many(df.to_dict('records'))

























