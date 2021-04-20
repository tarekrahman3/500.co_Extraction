# Domain: 500.co
# Website Title: 500 Startups
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import csv

options = Options()
options.add_argument("--no-sandbox")
options.add_experimental_option("useAutomationExtension", False)
options.add_experimental_option("excludeSwitches",["enable-automation"])
options.add_argument("--start-maximized")
options.add_argument('--ignore-certificate-errors')
driver=webdriver.Chrome(options=options, executable_path='/home/tarek/MY_PROJECTS/Selenium_Projects/webdrivers/chromedriver')
dict_array = []
driver.get("https://500.co/startups?filter=1&region=US+-+CA&sector=&platform=")

def infinite_scroll():
	button_xpath = '//*[@id="portfolioPagination"]/button'
	while True:
		try:
			WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, button_xpath)))
			# js pathfinder & scroll
			java_script = '''
			var element = document.getElementById("portfolioPagination");
			element.scrollIntoView(false);
			'''
			driver.execute_script(java_script)
			time.sleep(2)
			driver.execute_script('window.scrollBy(0, 100);')
			a = driver.find_element_by_xpath(button_xpath)
			button = a.text
			print(button)
			if button != 'Load More':
				break
			else:
				pass
			a.click()
		except:
				pass

infinite_scroll()
table = driver.find_elements_by_xpath('//tbody[@id="portfolioContainer"]/tr')
for each_row in table:
	name = each_row.find_element_by_xpath('.//td[@class="portfolio-name"]').text
	try:
		url = each_row.find_element_by_xpath('.//td[@class="portfolio-url"]/a').get_attribute('href')
	except:
		url = ''
	try:
		country = each_row.find_element_by_xpath('.//td[@class="portfolio-country"]').text
	except:
		country = ''
	try:
		sector = each_row.find_element_by_xpath('.//td[@class="portfolio-sector"]').text
	except:
		sector = ''
	try:
		technology = each_row.find_element_by_xpath('.//td[@class="portfolio-platform"]').text
	except:
		technology = ''
	
	data = {
	'name':name,
	'url':url,
	'country': country,
	'sector':sector,
	'technology':technology
	}
	dict_array(data)

fields = list(dict_array[0].keys())
with open('500_startup.csv', 'w') as csvfile: 
	writer = csv.DictWriter(csvfile, fieldnames = fields)
	writer.writeheader()
	writer.writerows(dict_array)
