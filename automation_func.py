import os
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

# =================================================== Create Option =================================================== #

def info_init(driver, product_type):
        time.sleep(3)
        create_listings = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, '.fabkit-Hidden-down--mobile')))
        create_listings[1].click()

        if(product_type == "3D Model"):
            asset_3d = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, '3d-model')))
            asset_3d.click()

            confirm_selection = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, '.fabkit-Button-root.fabkit-Button--md.fabkit-Button--primary')))
            if confirm_selection.get_attribute('aria-label') == "Confirm selected option: 3d-model":
                confirm_selection.click()
        elif(product_type == "Textures"):
            texture = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'material')))
            texture.click()

            confirm_selection = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, '.fabkit-Button-root.fabkit-Button--md.fabkit-Button--primary')))
            if confirm_selection.get_attribute('aria-label') == "Confirm selected option: material":
                confirm_selection.click()

def price_select(driver, price):
    price_dropdown = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'fabkit-Dropdown-container')))
    price_list = WebDriverWait(price_dropdown, 20).until(EC.presence_of_all_elements_located((By.TAG_NAME, 'li')))
    for i in price_list:
        if(i.get_attribute('innerHTML') == price):
            i.click()
            break

def upload_images_func(driver, folder_path):
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
        WebDriverWait(driver, 60).until(
            EC.invisibility_of_element_located((By.CSS_SELECTOR, ".fabkit-Modal-container"))
        )
    except Exception as e:
        print("Timed out waiting for modal to disappear.")

def file_upload(driver, folder_path, file_name, file_type, add_bool=False, add_desc=None):
    upload_model_btn = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, ".fabkit-Surface-root.fabkit-Surface--outlined.fabkit-Surface--emphasis-background-elevated-high-default.fabkit-scale--radius-2.fabkit-scale--gutterX-spacing-5.fabkit-scale--gutterY-spacing-6.kUuzwc_J button.fabkit-Button-root.fabkit-Button--md.fabkit-Button--primary.fabkit-Button--fullWidth")))
    upload_model_btn.click()
    general_upload(driver, folder_path, file_name, file_type, add_bool, add_desc)

def file_upload_next(driver, folder_path, file_name, file_type, add_bool=False, add_desc=None):
    upload_next_model_btn = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, '.fabkit-Button-root.fabkit-Button--md.fabkit-Button--primary.fabkit-Button--fullWidth')))
    upload_next_model_btn.click()
    general_upload(driver, folder_path, file_name, file_type, add_bool, add_desc)    

def general_upload(driver, folder_path, file_name, file_type, add_bool, add_desc):
    time.sleep(0.1)
    upload_buttons =  WebDriverWait(driver, 20).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, '.fabkit-Stack-root.fabkit-Stack--align_center.fabkit-scale--gapX-spacing-4.fabkit-scale--gapY-spacing-4.fabkit-Surface-root.fabkit-Surface--emphasis-background-elevated-high-default.fabkit-scale--radius-2.fabkit-Surface--interactive.fabkit-scale--gutterX-spacing-3.fabkit-scale--gutterY-spacing-3.option.j6NLBb2a')))
    for i in range(len(upload_buttons)):
        type_of_model = driver.find_elements(By.CSS_SELECTOR, '.fabkit-Stack-root.fabkit-Stack--align_center.fabkit-scale--gapX-spacing-4.fabkit-scale--gapY-spacing-4.fabkit-Surface-root.fabkit-Surface--emphasis-background-elevated-high-default.fabkit-scale--radius-2.fabkit-Surface--interactive.fabkit-scale--gutterX-spacing-3.fabkit-scale--gutterY-spacing-3.option.j6NLBb2a .fabkit-Typography-root.fabkit-Typography--align-start.fabkit-Typography--intent-primary.fabkit-Text--md.fabkit-Text--regular.fabkit-Stack-grow')[i].get_attribute('innerHTML')
        if(type_of_model == file_name):
            uke_btn = driver.find_elements(By.CSS_SELECTOR, '.fabkit-Stack-root.fabkit-Stack--align_center.fabkit-scale--gapX-spacing-4.fabkit-scale--gapY-spacing-4.fabkit-Surface-root.fabkit-Surface--emphasis-background-elevated-high-default.fabkit-scale--radius-2.fabkit-Surface--interactive.fabkit-scale--gutterX-spacing-3.fabkit-scale--gutterY-spacing-3.option.j6NLBb2a')[i]
            uke_btn.click()
            uk_btn = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, '.fabkit-Modal-container button.fabkit-Button-root.fabkit-Button--md.fabkit-Button--primary')))
            uk_btn.click()
            model_input = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, '.fabkit-Modal-container input.fabkit-ScreenReaderOnly-root')))
            driver.execute_script("arguments[0].style.display = 'block';", model_input)
            model_input.send_keys(next((os.path.join(folder_path, filename) for filename in os.listdir(folder_path) if filename.endswith(file_type)), None))
            driver.find_element(By.CSS_SELECTOR, '.fabkit-Modal-container button.fabkit-Button-root.fabkit-Button--md.fabkit-Button--primary').click()
            break

    try:
        WebDriverWait(driver, 30).until(
            EC.invisibility_of_element_located((By.CSS_SELECTOR, ".fabkit-Modal-container"))
        )
    except Exception as e:
        print("Timed out waiting for modal to disappear.")
    
    time.sleep(1)
    
    if(add_bool):
            add_desc_elem = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, '.tiptap.ProseMirror.fabkit-RichEditor-content.fabkit-RichEditor-prose')))
            driver.execute_script(f"arguments[0].innerHTML = '<p>{add_desc}</p>';", add_desc_elem)

    time.sleep(1)

# =================================================== Edit Option =================================================== #

def edit_init(driver, file_name):
    time.sleep(1)
    select_edit_element(driver, file_name)
    time.sleep(2)
    
    # time.sleep(3)
    # listings = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, '.fabkit-Stack-root.fabkit-scale--gapX-layout-6.fabkit-scale--gapY-layout-6.fabkit-Stack--column ul li')))
    # for i in listings:
    #     ...

    # asset_3d = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, '3d-model')))
    # asset_3d.click()

    # confirm_selection = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, '.fabkit-Button-root.fabkit-Button--md.fabkit-Button--primary')))
    # if confirm_selection.get_attribute('aria-label') == "Confirm selected option: 3d-model":
    #     confirm_selection.click()

# Scroll and collect all dynamically loaded elements
def select_edit_element(driver, file_name, scroll_pause_time=0.1):
    SCROLLABLE_CONTAINER_SELECTOR = '.fabkit-Stack-root.fabkit-scale--gapX-layout-6.fabkit-scale--gapY-layout-6.fabkit-Stack--column'
    ELEMENTS_SELECTOR = 'ul li'

    # Locate the scrollable container
    container = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, SCROLLABLE_CONTAINER_SELECTOR))
    )

    # Initialize variables
    scroll_height = 1500
    count = 0

    while count < 19:
        time.sleep(scroll_pause_time)

        # Get current elements
        current_elements = container.find_elements(By.CSS_SELECTOR, ELEMENTS_SELECTOR)

        # Add new elements to the set
        for elem in current_elements:
            if (elem.find_element(By.CSS_SELECTOR, '.fabkit-Typography-ellipsisWrapper').get_attribute('innerHTML') == file_name):
                elem.click()
                count = 20
                break
        
        if (count == 20):
            break

        # Scroll down
        driver.execute_script("document.documentElement.scrollTo(0, arguments[0]);", scroll_height)

        # Check if scrolling reaches the bottom
        scroll_height += 1500
        count += 1