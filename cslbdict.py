import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.keys import Keys



def getCompanyName(cslb_num, cslb_dict):
    new_company = False
    company_name = ""
    company_return = cslb_dict.get(cslb_num)
    if(company_return!=None):
        company_name = company_return
        return {
            "company": company_name,
            "new_company": new_company,
            "new_cslbs": None
        }
    else: 
        new_company = True
        driver = webdriver.Chrome()
        wait = WebDriverWait(driver, 20)
        driver.get("https://www.cslb.ca.gov/onlineservices/checklicenseII/checklicense.aspx")
        input = wait.until(EC.visibility_of_element_located((By.ID, "MainContent_LicNo")))
        input.clear()
        input.click()
        input.send_keys(str(cslb_num))
        search = wait.until(EC.visibility_of_element_located((By.ID, "MainContent_Contractor_License_Number_Search")))
        search.click()
        main_text = wait.until(EC.visibility_of_element_located((By.ID, "MainContent_BusInfo"))).text
        new_company_name = main_text.splitlines()[0]
        driver.quit()
        cslb_dict[cslb_num] = new_company_name
        return {
            "company": company_name,
            "new_company": new_company,
            "new_cslbs": cslb_dict
        }

