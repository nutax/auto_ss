import time
import sys
import os
from PIL import ImageGrab, Image
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
from datetime import datetime

def authenticate_google_drive():
    """Authenticates Google Drive and returns a GoogleDrive instance."""
    gauth = GoogleAuth()
    gauth.LocalWebserverAuth()
    return GoogleDrive(gauth)

def take_screenshot():
    """Captures a screenshot and returns it as a PIL Image."""
    return ImageGrab.grab()

def resize_image(image, scale_factor):
    """Resizes the image by a scale factor."""
    new_width = int(image.width / scale_factor)
    new_height = int(image.height / scale_factor)
    return image.resize((new_width, new_height), Image.ANTIALIAS)

def save_image(image, filename):
    """Saves the image to a file."""
    image.save(filename)

def upload_to_drive(drive, file_path, folder_id):
    """Uploads a file to Google Drive into a specific folder."""
    gfile = drive.CreateFile({'parents': [{'id': folder_id}]})
    gfile.SetContentFile(file_path)
    gfile.Upload()
    print(f"Uploaded {file_path} to Google Drive")
    os.remove(file_path)
    print(f"Deleted local file {file_path}")

def main():
    if len(sys.argv) != 3:
        print("Usage: python script.py <interval_in_seconds> <resize_factor>")
        sys.exit(1)

    # Input parameters
    X = float(sys.argv[1])  # Interval in seconds
    Y = float(sys.argv[2])  # Resize factor
    
    folder_id = '1uREyKOscxUNwoh2054VLtPO0HGRQs-r2'  # Replace with your Google Drive folder ID
    drive = authenticate_google_drive()
    print("Google Drive authenticated. Starting screenshot capture...")

    try:
        while True:
            # Capture timestamp for unique file names
            timestamp = datetime.now().strftime("%Y_%m_%d__%H_%M_%S")
            file_name = f"{timestamp}.png"
            
            # Capture and process the screenshot
            screenshot = take_screenshot()
            resized_screenshot = resize_image(screenshot, Y)
            save_image(resized_screenshot, file_name)
            print(f"Screenshot saved as {file_name}")
            
            # Upload to Google Drive
            upload_to_drive(drive, file_name, folder_id)

            # Wait for the next interval
            time.sleep(X)
    except KeyboardInterrupt:
        print("Program terminated by user.")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
