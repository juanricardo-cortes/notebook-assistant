# Notebook Assistant

## Prerequisites

1. **Powershell**
2. **Python**

## Setup Instructions

1. Create a folder with the following path:
   ```
   C:\pinokio
   ```

2. Navigate to the folder path:
   ```
   cd C:\pinokio
   ```

3. Run the following commands in Powershell (ensure you are in `C:\pinokio`):

   ```powershell
   Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy Unrestricted
   .\api\notebook-assistant\app\env\Scripts\activate
   which python
   ```

   - The `which python` command should confirm that `notebook-assistant` is the active environment.

4. Install the required Python packages:
   ```powershell
   pip install transformers accelerate diffusers gradio devicetorch openai beautifulsoup4 selenium requests webdriver-manager torch youtube-transcript-api google-api-python-client playwright facebook-sdk linkedin-scraper google-cloud-storage pyautogui
   ```