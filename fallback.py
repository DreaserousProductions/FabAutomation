import os
from logger import log_error

def handle_error(driver, error_message, screenshot_name="error.png"):
    log_error(error_message)
    
    # Create the logs directory if it doesn't exist
    logs_dir = os.path.join(os.getcwd(), "logs")
    if not os.path.exists(logs_dir):
        os.makedirs(logs_dir)

    # Save the screenshot in the logs directory
    screenshot_path = os.path.join(logs_dir, screenshot_name)
    driver.save_screenshot(screenshot_path)