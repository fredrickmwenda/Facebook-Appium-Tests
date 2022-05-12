import time
import os
import sys

def main():
    from appium-test import Action
    
    leakTest = Action()
    leakTest.get_private_messages()
    leakTest.get_contact_list()
    leakTest.get_phone_numbers()
    leakTest.get_user_all_locations()

if __name__ == '__main__':
    main()


