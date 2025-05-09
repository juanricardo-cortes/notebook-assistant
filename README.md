# Notebook Assistant

## Prerequisites

1. **Powershell**
2. **Python** ([Download Python](https://www.python.org/))
3. **Pinokio** ([Install Pinokio](https://program.pinokio.computer/#/?id=install))

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
   # Step 1: Set the execution policy to unrestricted for the current user.
   Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy Unrestricted

   # Step 2: Clone the repository from GitHub to your local machine.
   git clone https://github.com/juanricardo-cortes/notebook-assistant.git

   # Step 3: Activate the virtual environment for the Notebook Assistant application.
   .\api\notebook-assistant\app\env\Scripts\activate

   # Step 4: Verify that the Notebook Assistant environment is active.
   which python
   ```

   - The `which python` command should confirm that `notebook-assistant` is the active environment.

4. Install the required Python packages:
   ```powershell
   pip install transformers accelerate diffusers gradio devicetorch openai beautifulsoup4 selenium requests webdriver-manager torch youtube-transcript-api google-api-python-client playwright facebook-sdk linkedin-scraper google-cloud-storage pyautogui
   ```

5. Modify `notebook-assistant/app/config/config.json`, change `notebook_email` and `notebook_password`.
   - Optional: This is where you can modify the list of profiles to scrape.

6. Send an email to `juanricardo.m.cortes@bhtechnology.org` to get `youtube_api_key`, `openai_api_key`, and `service-account.json` file.