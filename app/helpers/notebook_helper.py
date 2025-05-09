import os
import time
import pyautogui # type: ignore
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.action_chains import ActionChains
from webdriver_manager.chrome import ChromeDriverManager # type: ignore

class NotebookHelper:
    def __init__(self, driver, headless=False):
        # Setup Chrome options
        # options = webdriver.ChromeOptions()
        # if headless:
        #     options.add_argument("--headless")
        # options.add_argument("--mute-audio")
        # options.add_argument("--no-sandbox")
        # options.add_argument("--disable-dev-shm-usage")
        # options.add_argument("--start-maximized")

        # self.driver = webdriver.Chrome(
        #     service=Service(ChromeDriverManager().install()),
        #     options=options
        # )

        self.driver = driver
        self.your_notebook_url = "https://notebooklm.google.com/"

    def open_notebook(self):
        self.driver.get(self.your_notebook_url)
        print(f"Opening Notebook URL: {self.your_notebook_url}")
        time.sleep(5)  # Let the page load

    def login(self, email, password):
        try:
            # Locate the email/username field and enter the email
            email_field = self.driver.find_element(By.ID, "identifierId")  # Replace with the actual ID or selector
            email_field.send_keys(email)
            self.driver.find_element(By.ID, "identifierNext").click()  # Replace with the actual ID or selector
            time.sleep(2)  # Wait for the password field to load

            # Locate the password field and enter the password
            password_field = self.driver.find_element(By.NAME, "Passwd")  # Replace with the actual name or selector
            password_field.send_keys(password)
            self.driver.find_element(By.ID, "passwordNext").click()  # Replace with the actual ID or selector
            time.sleep(5)  # Wait for the login process to complete

            # Click "Do this later" if the prompt appears
            try:
                do_this_later_button = self.driver.find_element(By.LINK_TEXT, "Do this later")  # Replace with the actual text or selector
                do_this_later_button.click()
                print("Clicked 'Do this later'.")
            except Exception as e:
                print("'Do this later' button not found or not needed:", e)

            print("Login successful!")
        except Exception as e:
            print(f"Login failed: {e}")

    def click_create_new_notebook(self):
        time.sleep(5)
        try:
            menu_button = self.driver.find_element(By.CLASS_NAME, "create-new-button")
            menu_button.click()
            print("Clicked on the 'Create New Notebook' button.")
            return True
        except Exception as e:
        # If both buttons are not found, print the error and return False
            print(f"Could not find button: {e}")
            return False
        
    def upload_files(self, data_array):
        print(f"Uploading files: {data_array}")
        time.sleep(3)
        try:
            input_file_button = self.driver.find_element(By.CSS_SELECTOR, "button[aria-label='Upload sources from your computer']")
            if input_file_button is not None:
                print("Found the input file button.")
                input_file_button.click()
                time.sleep(2)
                file_path = os.path.abspath(data_array[0])  # Get the absolute path of the file
                pyautogui.write(file_path)
                pyautogui.press('enter')
                time.sleep(20) # Wait for upload

                add_file_button = self.driver.find_element(By.CSS_SELECTOR, "button[aria-label='Add source']")
                for data in data_array[1:]:
                    if add_file_button is not None:
                        print("Found the add file button.")
                        add_file_button.click()
                        time.sleep(2)
                        input_file_button = self.driver.find_element(By.CSS_SELECTOR, "button[aria-label='Upload sources from your computer']")
                        input_file_button.click()
                        time.sleep(2)
                        file_path = os.path.abspath(data)
                        pyautogui.write(file_path)
                        pyautogui.press('enter')
                        time.sleep(20)
                    else:
                        print("Add file button not found.")
                        return False
                return True
            else:
                print("Input file button not found.")
                return False
        except Exception as e:
            print(f"Could not find input file button: {e}")
            return False
        
    def click_pasted_text_button(self):
        time.sleep(3)
        try:
            level_one = self.driver.find_elements(By.CLASS_NAME, "mdc-evolution-chip--with-primary-icon")
            for element in level_one:
                level_two = element.find_element(By.CLASS_NAME, "mdc-evolution-chip__cell")
                level_three = level_two.find_element(By.CLASS_NAME, "mdc-evolution-chip__action")
                level_four = level_three.find_element(By.CLASS_NAME, "mat-mdc-chip-action-label")
                level_five = level_four.find_element(By.TAG_NAME, "span")
                print(f"Found button: {level_five.text}")
                if level_five is not None:
                    if level_five.text == "Copied text":
                        print("Found the Text button.")
                        break

            level_three.click()
            print("Clicked on the 'YouTube' button.")
            return True
        except Exception as e:
            print(f"Could not find YouTube button: {e}")
            return False
        
    def click_youtube_button(self):
        time.sleep(3)
        try:
            level_one = self.driver.find_elements(By.CLASS_NAME, "mdc-evolution-chip--with-primary-icon")
            for element in level_one:
                level_two = element.find_element(By.CLASS_NAME, "mdc-evolution-chip__cell")
                level_three = level_two.find_element(By.CLASS_NAME, "mdc-evolution-chip__action")
                level_four = level_three.find_element(By.CLASS_NAME, "mat-mdc-chip-action-label")
                level_five = level_four.find_element(By.TAG_NAME, "span")
                print(f"Found button: {level_five.text}")
                if level_five is not None:
                    if level_five.text == "YouTube":
                        print("Found the YouTube button.")
                        break

            level_three.click()
            print("Clicked on the 'YouTube' button.")
            return True
        except Exception as e:
            print(f"Could not find YouTube button: {e}")
            return False

    def upload_youtube_source(self, link):
        time.sleep(3)
        try:
            # Locate the YouTube link input field and enter the link
            youtube_link_field = self.driver.find_element(By.CLASS_NAME, "mat-mdc-input-element")  # Replace with the actual class or selector
            youtube_link_field.send_keys(link)
            print(f"Entered YouTube link: {link}")

            time.sleep(2)  # Wait for the link to be processed
            submit_buttons = self.driver.find_elements(By.CLASS_NAME, "mat-mdc-unelevated-button")
            print(f"Found {len(submit_buttons)} submit buttons.")
            for submit_button in submit_buttons:
                validate_button = submit_button.find_element(By.CLASS_NAME, "mdc-button__label")
                if validate_button is not None:
                    if validate_button.text == "Insert":
                        submit_button.click()
            return True
        except Exception as e:
            print(f"Could not enter YouTube link: {e}")
            return False
        
    def generate_audio_podcast(self):
        time.sleep(3)
        try:
            # Locate the "Generate Audio Podcast" button and click it
            while True:
                try:
                    generate_button = self.driver.find_element(By.CLASS_NAME, "generate-button")  # Replace with the actual class or selector
                    if generate_button.is_enabled():
                        generate_button.click()
                        print("Clicked on the 'Generate Audio Podcast' button.")
                        break
                except Exception as e:
                    print(f"Could not find 'Generate Audio Podcast' button: {e}")
                    time.sleep(1)
            return True
        except Exception as e:
            print(f"Could not find 'Generate Audio Podcast' button: {e}")
            return False

    def download_file(self):
        time.sleep(30)
        try:
            # Locate the download button and click it
            while True: 
                try:
                    expand_button = self.driver.find_element(By.CSS_SELECTOR, "button[aria-label='See more options for audio player']")  # Replace with the actual class or selector
                    if expand_button is not None:
                        break
                    else: 
                        continue
                except Exception as e:
                    continue
            time.sleep(2)
            expand_button.click()
            time.sleep(3)
            download_button = self.driver.find_element(By.CSS_SELECTOR, "a.mat-mdc-menu-item") 
            time.sleep(5)
            download_button.click()
            print("Clicked on the 'Download' button.")
            return True
        except Exception as e:
            print(f"Could not find 'Download' button: {e}")
            return False
    
    def test_notebook(self):
        self.driver.get("https://notebooklm.google.com/notebook/674d14b6-e291-42f9-8bb4-ccdefd762cea")
        print(f"Opening Notebook URL: {self.your_notebook_url}")
        time.sleep(15)  # Let the page load
        expand_button = self.driver.find_element(By.CSS_SELECTOR, "button[aria-label='Load the audio overview']")
        expand_button.click()
        time.sleep(5)
    
    def wait(self, seconds):
        time.sleep(seconds)
