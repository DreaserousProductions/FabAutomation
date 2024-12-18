import os
import time
import subprocess
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from config import USER_DATA_DIR, USER_AGENT, WEBSITE_URL
from fallback import handle_error
from logger import log_info

# Kill all running chrome processes
def kill_existing_chrome():
    # For Windows
    if os.name == 'nt':
        subprocess.call(['taskkill', '/F', '/IM', 'chrome.exe'])
    # For Linux/macOS
    else:
        subprocess.call(["pkill", "chrome"])

def initialize_driver():
    kill_existing_chrome()

    # Configure Chrome options
    chrome_options = Options()
    chrome_options.add_argument(f"user-data-dir={USER_DATA_DIR}")
    chrome_options.add_argument(f"user-agent={USER_AGENT}")
    # chrome_options.add_argument("--headless")
    # chrome_options.add_argument("--disable-gpu")
    # chrome_options.add_argument("--no-sandbox")
    # chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:7898")
    chrome_options.add_experimental_option("excludeSwitches", ["enable-logging", "enable-automation"])
    driver_service = webdriver.ChromeService()

    # Initialize WebDriver
    driver = webdriver.Chrome(service=driver_service, options=chrome_options)
    return driver

def automate_listing_creation(folder_path, desc_text, cat_text, tags, price, pro_price, additional_desc, submit_for_review):
    driver = initialize_driver()
    try:
        driver.get(WEBSITE_URL)
        log_info(f"Opened URL: {WEBSITE_URL}")

        create_listings = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, '.fabkit-Hidden-down--mobile')))
        create_listings[1].click()

        asset_3d = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, '3d-model')))
        asset_3d.click()

        confirm_selection = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, '.fabkit-Button-root.fabkit-Button--md.fabkit-Button--primary')))
        if confirm_selection.get_attribute('aria-label') == "Confirm selected option: 3d-model":
            confirm_selection.click()
        
        input_list = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, '.tKmud1ea .fabkit-InputContainer-root.fabkit-InputContainer--md')))
        input_list[0].find_element(By.TAG_NAME, 'input').send_keys(folder_path.split("/")[-1])
        
        if desc_text:
            description = driver.find_element(By.CSS_SELECTOR, '.tiptap.ProseMirror.fabkit-RichEditor-content.fabkit-RichEditor-prose')
            driver.execute_script("arguments[0].innerHTML = arguments[1];", description, '<p>{}</p>'.format(desc_text))
        
        category = input_list[2].find_element(By.TAG_NAME, 'input')
        category.click()
        list_of_cats = driver.find_elements(By.CSS_SELECTOR, '.fabkit-Dropdown-container li')
        for i in list_of_cats:
            WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CLASS_NAME, 'fabkit-TreeSelectOption-label')))
            if i.find_element(By.CLASS_NAME, 'fabkit-TreeSelectOption-label').get_attribute('innerHTML').replace("&amp;", "&") == cat_text:
                i.click()
                break

        time.sleep(1)

        agreement_inputs = driver.find_elements(By.CSS_SELECTOR, '.fabkit-Radio-root.fabkit-Radio--md')
        agreement_inputs[0].click()

        time.sleep(1)

        price_inputs = driver.find_elements(By.CSS_SELECTOR, '.fabkit-InputContainer-root.fabkit-InputContainer--md')
        price_inputs[5].click()
        time.sleep(0.1)
        price_dropdown = driver.find_element(By.CLASS_NAME, 'fabkit-Dropdown-container')
        price_list = price_dropdown.find_elements(By.TAG_NAME, 'li')
        for i in price_list:
            if(i.get_attribute('innerHTML') == price):
                i.click()
                break
        time.sleep(1)
        price_inputs[6].click()
        time.sleep(0.1)
        pro_price_dropdown = driver.find_element(By.CLASS_NAME, 'fabkit-Dropdown-container')
        pro_price_list = pro_price_dropdown.find_elements(By.TAG_NAME, 'li')
        for i in pro_price_list:
            if(i.get_attribute('innerHTML') == pro_price):
                i.click()
                break

        tags_input = input_list[3].find_element(By.TAG_NAME, 'input')
        for i in tags:
            tags_input.send_keys(i)
            time.sleep(1)
            tags_input.send_keys(Keys.ARROW_DOWN)
            time.sleep(0.5)
            tags_input.send_keys(Keys.RETURN)
            time.sleep(0.5)
        
        preview_img_upload = driver.find_element(By.CSS_SELECTOR, "input.fabkit-ScreenReaderOnly-root")
        file_path = f"{folder_path}/preview_1.jpg"
        driver.execute_script("arguments[0].style.display = 'block';", preview_img_upload)
        preview_img_upload.send_keys(file_path)

        time.sleep(1)

        upload_images_btn = driver.find_element(By.CSS_SELECTOR, '.fabkit-Stack-root.fabkit-Stack--align_center.fabkit-scale--gapX-spacing-6.fabkit-scale--gapY-spacing-6.fabkit-Stack--column.fabkit-Surface-root.fabkit-Surface--outlined.fabkit-scale--radius-2.fabkit-scale--gutterX-spacing-6.fabkit-scale--gutterY-spacing-6 .fabkit-Button-root.fabkit-Button--md.fabkit-Button--primary')
        upload_images_btn.click()
        choose_img_dropdown = driver.find_elements(By.CSS_SELECTOR, '.fabkit-Dropdown-container .fabkit-List-item.fabkit-List--interactive.fabkit-List--rounded')
        choose_img_dropdown[0].click()
        upload_images_input = driver.find_element(By.CSS_SELECTOR, '.fabkit-Stack-root.fabkit-scale--gapX-layout-6.fabkit-scale--gapY-layout-6.fabkit-Stack--column.fabkit-Modal-content input.fabkit-ScreenReaderOnly-root')
        driver.execute_script("arguments[0].style.display = 'block';", upload_images_input)
        upload_images_input.send_keys("\n".join([os.path.join(folder_path, filename) for filename in os.listdir(folder_path) if filename.startswith("preview")]))
        confirm_btn = driver.find_element(By.CSS_SELECTOR, '.fabkit-Modal-container button.fabkit-Button-root.fabkit-Button--md.fabkit-Button--primary')
        confirm_btn.click()

        try:
            WebDriverWait(driver, 30).until(
                EC.invisibility_of_element_located((By.CSS_SELECTOR, ".fabkit-Modal-container"))
            )
        except Exception as e:
            print("Timed out waiting for modal to disappear.")

        agreement_inputs[2].click()

        time.sleep(0.1)

        driver.find_element(By.CSS_SELECTOR, '.fabkit-Checkbox-root.fabkit-Checkbox--md input').click()

        upload_model_btn = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.CSS_SELECTOR, ".fabkit-Surface-root.fabkit-Surface--outlined.fabkit-Surface--emphasis-background-elevated-high-default.fabkit-scale--radius-2.fabkit-scale--gutterX-spacing-5.fabkit-scale--gutterY-spacing-6.kUuzwc_J button.fabkit-Button-root.fabkit-Button--md.fabkit-Button--primary.fabkit-Button--fullWidth")))
        upload_model_btn.click()

        upload_buttons = WebDriverWait(driver, 5).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, '.fabkit-Stack-root.fabkit-Stack--align_center.fabkit-scale--gapX-spacing-4.fabkit-scale--gapY-spacing-4.fabkit-Surface-root.fabkit-Surface--emphasis-background-elevated-high-default.fabkit-scale--radius-2.fabkit-Surface--interactive.fabkit-scale--gutterX-spacing-3.fabkit-scale--gutterY-spacing-3.option.j6NLBb2a')))
        for i in upload_buttons:
            type_of_model = i.find_element(By.CSS_SELECTOR, '.fabkit-Typography-root.fabkit-Typography--align-start.fabkit-Typography--intent-primary.fabkit-Text--md.fabkit-Text--regular.fabkit-Stack-grow').get_attribute('innerHTML')
            if(type_of_model == 'OBJ'):
                i.click()
                driver.find_element(By.CSS_SELECTOR, '.fabkit-Modal-container button.fabkit-Button-root.fabkit-Button--md.fabkit-Button--primary').click()
                model_input = driver.find_element(By.CSS_SELECTOR, '.fabkit-Modal-container input.fabkit-ScreenReaderOnly-root')
                driver.execute_script("arguments[0].style.display = 'block';", model_input)
                model_input.send_keys(next((os.path.join(folder_path, filename) for filename in os.listdir(folder_path) if filename.endswith(".obj")), None))
                driver.find_element(By.CSS_SELECTOR, '.fabkit-Modal-container button.fabkit-Button-root.fabkit-Button--md.fabkit-Button--primary').click()
                break
        
        try:
            WebDriverWait(driver, 20).until(
                EC.invisibility_of_element_located((By.CSS_SELECTOR, ".fabkit-Modal-container"))
            )
        except Exception as e:
            print("Timed out waiting for modal to disappear.")
            
        upload_next_model_btn = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.CSS_SELECTOR, '.fabkit-Button-root.fabkit-Button--md.fabkit-Button--primary.fabkit-Button--fullWidth')))
        upload_next_model_btn.click()

        time.sleep(1)

        upload_buttons = WebDriverWait(driver, 5).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, '.fabkit-Stack-root.fabkit-Stack--align_center.fabkit-scale--gapX-spacing-4.fabkit-scale--gapY-spacing-4.fabkit-Surface-root.fabkit-Surface--emphasis-background-elevated-high-default.fabkit-scale--radius-2.fabkit-Surface--interactive.fabkit-scale--gutterX-spacing-3.fabkit-scale--gutterY-spacing-3.option.j6NLBb2a')))
        for i in upload_buttons:
            type_of_model = i.find_element(By.CSS_SELECTOR, '.fabkit-Typography-root.fabkit-Typography--align-start.fabkit-Typography--intent-primary.fabkit-Text--md.fabkit-Text--regular.fabkit-Stack-grow').get_attribute('innerHTML')
            if(type_of_model == 'FBX'):
                i.click()
                driver.find_element(By.CSS_SELECTOR, '.fabkit-Modal-container button.fabkit-Button-root.fabkit-Button--md.fabkit-Button--primary').click()
                model_input = driver.find_element(By.CSS_SELECTOR, '.fabkit-Modal-container input.fabkit-ScreenReaderOnly-root')
                driver.execute_script("arguments[0].style.display = 'block';", model_input)
                model_input.send_keys(next((os.path.join(folder_path, filename) for filename in os.listdir(folder_path) if filename.endswith(".fbx")), None))
                driver.find_element(By.CSS_SELECTOR, '.fabkit-Modal-container button.fabkit-Button-root.fabkit-Button--md.fabkit-Button--primary').click()
                break
        
        try:
            WebDriverWait(driver, 20).until(
                EC.invisibility_of_element_located((By.CSS_SELECTOR, ".fabkit-Modal-container"))
            )
        except Exception as e:
            print("Timed out waiting for modal to disappear.")

        time.sleep(1)

        upload_next_model_btn = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.CSS_SELECTOR, '.fabkit-Button-root.fabkit-Button--md.fabkit-Button--primary.fabkit-Button--fullWidth')))
        upload_next_model_btn.click()

        time.sleep(1)

        upload_buttons = WebDriverWait(driver, 5).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, '.fabkit-Stack-root.fabkit-Stack--align_center.fabkit-scale--gapX-spacing-4.fabkit-scale--gapY-spacing-4.fabkit-Surface-root.fabkit-Surface--emphasis-background-elevated-high-default.fabkit-scale--radius-2.fabkit-Surface--interactive.fabkit-scale--gutterX-spacing-3.fabkit-scale--gutterY-spacing-3.option.j6NLBb2a')))
        for i in upload_buttons:
            type_of_model = i.find_element(By.CSS_SELECTOR, '.fabkit-Typography-root.fabkit-Typography--align-start.fabkit-Typography--intent-primary.fabkit-Text--md.fabkit-Text--regular.fabkit-Stack-grow').get_attribute('innerHTML')
            if(type_of_model == 'GLB'):
                i.click()
                driver.find_element(By.CSS_SELECTOR, '.fabkit-Modal-container button.fabkit-Button-root.fabkit-Button--md.fabkit-Button--primary').click()
                model_input = driver.find_element(By.CSS_SELECTOR, '.fabkit-Modal-container input.fabkit-ScreenReaderOnly-root')
                driver.execute_script("arguments[0].style.display = 'block';", model_input)
                model_input.send_keys(next((os.path.join(folder_path, filename) for filename in os.listdir(folder_path) if filename.endswith(".glb")), None))
                driver.find_element(By.CSS_SELECTOR, '.fabkit-Modal-container button.fabkit-Button-root.fabkit-Button--md.fabkit-Button--primary').click()
                break

        try:
            WebDriverWait(driver, 20).until(
                EC.invisibility_of_element_located((By.CSS_SELECTOR, ".fabkit-Modal-container"))
            )
        except Exception as e:
            print("Timed out waiting for modal to disappear.")

        upload_next_model_btn = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.CSS_SELECTOR, '.fabkit-Button-root.fabkit-Button--md.fabkit-Button--primary.fabkit-Button--fullWidth')))
        upload_next_model_btn.click()

        time.sleep(1)

        upload_buttons =  WebDriverWait(driver, 5).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, '.fabkit-Stack-root.fabkit-Stack--align_center.fabkit-scale--gapX-spacing-4.fabkit-scale--gapY-spacing-4.fabkit-Surface-root.fabkit-Surface--emphasis-background-elevated-high-default.fabkit-scale--radius-2.fabkit-Surface--interactive.fabkit-scale--gutterX-spacing-3.fabkit-scale--gutterY-spacing-3.option.j6NLBb2a')))
        for i in upload_buttons:
            type_of_model = i.find_element(By.CSS_SELECTOR, '.fabkit-Typography-root.fabkit-Typography--align-start.fabkit-Typography--intent-primary.fabkit-Text--md.fabkit-Text--regular.fabkit-Stack-grow').get_attribute('innerHTML')
            if(type_of_model == 'Additional files'):
                i.click()
                driver.find_element(By.CSS_SELECTOR, '.fabkit-Modal-container button.fabkit-Button-root.fabkit-Button--md.fabkit-Button--primary').click()
                model_input = driver.find_element(By.CSS_SELECTOR, '.fabkit-Modal-container input.fabkit-ScreenReaderOnly-root')
                driver.execute_script("arguments[0].style.display = 'block';", model_input)
                model_input.send_keys(next((os.path.join(folder_path, filename) for filename in os.listdir(folder_path) if filename.endswith(".zip")), None))
                driver.find_element(By.CSS_SELECTOR, '.fabkit-Modal-container button.fabkit-Button-root.fabkit-Button--md.fabkit-Button--primary').click()
                break

        try:
            WebDriverWait(driver, 20).until(
                EC.invisibility_of_element_located((By.CSS_SELECTOR, ".fabkit-Modal-container"))
            )
        except Exception as e:
            print("Timed out waiting for modal to disappear.")
        
        time.sleep(1)
        
        if(additional_desc):
            add_desc = driver.find_element(By.CSS_SELECTOR, '.tiptap.ProseMirror.fabkit-RichEditor-content.fabkit-RichEditor-prose')
            driver.execute_script(f"arguments[0].innerHTML = '<p>{additional_desc}</p>';", add_desc)

        if(submit_for_review):
            submit_btn = driver.find_element(By.CSS_SELECTOR, '.fabkit-Button-root.fabkit-Button--md.fabkit-Button--primary')
            submit_btn.click()

            proceed_with_conversion_btn = driver.find_element(By.CSS_SELECTOR, '.fabkit-Modal-container .fabkit-Button-root.fabkit-Button--md.fabkit-Button--secondary')
            proceed_with_conversion_btn.click()

            final_confirmation_btn = driver.find_element(By.CSS_SELECTOR, '.fabkit-Modal-container .fabkit-Button-root.fabkit-Button--md.fabkit-Button--primary')
            final_confirmation_btn.click()

            close_btn = driver.find_element(By.CSS_SELECTOR, '.fabkit-Modal-container .fabkit-Button-root.fabkit-Button--md.fabkit-Button--primary')
            close_btn.click()
        else:
            time.sleep(2)
            # driver.find_element(By.CSS_SELECTOR, '.fabkit-Typography-root.fabkit-Typography--align-start.fabkit-Typography--intent-primary.fabkit-Paragraph--sm.fabkit-Paragraph--regular.fabkit-Link-root.fabkit-Link--primary.fabkit-Stack-root.fabkit-Stack--align_center.fabkit-scale--gapX-spacing-1.fabkit-scale--gapY-spacing-1').click()

    except NoSuchElementException as e:
        handle_error(driver, "Element not found: " + str(e))
    except Exception as e:
        handle_error(driver, "Unexpected error: " + str(e))
    finally:
        time.sleep(2)
        driver.quit()
        log_info("Driver closed.")

