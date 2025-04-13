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
    driver.get(port)
    time.sleep(3)
    wait = WebDriverWait(driver, 10)
    search_input = wait.until(EC.presence_of_element_located(
        (By.XPATH, "//input[@placeholder='Search for your train line here!']")
    ))
    time.sleep(3)
    search_input.send_keys("BTS")
    search_input.send_keys(Keys.RETURN)
    time.sleep(3)
    view_button = wait.until(EC.element_to_be_clickable(
        (By.XPATH, "//button[contains(text(), 'View')]")
    ))
    view_button.click()
    time.sleep(3)

    # Check graph presence
    try:
        graph = wait.until(EC.presence_of_element_located((By.TAG_NAME, "canvas")))
        time.sleep(3)
        print("✅ Graph presence found. 1st Test passed.")
    except Exception as e:
        print("❌ Failed to find graph on detail page. 1st Test failed.", e)

    # Verify axis labels to match with Passenger Count
    try:
        x_label = wait.until(EC.presence_of_element_located((By.ID, "x-label")))
        y_label = wait.until(EC.presence_of_element_located((By.ID, "y-label")))
        assert x_label.text == "Time (Hour)"
        assert y_label.text == "Passenger Count"
        time.sleep(3)
        print("✅ X and Y axis labels are correct. 2nd Test passed.")
    except AssertionError:
        print(f"❌ Axis label mismatch. Expected Y: 'Passenger Count', got: '{y_label.text}'. 2nd Test failed.")
    except Exception as e:
        print("❌ Error checking axis labels. 2nd Test failed.", e)

    # Verify axis labels to match with Temperature
    try:
        dropdown = wait.until(EC.presence_of_element_located((By.ID, "attribute")))
        select = Select(dropdown)
        select.select_by_value("temperature_c")
        time.sleep(3)
        x_label = wait.until(EC.presence_of_element_located((By.ID, "x-label")))
        y_label = wait.until(EC.presence_of_element_located((By.ID, "y-label")))
        assert x_label.text == "Time (Hour)"
        assert y_label.text == "Temperature (°C)"
        time.sleep(3)
        print("✅ Y axis changed to Temperature. 3rd Test passed.")
    except AssertionError:
        print(f"❌ Axis label mismatch. Expected Y: 'Temperature (°C)', got: '{y_label.text}'. 3rd Test failed.")
    except Exception as e:
        print("❌ Error selecting temperature_c or checking labels. 3rd Test failed.", e)

    # Verify axis labels to match with Humidity
    try:
        select.select_by_value("humidity")
        time.sleep(3)
        x_label = wait.until(EC.presence_of_element_located((By.ID, "x-label")))
        y_label = wait.until(EC.presence_of_element_located((By.ID, "y-label")))
        assert x_label.text == "Time (Hour)"
        assert y_label.text == "Humidity (%)"
        time.sleep(3)
        print("✅ Y axis changed to Humidity. 4th Test passed.")
    except AssertionError:
        print(f"❌ Axis label mismatch. Expected Y: 'Humidity (%)', got: '{y_label.text}'. 4th Test failed.")
    except Exception as e:
        print("❌ Error selecting humidity or checking labels. 4th Test failed.", e)

    # Verify axis labels to match with Pressure
    try:
        select.select_by_value("pressure_mb")
        time.sleep(3)
        x_label = wait.until(EC.presence_of_element_located((By.ID, "x-label")))
        y_label = wait.until(EC.presence_of_element_located((By.ID, "y-label")))
        assert x_label.text == "Time (Hour)"
        assert y_label.text == "Pressure (mb)"
        time.sleep(3)
        print("✅ Y axis changed to Pressure. 5th Test passed.")
    except AssertionError:
        print(f"❌ Axis label mismatch. Expected Y: 'Pressure (mb)', got: '{y_label.text}'. 5th Test failed.")
    except Exception as e:
        print("❌ Error selecting pressure_mb or checking labels. 5th Test failed.", e)

finally:
    driver.quit()
