
from selenium import webdriver

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
import os
import time
import datetime as dt


def rename_latest_download_file(path, updatedFileName):
      os.chdir(path)
      files = sorted(os.listdir(os.getcwd()), key=os.path.getmtime)
      newest = files[-1]
      os.rename(path+newest, path+updatedFileName)
      return newest

def analyze_file(filename, rootDir):
    options = webdriver.ChromeOptions()
    prefs = {"profile.default_content_settings.popups": 0,
             "download.default_directory": 
                        rootDir+'\SarReports\\',#IMPORTANT - ENDING SLASH V IMPORTANT
             "directory_upgrade": True}
    options.add_experimental_option("prefs",prefs)
    driver = webdriver.Chrome(executable_path=rootDir+"\chrome\chromedriver.exe", chrome_options=options)
    driver.maximize_window()
    driver.get("https://sarchart.dotsuresh.com/")
    
    try:
        WebDriverWait(driver, 40).until(EC.presence_of_element_located((By.XPATH, '//*[@id="start"]/input')))
        
        print("website is open, now proceeding to upload file for analysis")
        driver.find_element(By.XPATH, '//*[@id="start"]/input').send_keys(rootDir+f"/SA_files/{filename}")
        
        time.sleep(2)
        WebDriverWait(driver, 40).until(EC.presence_of_element_located((By.ID, "btnReport")))
        print("Able to analyze successfully now proceeding to downloading reports for further analysis")
        driver.save_screenshot(f"{rootDir}/{filename}_analyzed.png")
        driver.find_element(By.ID, "btnReport").click()

        WebDriverWait(driver, 40).until(EC.presence_of_element_located((By.ID, "btnSave")))

        driver.find_element(By.ID, 'btnSave').click()
        
        # driver.save_screenshot(f"{filename}_saved.png")    
        
        time.sleep(2)
    except Exception as e:
        print("unable to analyze sar file:: ", e.with_traceback(e))
    
    driver.close()

# analyze_file("testdev")
# newest = rename_latest_download_file(os.getcwd()+'\SarReports\\', "test.pdf")
# print(newest)

# print(os.getcwd())

today = dt.datetime.now().date()
rootDir = os.getcwd()
dir = os.getcwd()+"\SA_files\\"  #path to directory
print(dir)
for file in os.listdir(dir):
    print(file)
    filetime = dt.datetime.fromtimestamp(
            os.path.getmtime(dir + file))
    if filetime.date() == today:
        analyze_file(file, rootDir)
        newest = rename_latest_download_file(rootDir+'\SarReports\\', file +".pdf")
