import os
import sys
import time
import requests
from bs4 import BeautifulSoup
from datetime import datetime
from urllib.parse import urlparse

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

WAIT_TIME = 20
MAX_RETRIES = 3
LOG_TIME_FORMAT = "%Y-%m-%d %H:%M:%S"

def log(message):
    ts = datetime.now().strftime(LOG_TIME_FORMAT)
    print(f"[{ts}] {message}")

if len(sys.argv) < 2:
    print("Usage: python mediafireAuto.py <mediafire_url>")
    sys.exit(1)

START_URL = sys.argv[1].strip()

if "mediafire.com" not in START_URL:
    print("Invalid MediaFire URL")
    sys.exit(1)

parsed = urlparse(START_URL)
root_name = parsed.fragment or parsed.path.replace("/", "") or "mediafire_download"
ROOT_DOWNLOAD_DIR = os.path.abspath(os.path.join("downloads", root_name))
os.makedirs(ROOT_DOWNLOAD_DIR, exist_ok=True)

options = Options()
options.add_argument("--disable-gpu")
options.add_argument("--disable-notifications")
options.add_argument("--start-maximized")

driver = webdriver.Chrome(options=options)
wait = WebDriverWait(driver, WAIT_TIME)

def wait_for_list():
    wait.until(EC.presence_of_element_located((By.ID, "main_list")))
    time.sleep(1.5)

def get_folders():
    return driver.find_elements(By.CSS_SELECTOR, "li.mf_filecontainer.folder")

def get_files():
    return driver.find_elements(By.CSS_SELECTOR, "li.mf_filecontainer.file")

def get_download_url(file_page_url):
    r = requests.get(file_page_url, timeout=30)
    r.raise_for_status()
    soup = BeautifulSoup(r.text, "html.parser")
    btn = soup.find("a", id="downloadButton")
    if not btn or not btn.get("href"):
        raise Exception("Download button not found")
    return btn["href"]

def download_with_resume(url, filepath):
    temp = filepath + ".part"
    headers = {}
    downloaded = 0

    if os.path.exists(temp):
        downloaded = os.path.getsize(temp)
        headers["Range"] = f"bytes={downloaded}-"

    with requests.get(url, stream=True, headers=headers, timeout=30) as r:
        r.raise_for_status()
        mode = "ab" if downloaded else "wb"
        with open(temp, mode) as f:
            for chunk in r.iter_content(8192):
                if chunk:
                    f.write(chunk)

    os.rename(temp, filepath)

def process_current_page(target_dir):
    files = get_files()
    log("Files found on page: " + str(len(files)))

    tasks = []
    for f in files:
        try:
            name = f.find_element(By.CSS_SELECTOR, "span.item-name").text.strip()
            link = f.find_element(By.CSS_SELECTOR, "a.thumbnailClickArea").get_attribute("href")
            tasks.append((name, link))
        except:
            pass

    for name, link in tasks:
        path = os.path.join(target_dir, name)
        if os.path.exists(path):
            log("File already exists, skipping: " + name)
            continue

        log("Preparing download: " + name)
        for attempt in range(1, MAX_RETRIES + 1):
            try:
                log("Attempt " + str(attempt) + " for " + name)
                url = get_download_url(link)
                download_with_resume(url, path)
                log("Download completed: " + name)
                break
            except Exception as e:
                log("Attempt failed: " + str(e))
                time.sleep(2)

log("Script started")
log("Target URL: " + START_URL)

driver.get(START_URL)
wait_for_list()

folders = get_folders()
files = get_files()

log("Initial folders detected: " + str(len(folders)))
log("Initial files detected: " + str(len(files)))

# Case 1: files exist at start URL
if files:
    log("Processing files at start URL")
    process_current_page(ROOT_DOWNLOAD_DIR)

# Case 2: folders exist
if folders:
    folder_snapshot = []
    for f in folders:
        try:
            name = f.find_element(By.CSS_SELECTOR, "span.item-name").text.strip()
            key = f.get_attribute("data-key")
            folder_snapshot.append((name, key))
        except:
            pass

    log("Total folders collected: " + str(len(folder_snapshot)))

    base = START_URL.split("#")[0]

    for index, (folder_name, folder_key) in enumerate(folder_snapshot, start=1):
        log("Processing folder " + str(index) + " of " + str(len(folder_snapshot)))
        log("Folder name: " + folder_name)

        folder_dir = os.path.join(ROOT_DOWNLOAD_DIR, folder_name)
        os.makedirs(folder_dir, exist_ok=True)

        driver.get(base + "#" + folder_key)
        wait_for_list()

        process_current_page(folder_dir)

log("All processing completed")
driver.quit()
log("Script finished")
