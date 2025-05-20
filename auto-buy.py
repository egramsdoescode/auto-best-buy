from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from dotenv import load_dotenv
import os
import time

# Load form fields from .env
load_dotenv()

# Start firefox
driver = webdriver.Firefox()

# Go to airpods url
driver.get(os.getenv("PRODUCT_URL"))

# Add airpods to cart
add_button = driver.find_element(By.CSS_SELECTOR, "button[data-test-id='add-to-cart']")
add_button.click()

# Wait for next page to load after clicking
driver.implicitly_wait(60)

# Go to cart
wait = WebDriverWait(driver, 10)
go_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//a[@href='/cart']"))) 
go_button.click()

# Click checkout button
checkout_button = driver.find_element(By.CSS_SELECTOR, "button[data-track='Checkout - Top']")
checkout_button.click()

# Store guest checkout button
guest_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button.guest")))

# Click screen so that google popup goes away
driver.execute_script("document.body.click();")

# Click guest checkout button
guest_button.click()

# Wait until address apply button is visible before entering form fields
apply_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button[data-track='Shipping: Save shipping address']")))

fields = {
    "firstName": os.getenv("FIRST_NAME"),
    "lastName":  os.getenv("LAST_NAME"),
    "street":    os.getenv("STREET"),
    "city":      os.getenv("CITY"),
    "zipcode":   os.getenv("ZIPCODE")
}

# Input form fields
for field_id, value in fields.items():
    input_element = driver.find_element(By.CSS_SELECTOR, f"input#{field_id}")
    input_element.send_keys(value)

# Select the state
state_dropdown_el = driver.find_element(By.CSS_SELECTOR, "select#state")
state_dropdown = Select(state_dropdown_el)
state_dropdown.select_by_visible_text(os.getenv("STATE"))

time.sleep(3)
driver.quit()
