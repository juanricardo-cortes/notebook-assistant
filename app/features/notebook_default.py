from helpers.notebook_helper import NotebookHelper
import urllib.parse

class NotebookDefault:
    def __init__(self):
        self.helper = NotebookHelper()

    def start(self, args):
        # Open the notebook
        self.helper.open_notebook()
        self.helper.login("juanricardo.m.cortes@bhtechnology.org", "iL0VEMIKEE")

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