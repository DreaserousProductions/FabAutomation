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
from selenium_stealth import stealth
from config import USER_DATA_DIR, USER_AGENT, WEBSITE_URL
from fallback import handle_error
from logger import log_info
from automation_func import (
    info_init, price_select, upload_images_func, file_upload, file_upload_next,
    edit_init, delete_init, delete_commit
    )

def kill_existing_chrome():
    if os.name == 'nt':
        subprocess.call(['taskkill', '/F', '/IM', 'chrome.exe'])
    else:
        subprocess.call(["pkill", "chrome"])

def initialize_driver(headless=False):
    kill_existing_chrome()

    # Configure Chrome options
    chrome_options = Options()
    chrome_options.add_argument(f"user-data-dir={USER_DATA_DIR}")
    chrome_options.add_argument(f"user-agent={USER_AGENT}")
    chrome_options.add_argument('--log-level=3')  # Suppress logs
    chrome_options.add_argument('--disable-logging')  # Disable logging
    if(headless):
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--no-sandbox")
    chrome_options.add_experimental_option("excludeSwitches", ["enable-logging", "enable-automation"])
    chrome_options.add_experimental_option('useAutomationExtension', False)
    driver_service = webdriver.ChromeService()

    # Initialize WebDriver
    driver = webdriver.Chrome(service=driver_service, options=chrome_options)

    stealth(driver,
        languages=["en-US", "en"],
        vendor="Google Inc.",
        platform="Win32",
        webgl_vendor="Intel Inc.",
        renderer="Intel Iris OpenGL Engine",
        fix_hairline=True,
        )
    
    return driver

def automate_listing_creation(headless, folder_path, desc_text, cat_text, tags, price, pro_price, additional_desc, submit_for_review, product_type):
    driver = initialize_driver(headless)
    try:
        driver.get(WEBSITE_URL)
        log_info(f"Opened URL: {WEBSITE_URL}")

        info_init(driver, product_type)
        
        # =========================== Information Input Page =========================== #
        input_list = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, '.tKmud1ea .fabkit-InputContainer-root.fabkit-InputContainer--md')))
        
        # Model Title ===========================
        title_box = input_list[0].find_element(By.TAG_NAME, 'input')
        title_box.send_keys(folder_path.split("/")[-1])
        
        # Description Text ===========================
        if desc_text:
            description = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, '.tiptap.ProseMirror.fabkit-RichEditor-content.fabkit-RichEditor-prose')))
            driver.execute_script("arguments[0].innerHTML = arguments[1];", description, '<p>{}</p>'.format(desc_text))
        
        # Category of Model ===========================
        category = input_list[2].find_element(By.TAG_NAME, 'input')
        category.click()
        list_of_cats = WebDriverWait(driver, 20).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, '.fabkit-Dropdown-container li .fabkit-TreeSelectOption-label')))
        for i in list_of_cats:
            if i.get_attribute('innerHTML').replace("&amp;", "&") == cat_text:
                i.click()
                break
        
        # License type & price ===========================
        agreement_inputs = WebDriverWait(driver, 20).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, '.fabkit-Radio-root.fabkit-Radio--md')))
        agreement_inputs[0].click()

        price_inputs = WebDriverWait(driver, 20).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, '.fabkit-InputContainer-root.fabkit-InputContainer--md')))
        price_inputs[5].click()

        price_select(driver, price)

        time.sleep(0.1)
        price_inputs[6].click()
        time.sleep(0.1)

        price_select(driver, pro_price)

        # Product Tags ===========================
        tags_input = input_list[3].find_element(By.TAG_NAME, 'input')
        for i in tags:
            tags_input.send_keys(i)
            time.sleep(1)
            tags_input.send_keys(Keys.ARROW_DOWN)
            time.sleep(0.1)
            tags_input.send_keys(Keys.RETURN)
            time.sleep(0.1)
        
        # Product Preview Image ===========================
        preview_img_upload = driver.find_element(By.CSS_SELECTOR, "input.fabkit-ScreenReaderOnly-root")
        file_path = f"{folder_path}/preview_1.jpg"
        driver.execute_script("arguments[0].style.display = 'block';", preview_img_upload)
        preview_img_upload.send_keys(file_path)

        upload_images_func(driver, folder_path, True)

        time.sleep(0.1)
        agreement_inputs[2].click() # Mature content
        time.sleep(0.1)
        driver.find_element(By.CSS_SELECTOR, '.fabkit-Checkbox-root.fabkit-Checkbox--md input').click() # Disallow use by Generative AI Programs
        time.sleep(0.1)

        if(product_type == "3D Model"):
            file_upload(driver, folder_path, "OBJ", ".obj")
            file_upload_next(driver, folder_path, "FBX", ".fbx")
            file_upload_next(driver, folder_path, "GLB", ".glb")
            file_upload_next(driver, folder_path, "Additional files", ".zip", True, additional_desc)
        else:
            file_upload(driver, folder_path, "Additional files", ".zip", True, additional_desc)

        if(submit_for_review):
            submit_btn = driver.find_element(By.CSS_SELECTOR, '.fabkit-Button-root.fabkit-Button--md.fabkit-Button--primary')
            submit_btn.click()
            time.sleep(0.1)
            proceed_with_conversion_btn = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, '.fabkit-Modal-container .fabkit-Button-root.fabkit-Button--md.fabkit-Button--secondary')))
            proceed_with_conversion_btn.click()
            time.sleep(0.1)
            final_confirmation_btn = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, '.fabkit-Modal-container .fabkit-Button-root.fabkit-Button--md.fabkit-Button--primary')))
            final_confirmation_btn.click()
            time.sleep(0.1)

    except NoSuchElementException as e:
        handle_error(driver, "Element not found: " + str(e) + f"\n{folder_path}")
    except Exception as e:
        handle_error(driver, "Unexpected error: " + str(e) + f"\n{folder_path}")
    finally:
        time.sleep(2)
        driver.quit()
        log_info("Driver closed.")

