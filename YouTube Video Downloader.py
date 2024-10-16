import os
import yt_dlp

def download_video(url, path):
    try:
        # yt-dlp configuration
        ydl_opts = {
            'format': 'best',  # Download the best available quality
            'outtmpl': os.path.join(path, '%(title)s.%(ext)s'),  # Save the file with the title as the name
        }

        # Start the download
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            print("Downloading...")
            ydl.download([url])

        print("Download completed!")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    # Get user inputs
    url = input("Enter the YouTube video URL: ")
    path = input("Enter the directory path to save the video: ").strip('\"')  # Removes double quotes

    # Check if the directory exists
    if not os.path.exists(path):
        print(f"The directory {path} does not exist.")
    else:
        # Download the video to the specified directory
        download_video(url, path)