from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.keys import Keys
import time
import glob
import os
import pandas as pd


list_of_files = glob.glob('C:/Users/Miles/Downloads/*.csv')
latest_file = max(list_of_files, key=os.path.getctime)

df = pd.read_csv('C:/Users/Miles/Downloads/RecordList20230424 (3).csv')

print(df.dtypes)

df['Storage'] = 0
df['Value'] = 0.00
df['CSLB'] = 0000000
df['Company'] = 'None'
df['STC Watts'] = 0000
df['Price per Watt'] = 0.00


length = len(df.index)

driver = webdriver.Chrome()
# driver.maximize_window()
driver.get("https://permits.mynevadacounty.com/CitizenAccess/Cap/CapHome.aspx?module=Building&TabName=Building")
wait = WebDriverWait(driver, 20)
wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "img[src='/CitizenAccess/nc-horizontal.png']")))



# for i in range(length):
#     permit_num = df.loc[i, 'Record Number']
#     permit_num_input = wait.until(EC.visibility_of_element_located((By.ID, "ctl00_PlaceHolderMain_generalSearchForm_txtGSPermitNumber")))
#     permit_num_input.click()
#     permit_num_input.send_keys(permit_num)
#     search_button = wait.until(EC.visibility_of_element_located((By.ID, "ctl00_PlaceHolderMain_btnNewSearch")))
#     search_button.click()


permit_num = str(df.loc[0, 'Record Number'])
permit_num_input = wait.until(EC.visibility_of_element_located((By.ID, "ctl00_PlaceHolderMain_generalSearchForm_txtGSPermitNumber")))
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


all_more_detail_text = wait.until(EC.visibility_of_element_located((By.ID, 'TRMoreDetail'))).text
more_detail_array = all_more_detail_text.splitlines()
value_string = ''
cslb = ''
parcel_num = ''

for index, item in enumerate(more_detail_array):
    if "Estimated Valuation" in item:
        value_string = more_detail_array[index+1]
    if "License Number:" in item:
        cslb = more_detail_array[index+1]
    if "Parcel Number:" in item:
        parcel_num = more_detail_array[index+1]



print("value string: " + value_string)
print("cslb: " + cslb)
print("parcel number: " + parcel_num)

if value_string != '':
    df.loc[0, 'Value'] = float(value_string.replace(',',''))
if cslb != '':
    df.loc[0, 'CSLB'] = cslb



time.sleep(10)



df.to_csv('C:/Users/Miles/Downloads/newCSV.csv')