def automate_listing_creation_bulk(headless, m_folder_path, desc_text, cat_text, tags, price, pro_price, additional_desc, submit_for_review, product_type, progress_signal):
    driver = initialize_driver(headless)
    fin_lis = []

    total_folders = sum(len(dirs) for _, dirs, _ in os.walk(m_folder_path))
    completed_folders = 0
    for root, dirs, files in os.walk(m_folder_path):
            for dir_name in dirs:
                folder_path = f"{root}/{dir_name}"
                try:
                    driver.get(WEBSITE_URL)
                    log_info(f"Opened URL: {WEBSITE_URL}")

                    info_init(driver, product_type)
                    
                    # =========================== Information Input Page =========================== #
                    input_list = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, '.tKmud1ea .fabkit-InputContainer-root.fabkit-InputContainer--md')))
                    
                    # Model Title ===========================
                    title_box = input_list[0].find_element(By.TAG_NAME, 'input')
                    title_box.send_keys(folder_path.split("/")[-1])
                    
                    # Description Text ===========================
                    if desc_text:
                        description = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, '.tiptap.ProseMirror.fabkit-RichEditor-content.fabkit-RichEditor-prose')))
                        driver.execute_script("arguments[0].innerHTML = arguments[1];", description, '<p>{}</p>'.format(desc_text))
                    
                    # Category of Model ===========================
                    category = input_list[2].find_element(By.TAG_NAME, 'input')
                    category.click()
                    list_of_cats = WebDriverWait(driver, 20).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, '.fabkit-Dropdown-container li .fabkit-TreeSelectOption-label')))
                    for i in list_of_cats:
                        if i.get_attribute('innerHTML').replace("&amp;", "&") == cat_text:
                            i.click()
                            break
                    
                    # License type & price ===========================
                    agreement_inputs = WebDriverWait(driver, 20).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, '.fabkit-Radio-root.fabkit-Radio--md')))
                    agreement_inputs[0].click()

                    price_inputs = WebDriverWait(driver, 20).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, '.fabkit-InputContainer-root.fabkit-InputContainer--md')))
                    price_inputs[5].click()

                    price_select(driver, price)

                    time.sleep(0.1)
                    price_inputs[6].click()
                    time.sleep(0.1)

                    price_select(driver, pro_price)

                    # Product Tags ===========================
                    tags_input = input_list[3].find_element(By.TAG_NAME, 'input')
                    for i in tags:
                        tags_input.send_keys(i)
                        time.sleep(1)
                        tags_input.send_keys(Keys.ARROW_DOWN)
                        time.sleep(0.1)
                        tags_input.send_keys(Keys.RETURN)
                        time.sleep(0.1)
                    
                    # Product Preview Image ===========================
                    preview_img_upload = driver.find_element(By.CSS_SELECTOR, "input.fabkit-ScreenReaderOnly-root")
                    file_path = f"{folder_path}/preview_1.jpg"
                    driver.execute_script("arguments[0].style.display = 'block';", preview_img_upload)
                    preview_img_upload.send_keys(file_path)

                    upload_images_func(driver, folder_path, True)

                    time.sleep(0.1)
                    agreement_inputs[2].click() # Mature content
                    time.sleep(0.1)
                    driver.find_element(By.CSS_SELECTOR, '.fabkit-Checkbox-root.fabkit-Checkbox--md input').click() # Disallow use by Generative AI Programs
                    time.sleep(0.1)

                    if(product_type == "3D Model"):
                        file_upload(driver, folder_path, "OBJ", ".obj")
                        file_upload_next(driver, folder_path, "FBX", ".fbx")
                        file_upload_next(driver, folder_path, "GLB", ".glb")
                        file_upload_next(driver, folder_path, "Additional files", ".zip", True, additional_desc)
                    else:
                        file_upload(driver, folder_path, "Additional files", ".zip", True, additional_desc)

                    if(submit_for_review):
                        submit_btn = driver.find_element(By.CSS_SELECTOR, '.fabkit-Button-root.fabkit-Button--md.fabkit-Button--primary')
                        submit_btn.click()
                        time.sleep(0.1)
                        proceed_with_conversion_btn = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, '.fabkit-Modal-container .fabkit-Button-root.fabkit-Button--md.fabkit-Button--secondary')))
                        proceed_with_conversion_btn.click()
                        time.sleep(0.1)
                        final_confirmation_btn = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, '.fabkit-Modal-container .fabkit-Button-root.fabkit-Button--md.fabkit-Button--primary')))
                        final_confirmation_btn.click()
                        time.sleep(0.1)

                    # Increment completed count and update progress
                    completed_folders += 1
                    progress_signal.emit(completed_folders / total_folders)

                    fin_lis.append(folder_path)
                except NoSuchElementException as e:
                    handle_error(driver, "Element not found: " + str(e) + f"\n{folder_path}")
                except Exception as e:
                    handle_error(driver, "Unexpected error: " + str(e) + f"\n{folder_path}")
                finally:
                    time.sleep(3)

                    log_info(folder_path)

    driver.quit()
    log_info("Driver Closed")
    return fin_lis

