import tkinter as tk
import os
import pandas as pd
import time
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from tkinter import filedialog

def clear_screen():
    os.system('cls')

def menu():
    print(f'''
    Welcome to the Data Entry System!
    Please select an option:
    1. Select the csv file to be read.{'Selected File: '+csv_name if csv_name else 'Nothing Selected yet.'}
        -Please check the format of the csv file.
    2. Enter the data onto Krishi Samagri.
    3. Enter the data onto Salt Trading.
    4. Exit the program.
        ''')

def validate(df:pd.DataFrame) -> bool:
    flag = True
    for index, row in df.iterrows():
        if len(str(row['phone'])) != 10:
            print(f'Invalid phone number {row['phone']} at index {index+1}.')
            flag = False
        year, month, day = row['Date'].split('/')
        if not year.isdigit() or not month.isdigit() or not day.isdigit():
            print(f'Invalid date {row['Date']} at index {index+1}.')
            flag = False
        else:
            if len(year) != 4 or int(month) < 1 or int(month) > 12 or int(day) < 1 or int(day) > 31:
                print(f'Invalid date {row['Date']} at index {index+1}.')
                flag = False
        if not row['Kilo'].isdigit():
            print(f'Invalid kilo {row['Kilo']} at index {index+1}.')
            flag = False
        if row['Details'].lower() not in ['u', 'd', 'p']:
            print(f'Invalid bag type {row['Details']} at index {index+1}.')
            flag = False
    return flag

def krishi():
    entry_details = pd.read_csv(
    csv_name, names=["Date", "Name", "Phone", "Details", "Kilo"]
)
    if not validate(entry_details):
        return
    driver.get("https://fms.kscl.gov.np/login")
    email_field = driver.find_element(By.NAME, "email")
    password_field = driver.find_element(By.NAME, "password") 
    submit_btn = driver.find_element(By.CSS_SELECTOR, ".btn")

    while 'login' in driver.current_url:
        email = input('Please enter your email: ')
        password = input('Please enter your password: ')

        email_field.send_keys(email)
        password_field.send_keys(password)
        submit_btn.click()

        if 'login' in driver.current_url:
            print('Invalid email or password. Please try again.')
        else:
            print('Logged in successfully.')

    for index, row in entry_details.iterrows():
        driver.get("https://fms.kscl.gov.np/sales/create/bulk")

        phone_field = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "input-consumer_phone"))
        )
        name_field = driver.find_element(By.ID, "input-consumer_name")
        kilo_field = driver.find_element(By.NAME, "kg[]")

        date = row["Date"].strip()
        name = row["Name"].strip()
        phone = row["Phone"]
        bag = row["Details"].strip()
        kilo = row["Kilo"]

        year = date.split("/")[0]
        month = date.split("/")[1]
        day = date.split("/")[2]
        

        if bag.lower() == "u":
            val = 1
        elif bag.lower() == "d":
            val = 2
        elif bag.lower() == "p":
            val = 3


        phone_field.clear()
        phone_field.send_keys(phone)
        name_field.send_keys(name)
        kilo_field.send_keys(kilo)

        tbl = driver.find_element(By.XPATH, '//*[@id="input-action_date"]')
        action.move_to_element(tbl).click().perform()
        
        time.sleep(0.3)
        year_select = Select(driver.find_element(By.ID, "ndp-year-select"))
        year_select.select_by_value(year)

        month_select = Select(driver.find_element(By.ID, "ndp-month-select"))
        month_select.select_by_value(month)
        
        if len(month) == 1:
            month = f"0{month}"
        if len(day) == 1:
            day = f"0{day}"
        table = driver.find_element(By.ID, "ndp-table")
        
        for i in table.find_elements(By.CLASS_NAME,"ndp-date"):
            value = i.find_element(By.TAG_NAME,"a")
            if value.get_attribute("data-value") == f"{year}-{month}-{day}":
                print("Clicked")
                value.click()
        
        dropdown = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.NAME, "commodity[]"))
        )
        dropdown.select_by_value(str(val))

        time.sleep(0.3)
        driver.find_element(By.CSS_SELECTOR, ".btn-success").click()
        assert driver.switch_to.alert.text == "Are you sure you want to Store ?"
        driver.switch_to.alert.accept()
        print(f"Entry for {name} on {date} is done.")