def bulk_draft_deletion():
    driver = initialize_driver()
    try:
        driver.get(WEBSITE_URL)
        log_info(f"Opened URL: {WEBSITE_URL}")
        time.sleep(2)

        while True:
            time.sleep(1)
            # Re-fetch listings every iteration
            check_listing = driver.find_element(By.CSS_SELECTOR, '.fabkit-ResultGrid-root.fabkit-ResultGrid-col--sm.fabkit-Grid-root.fabkit-scale--gapX-layout-6.fabkit-scale--gapY-layout-6')
            
            # If no listings are left, break the loop
            if not check_listing:
                break

            listings = check_listing.find_elements(By.TAG_NAME, 'li')

            # Check the first listing
            first_listing = listings[0]  # Always target the first listing
            badge_label = first_listing.find_element(By.CSS_SELECTOR, '.fabkit-Badge-root.fabkit-Badge--filled.fabkit-Badge--gray.fabkit-Badge--sm.njpEEPcc .fabkit-Badge-label')

            # Check if the badge label is "Draft"
            if badge_label.get_attribute('innerHTML') == 'Draft':
                three_dot = first_listing.find_element(By.CSS_SELECTOR, '.fabkit-Button-root.fabkit-Button--icon.fabkit-Button--sm.fabkit-Button--ghost')
                three_dot.click()

                # Click the delete option
                delete_listing = driver.find_elements(By.CSS_SELECTOR, '.fabkit-List-item.fabkit-List--interactive.fabkit-List--rounded')
                if delete_listing and len(delete_listing) > 1:
                    delete_listing[1].click()

                # Click the delete button
                delete_btn = driver.find_element(By.CSS_SELECTOR, '.fabkit-Button-root.fabkit-Button--md.fabkit-Button--critical')
                delete_btn.click()

                log_info("A draft has been deleted")
                
                # Allow time for UI to update after deletion
                time.sleep(1)

    except NoSuchElementException as e:
        print("EOF")
    except Exception as e:
        handle_error(driver, "Unexpected error: " + str(e))
    finally:
        driver.quit()
        log_info("Driver closed.")