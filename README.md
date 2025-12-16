MEDIAFIRE AUTO DOWNLOADER
========================

A reliable Python tool to automatically download files and folders from public MediaFire links, with resume support and folder mirroring.


--------------------------------------------------
OVERVIEW
--------------------------------------------------

MediaFire Auto Downloader is designed to handle MediaFire’s dynamic web interface safely and consistently.

Instead of relying on fragile browser clicks for downloads, the script:
- Uses Selenium only to browse folders and discover files
- Extracts the real direct download URLs
- Downloads files using HTTP requests (requests library)

This approach avoids common issues such as:
- Elements not clickable
- Stale element references
- Browser crashes during downloads
- Partial or corrupted files


--------------------------------------------------
FEATURES
--------------------------------------------------

- Supports public MediaFire folder URLs
- Works with root folders and direct subfolder links
- Automatically detects folders and files on the current page
- Recursively processes all folders
- Downloads files found on any page
- Creates per-folder local directories
- Resume support for interrupted downloads
- Verifies downloads using file size
- Skips files that already exist and are complete
- Retries failed downloads
- Clean timestamped logging
- Stable and repeatable behavior


--------------------------------------------------
REQUIREMENTS
--------------------------------------------------

System:
- Windows, Linux, or macOS
- Google Chrome browser
- ChromeDriver (matching Chrome version)

Python:
- Python 3.9 or newer

Python packages:
- selenium
- requests
- beautifulsoup4

Install dependencies:

    pip install selenium requests beautifulsoup4


--------------------------------------------------
INSTALLATION
--------------------------------------------------

1. Clone the repository

    git clone https://github.com/your-username/mediafire-auto-downloader.git
    cd mediafire-auto-downloader

2. Install dependencies

    pip install -r requirements.txt

3. Verify Chrome and ChromeDriver compatibility


--------------------------------------------------
USAGE
--------------------------------------------------

Run the script by passing a MediaFire URL as an argument.

    python mediafireAuto.py <mediafire_url>

Examples:

    python mediafireAuto.py https://www.mediafire.com/?xiewm7hyckakp
    python mediafireAuto.py https://www.mediafire.com/?xiewm7hyckakp#mm06h4pyd1osk

The script automatically detects:
- Pages containing folders
- Pages containing files
- Pages containing both folders and files


--------------------------------------------------
DOWNLOAD STRUCTURE
--------------------------------------------------

Downloaded files are stored under the downloads directory.
Each MediaFire folder is mirrored locally.

Example:

    downloads/
      xiewm7hyckakp/
        Annamacharya Krithis by Unnikrishnan - V/
          Chaladha Hari.mp3
          Another Song.mp3


--------------------------------------------------
RESUME & VERIFICATION
--------------------------------------------------

- If a download is interrupted, rerunning the script resumes it
- Existing files are checked by size
- Completed files are skipped automatically
- Corrupted or incomplete files are re-downloaded


--------------------------------------------------
LOGGING
--------------------------------------------------

The script prints timestamped logs to the console, including:
- Folder discovery
- File detection
- Download start and completion
- Retry attempts
- Errors (if any)


--------------------------------------------------
LIMITATIONS
--------------------------------------------------

- Works only with public MediaFire links
- Does not bypass:
  - Password protection
  - Private folders
  - Copyright restrictions
- Download speed depends on MediaFire servers


--------------------------------------------------
LICENSE
--------------------------------------------------

This project is provided for educational and personal use only.
Users are responsible for complying with MediaFire’s terms of service.


--------------------------------------------------
DISCLAIMER
--------------------------------------------------

This tool is not affiliated with or endorsed by MediaFire.
Use responsibly and only download content you are authorized to access.