def automate_listing_edit(headless, folder_path, tags, price, pro_price, additional_desc, submit_for_review):
    driver = initialize_driver(headless)
    try:
        driver.get(WEBSITE_URL)
        log_info(f"Opened URL: {WEBSITE_URL}")

        edit_init(driver, folder_path.split('/')[-1])

        # =========================== Information Input Page =========================== #
        # License type & price ===========================
        agreement_inputs = WebDriverWait(driver, 20).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, '.fabkit-Radio-root.fabkit-Radio--md')))
        agreement_inputs[0].click()

        price_inputs = WebDriverWait(driver, 20).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, '.fabkit-InputContainer-root.fabkit-InputContainer--md')))
        price_inputs[5].click()

        price_select(driver, price)

        time.sleep(0.1)
        price_inputs[6].click()
        time.sleep(0.1)

        price_select(driver, pro_price)
        time.sleep(0.1)

        # Product Tags ===========================
        tags_input = driver.find_element(By.CSS_SELECTOR, 'input[aria-describedby=" tagsDesc tagsCount"]')
        p_tags = driver.find_elements(By.CSS_SELECTOR, '.fabkit-Tag-root.fabkit-Tag--md.fabkit-Tag--deletable span')
        p_lis = [i.get_attribute('innerHTML') for i in p_tags]
        for i in tags:
            if i not in p_lis:
                tags_input.send_keys(i)
                time.sleep(1)
                tags_input.send_keys(Keys.ARROW_DOWN)
                time.sleep(0.1)
                tags_input.send_keys(Keys.RETURN)
                time.sleep(0.1)
        
        # Product Preview Image ===========================
        preview_img_upload = driver.find_element(By.CSS_SELECTOR, "input.fabkit-ScreenReaderOnly-root")
        file_path = f"{folder_path}/preview_1.jpg"
        driver.execute_script("arguments[0].style.display = 'block';", preview_img_upload)
        preview_img_upload.send_keys(file_path)

        previous_images_close = WebDriverWait(driver, 20).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, '.fabkit-XButton-root.fabkit-XButton--solid.fabkit-XButton--sm.Nu5QNzvD')))
        renew = False
        for i in range(len(previous_images_close)):
            time.sleep(1)
            previous_images_close = WebDriverWait(driver, 20).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, '.fabkit-XButton-root.fabkit-XButton--solid.fabkit-XButton--sm.Nu5QNzvD')))
            if(renew):
                previous_images_close[1].click()
            else:
                previous_images_close[0].click()
            try:
                time.sleep(0.1)
                close_btn = driver.find_element(By.CSS_SELECTOR, ".fabkit-Modal-container .fabkit-XButton-root.fabkit-XButton--ghost.fabkit-XButton--lg.fabkit-Modal-closeButton")
                close_btn.click()
                renew = True
            except:
                ...

        time.sleep(1)

        upload_images_func(driver, folder_path, not renew)

        time.sleep(0.1)
        agreement_inputs[2].click() # Mature content
        time.sleep(0.1)
        driver.find_element(By.CSS_SELECTOR, '.fabkit-Checkbox-root.fabkit-Checkbox--md input').click() # Disallow use by Generative AI Programs
        time.sleep(0.1)

        file_upload_next(driver, folder_path, "OBJ", ".obj")
        file_upload_next(driver, folder_path, "FBX", ".fbx")
        file_upload_next(driver, folder_path, "Additional files", ".zip", True, additional_desc)

        # Submit for Review or Safe as draft ===========================
        if(submit_for_review):
            submit_btn = driver.find_element(By.CSS_SELECTOR, '.fabkit-Button-root.fabkit-Button--md.fabkit-Button--primary')
            submit_btn.click()
            time.sleep(0.1)
            proceed_with_conversion_btn = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, '.fabkit-Modal-container .fabkit-Button-root.fabkit-Button--md.fabkit-Button--secondary')))
            proceed_with_conversion_btn.click()
            time.sleep(0.1)
            final_confirmation_btn = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, '.fabkit-Modal-container .fabkit-Button-root.fabkit-Button--md.fabkit-Button--primary')))
            final_confirmation_btn.click()
            time.sleep(0.1)

    except NoSuchElementException as e:
        handle_error(driver, "Element not found: " + str(e) + f"\n{folder_path}")
    except Exception as e:
        handle_error(driver, "Unexpected error: " + str(e) + f"\n{folder_path}")
    finally:
        time.sleep(2)
        driver.quit()
        log_info("Driver closed.")

