#!/usr/bin/python3
import json
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

# Configure logging
logging.basicConfig(level=logging.ERROR)

# Setup Chrome webdriver
options = webdriver.ChromeOptions()
options.add_argument('--headless')
options.add_argument('--disable-gpu')
options.add_argument('--disable-dev-shm-usage')
options.add_argument('--no-sandbox')
options.add_argument('--disable-plugins')
options.add_argument('--disable-extensions')
options.add_argument('--blink-settings=imagesEnabled=false')
driver = webdriver.Chrome(options=options)

try:
    # Open the login page
    driver.set_page_load_timeout(60)
    driver.get("http://192.168.1.242:8081/WebMC/users/login")

    # Wait for the JavaScript to load
    wait = WebDriverWait(driver, 5)

    # Input username and password
    username = wait.until(EC.presence_of_element_located((By.ID, 'UserUsernameShow')))
    password = driver.find_element(By.ID, 'UserPasswordShow')
    username.send_keys('zabbix')
    password.send_keys('zabbix')

    # Execute the JavaScript for encrypting credentials and submitting form
    driver.execute_script("""
    var username = document.getElementById('UserUsernameShow').value;
    var password = document.getElementById('UserPasswordShow').value;
    document.getElementById('UserUsername').value = EncryptPassword(username);
    document.getElementById('UserPassword').value = EncryptPassword(password);
    document.getElementById('UserLoginForm').submit();
    """)

    # Handle possible alert
    try:
        WebDriverWait(driver, 5).until(EC.alert_is_present())
        alert = driver.switch_to.alert
        alert.accept()
        logging.info("Alert accepted")
    except TimeoutException:
        logging.info("No alert was present.")

    # Wait for a specific element that signifies successful login
    WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.ID, 'Fea_Pbx_Cfg')))
    logging.info("Logged in! Dashboard is visible.")

    # Interactions and data collection
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, 'Fea_Pbx_Cfg'))).click()
    logging.info("Clicked on 'Fea_Pbx_Cfg'.")
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, 'Fea_Cfg'))).click()
    logging.info("Clicked on 'Fea_Cfg'.")
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, 'Fea_Slot'))).click()
    logging.info("Clicked on 'Fea_Slot'.")

    slot04_button = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'slot04')))
    ActionChains(driver).move_to_element(slot04_button).perform()
    logging.info("Hovered over 'slot04'.")

    card_status_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, 'cardStatus')))
    card_status_button.click()
    logging.info("Clicked on 'cardStatus'.")

    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'card_status')))
    statuses = {
        'Card': driver.find_element(By.ID, 'card_status').text.split(':')[1].strip(),
        'SYNC-ERR': driver.find_element(By.ID, 'syncerr_status').text.split(':')[1].strip(),
        'RAI': driver.find_element(By.ID, 'rai_status').text.split(':')[1].strip(),
        'AIS': driver.find_element(By.ID, 'ais_status').text.split(':')[1].strip(),
        'SYNC': driver.find_element(By.ID, 'sync_status').text.split(':')[1].strip()
    }

    # Output the collected data as JSON
    print(json.dumps(statuses, indent=2))
    
    #Popup Close
    #popupClose_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, 'popupClose')))
    #popupClose_button.click()
    #logging.info("Clicked on 'popupClose'.")
    
    # Logout process
    #logout_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//a[@onclick='goLogut()']")))
    #logout_button.click()
    #logging.info("Logged out successfully.")

except TimeoutException:
    logging.error("Failed to log in or the expected element was not found.")
finally:
    driver.quit()
