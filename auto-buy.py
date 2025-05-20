import selenium
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
wait = WebDriverWait(driver, 10)

# Add airpods to cart
add_button = driver.find_element(By.CSS_SELECTOR, "button[data-test-id='add-to-cart']") 
add_button.click()

# Wait for next page to load after clicking
driver.implicitly_wait(60)

# Go to cart
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

shipping_fields = {
    "firstName": os.getenv("FIRST_NAME"),
    "lastName":  os.getenv("LAST_NAME"),
    "street":    os.getenv("STREET"),
    "street2":   os.getenv("STREET2"),
    "city":      os.getenv("CITY"),
    "zipcode":   os.getenv("ZIPCODE")
}

show_apt = driver.find_element(By.CSS_SELECTOR, "button[class='c-button-link address-form__showAddress2Link']")
show_apt.click()

# Input form fields
for field_id, value in shipping_fields.items():
    input_element = driver.find_element(By.CSS_SELECTOR, f"input#{field_id}")
    input_element.send_keys(value)

# Select the state
state_dropdown_el = driver.find_element(By.CSS_SELECTOR, "select#state")
state_dropdown = Select(state_dropdown_el)
state_dropdown.select_by_visible_text(os.getenv("STATE"))

address_checkbox = driver.find_element(By.CSS_SELECTOR, "span[class='c-checkbox-brand']")

# Scroll into view
driver.execute_script("arguments[0].scrollIntoView(true);", address_checkbox)
address_checkbox.click()
 
apply_button.click()

WebDriverWait(driver, 15).until(
    EC.invisibility_of_element_located((By.CSS_SELECTOR, "i[class='spinner spinner-large']"))
)

print("I am after spinning wait part 1")

contact_fields = {
    "user.emailAddress":      os.getenv("EMAIL"),
    "user.phone":             os.getenv("PHONE")
}

for field_id, value in contact_fields.items():
    input_element = driver.find_element(By.CSS_SELECTOR, f"input[id='{field_id}']")
    input_element.send_keys(value)

WebDriverWait(driver, 15).until(
    EC.invisibility_of_element_located((By.CSS_SELECTOR, "i[class='spinner spinner-large']"))
)

print("I am after spinning wait part 2")
continue_to_payment = driver.find_element(By.CSS_SELECTOR, "button[class='btn btn-lg btn-block btn-secondary']")
continue_to_payment.click()
