from logger import log_error

def handle_error(driver, error_message, screenshot_name="error.png"):
    log_error(error_message)
    print(f"Error: {error_message}. Check logs for details.")
    
    # Take a screenshot for debugging
    driver.save_screenshot(screenshot_name)
    print(f"Screenshot saved as {screenshot_name}")
    
    # Ask user how they want to handle the error
    user_action = input("Do you want to (r)efresh the page, (c)ontinue, or (e)xit? (r/c/e): ").lower()

    if user_action == 'r':
        # Refresh the page if user chooses to do so
        driver.refresh()
        print("Page refreshed to attempt recovery.")
    elif user_action == 'c':
        # Continue with the execution
        print("Continuing with the process.")
    elif user_action == 'e':
        # Exit the script if user chooses to exit
        print("Exiting the script.")
        driver.quit()  # Optionally, close the driver
    else:
        # Invalid input
        print("Invalid choice. The script will continue.")