def automate_listing_edit_bulk(headless, m_folder_path, tags, price, pro_price, additional_desc, submit_for_review, progress_signal):
    driver = initialize_driver(headless)
    fin_lis = []

    total_folders = sum(len(dirs) for _, dirs, _ in os.walk(m_folder_path))
    completed_folders = 0
    for root, dirs, files in os.walk(m_folder_path):
            for dir_name in dirs:
                folder_path = f"{root}/{dir_name}"
                try:
                    driver.get(WEBSITE_URL)
                    log_info(f"Opened URL: {WEBSITE_URL}")

                    edit_init(driver, folder_path.split('/')[-1])

                    # =========================== Information Input Page =========================== #
                    # License type & price ===========================
                    agreement_inputs = WebDriverWait(driver, 20).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, '.fabkit-Radio-root.fabkit-Radio--md')))
                    agreement_inputs[0].click()

                    price_inputs = WebDriverWait(driver, 20).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, '.fabkit-InputContainer-root.fabkit-InputContainer--md')))
                    price_inputs[5].click()

                    price_select(driver, price)

                    time.sleep(0.1)
                    price_inputs[6].click()
                    time.sleep(0.1)

                    price_select(driver, pro_price)
                    time.sleep(0.1)

                    # Product Tags ===========================
                    tags_input = driver.find_element(By.CSS_SELECTOR, 'input[aria-describedby=" tagsDesc tagsCount"]')
                    p_tags = driver.find_elements(By.CSS_SELECTOR, '.fabkit-Tag-root.fabkit-Tag--md.fabkit-Tag--deletable span')
                    p_lis = [i.get_attribute('innerHTML') for i in p_tags]
                    for i in tags:
                        if i not in p_lis:
                            tags_input.send_keys(i)
                            time.sleep(1)
                            tags_input.send_keys(Keys.ARROW_DOWN)
                            time.sleep(0.1)
                            tags_input.send_keys(Keys.RETURN)
                            time.sleep(0.1)
                    
                    # Product Preview Image ===========================
                    preview_img_upload = driver.find_element(By.CSS_SELECTOR, "input.fabkit-ScreenReaderOnly-root")
                    file_path = f"{folder_path}/preview_1.jpg"
                    driver.execute_script("arguments[0].style.display = 'block';", preview_img_upload)
                    preview_img_upload.send_keys(file_path)

                    time.sleep(1)

                    previous_images_close = WebDriverWait(driver, 20).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, '.fabkit-XButton-root.fabkit-XButton--solid.fabkit-XButton--sm.Nu5QNzvD')))
                    renew = False
                    for i in range(len(previous_images_close)):
                        time.sleep(1)
                        previous_images_close = WebDriverWait(driver, 20).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, '.fabkit-XButton-root.fabkit-XButton--solid.fabkit-XButton--sm.Nu5QNzvD')))
                        if(renew):
                            previous_images_close[1].click()
                        else:
                            previous_images_close[0].click()
                        try:
                            time.sleep(0.1)
                            close_btn = driver.find_element(By.CSS_SELECTOR, ".fabkit-Modal-container .fabkit-XButton-root.fabkit-XButton--ghost.fabkit-XButton--lg.fabkit-Modal-closeButton")
                            close_btn.click()
                            renew = True
                        except:
                            ...
                            
                    time.sleep(1)

                    upload_images_func(driver, folder_path, not renew)

                    time.sleep(0.1)
                    agreement_inputs[2].click() # Mature content
                    time.sleep(0.1)
                    driver.find_element(By.CSS_SELECTOR, '.fabkit-Checkbox-root.fabkit-Checkbox--md input').click() # Disallow use by Generative AI Programs
                    time.sleep(0.1)

                    file_upload_next(driver, folder_path, "OBJ", ".obj")
                    file_upload_next(driver, folder_path, "FBX", ".fbx")
                    file_upload_next(driver, folder_path, "Additional files", ".zip", True, additional_desc)

                    # Submit for Review or Safe as draft ===========================
                    if(submit_for_review):
                        submit_btn = driver.find_element(By.CSS_SELECTOR, '.fabkit-Button-root.fabkit-Button--md.fabkit-Button--primary')
                        submit_btn.click()
                        time.sleep(0.1)
                        proceed_with_conversion_btn = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, '.fabkit-Modal-container .fabkit-Button-root.fabkit-Button--md.fabkit-Button--secondary')))
                        proceed_with_conversion_btn.click()
                        time.sleep(0.1)
                        final_confirmation_btn = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, '.fabkit-Modal-container .fabkit-Button-root.fabkit-Button--md.fabkit-Button--primary')))
                        final_confirmation_btn.click()
                        time.sleep(0.1)

                    # Increment completed count and update progress
                    completed_folders += 1
                    progress_signal.emit(completed_folders / total_folders)

                    fin_lis.append(folder_path)
                except NoSuchElementException as e:
                    handle_error(driver, "Element not found: " + str(e) + f"\n{folder_path}")
                except Exception as e:
                    handle_error(driver, "Unexpected error: " + str(e) + f"\n{folder_path}")
                finally:
                    time.sleep(2)
                    log_info(folder_path)
                    
    driver.quit()
    log_info("Driver Closed")
    return fin_lis

def select_drafts(headless, drafts_signal):
    driver = initialize_driver(headless)
    selected_drafts = []

    try:
        driver.get(WEBSITE_URL)
        log_info(f"Opened URL: {WEBSITE_URL}")
        time.sleep(2)

        drafts_signal.emit(delete_init(driver))
        
    except NoSuchElementException as e:
        handle_error(driver, "No such element error: " + str(e))
    except Exception as e:
        handle_error(driver, "Unexpected error: " + str(e))
    finally:
        driver.quit()
        log_info("Driver closed.")

def selective_delete(headless, drafts):
    driver = initialize_driver(headless)
    try:
        driver.get(WEBSITE_URL)
        log_info(f"Opened URL: {WEBSITE_URL}")
        time.sleep(2)

        draft_btn = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'draft')))
        draft_btn.click()

        for i in drafts:
            delete_commit(driver, i)
            time.sleep(1)            

    except NoSuchElementException as e:
        print("EOF")
    except Exception as e:
        handle_error(driver, "Unexpected error: " + str(e))
    finally:
        driver.quit()
        log_info("Driver closed.")