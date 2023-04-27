from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.keys import Keys
import time
import glob
import os
import pandas as pd
from descriptionParse import getSizeAndType, getLicenseValueParcel
from cslbdict import getCompanyName
from downloadFromAcela import getInitialCsv
from analyze import makePlot

start_time = time.time()

getInitialCsv()


list_of_files = glob.glob('C:/Users/Miles/Downloads/*.csv')
latest_file = max(list_of_files, key=os.path.getctime)
print(latest_file)
df = pd.read_csv(latest_file)
df['Roof or Ground'] ="None"
df['Storage'] = False
df['Value'] = 0.00
df['CSLB'] = 0000000
df['Company'] = 'None'
df['STC Watts'] = 0000.00
df['Price per Watt'] = 0.00
# df['Parcel']
length = len(df.index)

cslbdf = pd.read_csv('./cslbNums.csv')
cslb_dict = dict(zip(cslbdf['CSLB #'], cslbdf['Company List']))


driver = webdriver.Chrome()
wait = WebDriverWait(driver, 20)

for i in range(length):
    try:
        driver.get("https://permits.mynevadacounty.com/CitizenAccess/Cap/CapHome.aspx?module=Building&TabName=Building")
        wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "img[src='/CitizenAccess/nc-horizontal.png']")))
        permit_num = str(df.loc[i, 'Record Number'])
        permit_num_input = wait.until(EC.visibility_of_element_located((By.ID, "ctl00_PlaceHolderMain_generalSearchForm_txtGSPermitNumber")))
        permit_num_input.clear()
        permit_num_input.click()
        permit_num_input.send_keys(permit_num)
        search_button = wait.until(EC.visibility_of_element_located((By.ID, "ctl00_PlaceHolderMain_btnNewSearch")))
        search_button.click()
        more_detail_expand = wait.until(EC.visibility_of_element_located((By.ID, 'imgMoreDetail')))
        more_detail_expand.click()
        money_expand = wait.until(EC.visibility_of_element_located((By.ID, 'imgAddtional')))
        money_expand.click()
        license_expand = wait.until(EC.visibility_of_element_located((By.ID, 'imgASI')))
        license_expand.click()
        parcel_expand = wait.until(EC.visibility_of_element_located((By.ID, 'imgParcel')))
        parcel_expand.click()

        project_description_text = wait.until(EC.visibility_of_element_located((By.ID, 'ctl00_PlaceHolderMain_PermitDetailList1_TBPermitDetailTest'))).text
        project_decription_array = project_description_text.split(" ")
        #returns type (string), size (float kW), storage (boolean)
        size_type_storage = getSizeAndType(project_decription_array)
        stc_size = size_type_storage['size']
        proj_type = size_type_storage['type']
        is_storage = size_type_storage['storage']
        if proj_type != "":
            df.loc[i, 'Roof or Ground'] = proj_type
        if stc_size != 0:
            df.loc[i, 'STC Watts'] = stc_size
        if is_storage == True:
            df.loc[i, "Storage"] = True



        all_more_detail_text = wait.until(EC.visibility_of_element_located((By.ID, 'TRMoreDetail'))).text
        more_detail_array = all_more_detail_text.splitlines()
        #returns value (float), cslb (int), parcel
        license_value_parcel = getLicenseValueParcel(more_detail_array)
        value = license_value_parcel['value']
        cslb = license_value_parcel['cslb']
        parcel = license_value_parcel['parcel']
        if value != 0:
            df.loc[i, 'Value'] = value
        if cslb != '':
            df.loc[i, 'CSLB'] = cslb
    
        company_name_function = getCompanyName(cslb, cslb_dict)
        company_name = company_name_function['company']
        is_new_company = company_name_function['new_company']
        new_cslb_list = company_name_function['new_cslbs']
        if company_name != "":
            df.loc[i, "Company"] = company_name
        if is_new_company == True:
            cslb_dict = new_cslb_list
            #update/overwrite csv
        if value!=0 and stc_size!=0:
            price_per_watt = round(value/(stc_size*1000), 2)
            df.loc[i, "Price per Watt"] = price_per_watt
        
    except:
        print("I CAUGHT AN ERROR")
        print(df.loc[i])




time.sleep(10)



df.to_csv('./result.csv')
time.sleep(10)
makePlot()

print("--- %s seconds ---" % (time.time() - start_time))
