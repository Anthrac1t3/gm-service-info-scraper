import sys
import os
import time

from selenium import webdriver
from selenium.common import NoSuchElementException
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


base_url = 'https://www.acdelcotds.com/'


def process_hitlist(passed_driver: webdriver.Firefox):
    #try:
    #    hits = passed_driver.find_elements(By.CLASS_NAME, 'hitListLink')
    #except NoSuchElementException as e:
    pass


if __name__ == "__main__":
    username = sys.argv[1]
    password = sys.argv[2]
    print(f'Username: {username}, Password: {password}')

    # Set up the Firefox browser_profile for printing
    firefox_options = Options()
    firefox_options.set_preference("print.always_print_silent", True)  # Suppress print dialog
    firefox_options.set_preference("print_printer", "Mozilla Save to PDF")  # Set "Save to PDF" as default printer
    firefox_options.set_preference("print.printer_Mozilla_Save_to_PDF.print_to_file", True)
    firefox_options.set_preference("print.printer_Mozilla_Save_to_PDF.print_bgcolor", True)
    #firefox_options.set_preference("print.printer_Mozilla_Save_to_PDF.print_to_filename",
    #                               "C:\\Users\\coler\\Downloads\\test.pdf")  # Output file location

    # Set up the Firefox driver
    driver = webdriver.Firefox(options=firefox_options)

    # Navigate to acdelco site
    driver.get(base_url)

    # Login to site
    try:
        # Wait for login button to load
        login_form_element = WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.XPATH, '/html/body/div/div/div[1]/nav/div/ul/ul/li[1]/div/span/div/a'))
        )
        # Click it when it's loaded
        login_form_element.click()

        # Wait for username input to load
        username_element = WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="loginId"]'))
        )
        username_element.send_keys(username)

        password_element = driver.find_element(By.XPATH, '//*[@id="loginPw"]')
        password_element.send_keys(password)

        login_button_element = driver.find_element(By.XPATH, '/html/body/div/div/div[1]/nav/div/ul/ul/li[1]/div/span/div/div/div/div[2]/div/form/button')
        login_button_element.click()

    except Exception as e:
        print(f"ERROR: {e}")
        driver.close()

    if input('Navigate to service info page and please press enter: ') == '':
        driver.switch_to.window(driver.window_handles[1])
        publications = driver.find_elements(By.CLASS_NAME, 'hitListLink')

        print(len(publications))
        print(publications)

        # save as pdf
        #root = driver.find_element(By.TAG_NAME, 'html')
        #root.screenshot(os.path.join('C:\\Users\\coler\\Downloads', 'test.png'))
        driver.execute_script('window.print();')

        time.sleep(30)


    # Close up the windows
    #driver.close()
    #driver.switch_to.window(driver.window_handles[0])
    driver.quit()
