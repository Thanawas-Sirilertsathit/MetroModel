"""Make sure to run both backend and frontend server before testing."""
import time
from decouple import config
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select

options = Options()
options.add_argument("--start-maximized")
service = Service()
driver = webdriver.Chrome(service=service, options=options)
port = config("FRONTEND_PORT")

try:
    # Start driver and go to the website
    driver.get(port)
    time.sleep(3)

    # Wait for the search bar to be present
    wait = WebDriverWait(driver, 10)
    search_input = wait.until(EC.presence_of_element_located(
    (By.XPATH, "//input[@placeholder='Search for your train line here!']")
    ))
    time.sleep(3)

    # Type BTS into the search bar
    search_input.send_keys("BTS")
    search_input.send_keys(Keys.RETURN)
    time.sleep(3)

    # Click the view button for BTS organization
    view_button = wait.until(EC.element_to_be_clickable(
        (By.XPATH, "//button[contains(text(), 'View')]")
    ))
    view_button.click()
    time.sleep(3)

    # Find the graph presence in the bts detail page
    graph = wait.until(EC.presence_of_element_located(
        (By.TAG_NAME, "canvas")
    ))
    time.sleep(3)
    print("✅ Graph presence found. 1st Test passed.")

    # Verify the graph X-axis and Y-axis labels
    x_label = wait.until(EC.presence_of_element_located((By.ID, "x-label")))
    y_label = wait.until(EC.presence_of_element_located((By.ID, "y-label")))
    assert x_label.text == "Time (Hour)"
    assert y_label.text == "Passenger Count"
    time.sleep(3)
    print("✅ X and Y axis labels are correct. 2nd Test passed.")

    # Select the dropdown option to be temperature_c
    dropdown = wait.until(EC.presence_of_element_located((By.ID, "attribute")))
    select = Select(dropdown)
    select.select_by_value("temperature_c")
    time.sleep(3)

    # Verify the graph X-axis and Y-axis labels after selecting the dropdown option
    x_label = wait.until(EC.presence_of_element_located((By.ID, "x-label")))
    y_label = wait.until(EC.presence_of_element_located((By.ID, "y-label")))
    assert x_label.text == "Time (Hour)"
    assert y_label.text == "Temperature (°C)"
    time.sleep(3)
    print("✅ X and Y axis labels are changed so Y axis label is temperature. 3rd Test passed.")

    # Select the dropdown option to be humidity
    dropdown = wait.until(EC.presence_of_element_located((By.ID, "attribute")))
    select = Select(dropdown)
    select.select_by_value("humidity")
    time.sleep(3)

    # Verify the graph X-axis and Y-axis labels after selecting the dropdown option
    x_label = wait.until(EC.presence_of_element_located((By.ID, "x-label")))
    y_label = wait.until(EC.presence_of_element_located((By.ID, "y-label")))
    assert x_label.text == "Time (Hour)"
    assert y_label.text == "Humidity (%)"
    time.sleep(3)
    print("✅ X and Y axis labels are changed so Y axis label is humidity. 4th Test passed.")

    # Select the dropdown option to be pressure_mb
    dropdown = wait.until(EC.presence_of_element_located((By.ID, "attribute")))
    select = Select(dropdown)
    select.select_by_value("pressure_mb")
    time.sleep(3)

    # Verify the graph X-axis and Y-axis labels after selecting the dropdown option
    x_label = wait.until(EC.presence_of_element_located((By.ID, "x-label")))
    y_label = wait.until(EC.presence_of_element_located((By.ID, "y-label")))
    assert x_label.text == "Time (Hour)"
    assert y_label.text == "Pressure (mb)"
    time.sleep(3)
    print("✅ X and Y axis labels are changed so Y axis label is pressure. 5th Test passed.")

finally:
    # Close the webdriver
    driver.quit()
