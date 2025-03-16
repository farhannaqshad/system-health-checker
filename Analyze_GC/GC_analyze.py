from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.expected_conditions import staleness_of
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
import os, sys, time
import datetime as dt

# files_to_analyze = ["testapp1_8080", "testapp1_8180", "testapp2_8080", "testapp2_8180"]

def analyse_file(filename):
    driver = webdriver.Chrome(executable_path=r"chrome\chromedriver.exe")
    driver.maximize_window()
    driver.get('https://gceasy.io')

    try:
        driver.find_element(By.ID, "file").send_keys(os.getcwd()+f"/GC_files/{filename}")
        driver.find_element(By.ID, "submitBtn").click()

        WebDriverWait(driver, 40).until(EC.presence_of_element_located((By.ID, 'getDownloadURL')))

        driver.save_screenshot(f"./GcReports/{filename}_summary.png")

        # gcDurationElement = WebDriverWait(driver, 40).until(EC.presence_of_element_located((By.XPATH, '//*[@id="report"]/div/div[7]/table/tbody/tr/td[1]/table/tbody/tr[2]/td/a')))
        

        # driver.find_element(By.CLASS_NAME, 'result_box')
    
        driver.execute_script("window.scrollTo(0, 1800)")
        driver.find_element(By.XPATH, '//tbody/tr[3]/td[1]/a[1]').click()
        time.sleep(2)
        driver.save_screenshot(f"./GcReports/{filename}_Gc_Duration.png")

        driver.execute_script("window.scrollTo(1800, 2650)")
        driver.save_screenshot(f"./GcReports/{filename}_GC_Details.png")
    except TimeoutException:
        print("Took too much time to load, exiting")
    driver.close()


#Main Work

today = dt.datetime.now().date()
dir = os.getcwd()+"\GC_files\\"  #path to directory
print(dir)
for file in os.listdir(dir):
    print(file)
    filetime = dt.datetime.fromtimestamp(
            os.path.getmtime(dir + file))
    if filetime.date() == today:
        analyse_file(file)

# for filename in files_to_analyze:
#     analyse_file(filename)