from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.keys import Keys
import time

def getInitialCsv():
    driver = webdriver.Chrome()
    # driver.maximize_window()
    driver.get("https://permits.mynevadacounty.com/CitizenAccess/Cap/CapHome.aspx?module=Building&TabName=Building")
    wait = WebDriverWait(driver, 20)
    wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "img[src='/CitizenAccess/nc-horizontal.png']")))
    wait.until(EC.element_to_be_clickable((By.ID, "ctl00_PlaceHolderMain_lblGSLoadASI"))).click()
    wait.until(EC.visibility_of_element_located((By.ID, "ctl00_PlaceHolderMain_divGSASITResult")))
    start_date = wait.until(EC.visibility_of_element_located((By.ID, "ctl00_PlaceHolderMain_generalSearchForm_txtGSStartDate")))
    start_date.click()
    start_date.send_keys("01/01/2023")
    end_date = wait.until(EC.visibility_of_element_located((By.ID, "ctl00_PlaceHolderMain_generalSearchForm_txtGSEndDate")))
    end_date.click()
    end_date.send_keys("01/31/2023")

    res_commer_select = wait.until(EC.visibility_of_element_located((By.ID, "ctl00_PlaceHolderMain_asiGSForm_NEVCO_ddl_0_0")))
    res_commer_select.click()
    res_commer_select.send_keys(Keys.ARROW_DOWN)
    res_commer_select.send_keys(Keys.ARROW_DOWN)
    res_commer_select.send_keys(Keys.ENTER)

    type_permit_select = wait.until(EC.visibility_of_element_located((By.ID, "ctl00_PlaceHolderMain_asiGSForm_NEVCO_ddl_0_1")))
    type_permit_select.click()
    type_permit_select.send_keys(Keys.ARROW_DOWN)
    type_permit_select.send_keys(Keys.ARROW_DOWN)
    type_permit_select.send_keys(Keys.ARROW_DOWN)
    type_permit_select.send_keys(Keys.ARROW_DOWN)
    type_permit_select.send_keys(Keys.ARROW_DOWN)
    type_permit_select.send_keys(Keys.ARROW_DOWN)
    type_permit_select.send_keys(Keys.ARROW_DOWN)
    type_permit_select.send_keys(Keys.ARROW_DOWN)
    type_permit_select.send_keys(Keys.ARROW_DOWN)
    type_permit_select.send_keys(Keys.ENTER)

    search_button = wait.until(EC.visibility_of_element_located((By.ID, "ctl00_PlaceHolderMain_btnNewSearch")))
    search_button.click()


    download_csv = wait.until(EC.visibility_of_element_located((By.ID, "ctl00_PlaceHolderMain_dgvPermitList_gdvPermitList_gdvPermitListtop4btnExport")))
    download_csv.click()


    time.sleep(10)
    driver.quit()