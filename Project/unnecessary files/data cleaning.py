'''
In the end all this work was for nothing. The files this gathers do not have the
desired information. I did a dumb. There goes 3 hours of my life.
'''

import numpy as np
import pandas as pd

if False:
    data = pd.read_csv('https://financialmodelingprep.com/api/financial-ratios/AAPL?datatype=csv')
    data = pd.read_csv('https://financialmodelingprep.com/api/v3/financials/cash-flow-statement/AAPL?datatype=csv')

#data = pd.read_csv('https://api.intrinio.com/historical_data?identifier=AAPL&item=totalrevenue&start_date=2014-01-01&end_date=2015-01-01')


from selenium import webdriver

if False:
    driver = webdriver.Chrome()
    driver.get('https://simfin.com/data/companies/247341')
    button = driver.find_element_by_id('buttonID')
    button.click()

if True:
    # pip install selenium
    # pip install webdriver-manager
    
    import sys, os
    from selenium.webdriver.common.keys import Keys
    from webdriver_manager.chrome import ChromeDriverManager
    from selenium.webdriver.support import expected_conditions as EC
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait 
    from selenium.webdriver.chrome.options import Options

    if False:
        # Set download preferences to the subdirectory 'files'
        options = webdriver.ChromeOptions()
        prefs = {'download.default_directory' : r'C:\Users\desid\Documents\UDel\MachineLearning\Project\files'}
        
        fileDir = sys.path[0] + '\\files'     
        prefs = {'download.default_directory' : fileDir}
        options.add_experimental_option('prefs', prefs)        
        
        session = webdriver.Chrome(ChromeDriverManager().install(), options = options)
    else:
        session = webdriver.Chrome(ChromeDriverManager().install())
        
    # Login to the SimFin
    session.get('https://simfin.com/login')
    session.find_element_by_xpath('/html/body/div[4]/div/div/div/div/div/div[1]/div[1]/div[3]/form/div[1]/input').send_keys('dmpilla@udel.edu')
    session.find_element_by_xpath('/html/body/div[4]/div/div/div/div/div/div[1]/div[1]/div[3]/form/div[2]/input').send_keys('cisc684project')
    session.find_element_by_xpath('/html/body/div[4]/div/div/div/div/div/div[1]/div[1]/div[3]/form/button').click()
    
    # Go to stock site
    session.get("https://simfin.com/data/companies/247341")
    WebDriverWait(session, 10).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="dynamic-content"]/div[1]/div[2]/div[2]/div/div[1]/div[1]/div[1]')))
    
    # Open download window
    session.find_elements_by_xpath("/html/body/div[4]/div/div/div/div/div/div[1]/div/div[2]/div[1]/div[2]/div/div/div[2]/div/button")[0].click()
    
    # Select file format as csv (NOT WORKING)
    WebDriverWait(session, 10).until(EC.visibility_of_element_located((By.XPATH, "/html/body/div[1]/div/div/div[3]/div/button[1]/span[1]/i")))
    session.find_elements_by_xpath("/html/body/div[1]/div/div/div[3]/div/div[1]/button[2]")[0].click()
    
    # Download the file
    session.implicitly_wait(4)
    session.find_elements_by_xpath("/html/body/div[1]/div/div/div[3]/div/button[1]/span[1]/i")[0].click()
    
    #session.close()