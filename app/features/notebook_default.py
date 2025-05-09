import json
import os
from helpers.notebook_helper import NotebookHelper
import urllib.parse


class NotebookDefault:
    def __init__(self, driver):
        self.helper = NotebookHelper(driver=driver)

    def generate_audio_podcast_from_profiles(self, data):
        CONFIG_PATH = os.path.join(os.path.dirname(__file__), "..", "config", "config.json")
        with open(CONFIG_PATH, "r") as config_file:
            CONFIG = json.load(config_file)
        # Open the notebook
        self.helper.open_notebook()
        self.helper.login(CONFIG["notebook_email"], CONFIG["notebook_password"])

        # self.helper.test_notebook()
        # self.helper.download_file()
        # Click to create a new notebook
        
        if self.helper.click_create_new_notebook():
            print("Successfully clicked to create a new notebook.")
            if self.helper.upload_files(data):
                print("Successfully clicked the input button.")
                if self.helper.generate_audio_podcast():
                        print("Successfully generated the audio podcast.")
                        if self.helper.download_file():
                            print("Successfully downloaded the audio podcast.")
                        else:
                            print("Failed to download the audio podcast.")
                else:
                    print("Failed to generate the audio podcast.")
            else:
                print("Failed to click the input button.")
        else:
            print("Failed to click to create a new notebook.")


    def generate_one_youtube_video_podcast(self, args):
        CONFIG_PATH = os.path.join(os.path.dirname(__file__), "..", "config", "config.json")
        with open(CONFIG_PATH, "r") as config_file:
            CONFIG = json.load(config_file)
        # Open the notebook
        self.helper.open_notebook()
        self.helper.login(CONFIG["notebook_email"], CONFIG["notebook_password"])

        # Click to create a new notebook
        if self.helper.click_create_new_notebook():
            print("Successfully clicked to create a new notebook.")
            if self.helper.click_youtube_button():
                print("Successfully clicked the YouTube button.")
                if self.helper.upload_youtube_source(urllib.parse.unquote(args)):
                    print("Successfully uploaded the YouTube source.")
                    if self.helper.generate_audio_podcast():
                        print("Successfully generated the audio podcast.")
                    else:
                        print("Failed to generate the audio podcast.")
                else:
                    print("Failed to upload the YouTube source.")
            else:
                print("Failed to click the YouTube button.")
        else:
            print("Failed to click to create a new notebook.")

        self.helper.wait(10000)

        return self.default