def salt_trading():
    entry_details = pd.read_csv(
    csv_name, names=["Date", "Name", "Phone", "Details", "Kilo"]
)
    if not validate(entry_details):
        return

    driver.get("https://stc.rarait.com/")
    email_field = driver.find_element(By.NAME, "email")
    password_field = driver.find_element(By.NAME, "password") 
    submit_btn = driver.find_element(By.CSS_SELECTOR, ".btn")
    
    while 'login' in driver.current_url:
        email = input('Please enter your email: ')
        password = input('Please enter your password: ')

        email_field.send_keys(email)
        password_field.send_keys(password)
        submit_btn.click()

        if 'login' in driver.current_url:
            print('Invalid email or password. Please try again.')
        else:
            print('Logged in successfully.')

    for index, row in entry_details.iterrows():
        driver.get("https://stc.rarait.com/sales/create/bulk")

        phone_field = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "input-consumer_phone"))
        )
        name_field = driver.find_element(By.ID, "input-consumer_name")
        kilo_field = driver.find_element(By.NAME, "kg[]")
        rate_field = driver.find_element(By.NAME, "rate[]")


        date = row["Date"].strip()
        name = row["Name"].strip()
        phone = row["Phone"]
        bag = row["Details"].strip()
        kilo = row["Kilo"]

        year = date.split("/")[0]
        month = date.split("/")[1]
        day = date.split("/")[2]
        

        if bag.lower() == "u":
            val = 3
            rate = 20
        elif bag.lower() == "d":
            val = 4
            rate = 49
        elif bag.lower() == "p":
            val = 5
            rate = 37

        phone_field.clear()
        phone_field.send_keys(phone)
        name_field.send_keys(name)
        kilo_field.send_keys(kilo)
        rate_field.clear()
        rate_field.send_keys(rate)

        tbl = driver.find_element(By.XPATH, '//*[@id="input-action_date"]')
        action.move_to_element(tbl).click().perform()
        
        time.sleep(0.3)
        year_select = Select(driver.find_element(By.ID, "ndp-year-select"))
        year_select.select_by_value(year)

        month_select = Select(driver.find_element(By.ID, "ndp-month-select"))
        month_select.select_by_value(month)
        
        if len(month) == 1:
            month = f"0{month}"
        if len(day) == 1:
            day = f"0{day}"
        table = driver.find_element(By.ID, "ndp-table")
        
        for i in table.find_elements(By.CLASS_NAME,"ndp-date"):
            value = i.find_element(By.TAG_NAME,"a")
            if value.get_attribute("data-value") == f"{year}-{month}-{day}":
                print("Clicked")
                value.click()
        
        dropdown = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.NAME, "commodity[]"))
        )
        dropdown.select_by_value(str(val))

        time.sleep(0.3)
        driver.find_element(By.CSS_SELECTOR, ".btn-success").click()
        assert driver.switch_to.alert.text == "Are you sure you want to Store ?"
        driver.switch_to.alert.accept()
        print(f"Entry for {name} on {date} is done.")


root = tk.Tk()
root.withdraw()
csv_file = None
csv_name = None

driver = webdriver.Chrome()
driver.get("https://google.com")
driver.implicitly_wait(10)
action = ActionChains(driver)

menu()
option = input('Please select an option: ')

while option != '4':
    if option == '1':
        currdir = os.getcwd()
        csv_file = filedialog.askopenfilename(initialdir=currdir, title='Please select a directory',filetypes=(('csv files', '*.csv'), ('all files', '*.*')))
        if csv_file:
            msg = 'You selected:', csv_file
            csv_name = os.path.basename(csv_file)
        else:
            msg = 'You did not select anything.'
    elif option == '2':
        if csv_file:
            krishi()
        else:
            print('You have not selected a csv file yet.')
    elif option == '3':
        if csv_file:
            salt_trading()
        else:
            print('You have not selected a csv file yet.')
    else:
        print('Invalid option. Please select a valid option.')
    
    clear_screen()
    menu()
    option = input('Please select an option: ')

