from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import WebDriverException
#For reading config file
import configparser
import sys

#read data from config file
def read_cred():
	config=configparser.ConfigParser()
	config.read('cred.ini')
	cred=config['cred']
	return cred

#for clicking approve button
def approve(driver):
	ele_approve=driver.find_element_by_xpath("//a[@href='/account/approve']")
	ele_approve.click()

#Providing authorization if not already authenticated
def auth(driver):
	credentials=read_cred()
	elem_un=driver.find_element_by_xpath("//input[@id='username']")
	elem_un.send_keys(credentials['username'])
	elem_un.send_keys(Keys.RETURN)
	elem_pass=driver.find_element_by_xpath("//input[@id='password']")
	elem_pass.send_keys(credentials['password'],Keys.RETURN)

#Selects duration of approval
def approval_duration(driver,duration):
	xpath="//input[@value='"+str(duration)+"']"
	driver.find_element_by_xpath(xpath).click()
	driver.find_element_by_id("approveBtn").click()
			
	
#Checks for duration and uses 60 min by default
if len(sys.argv) < 2:
	duration=1
else:
	duration=sys.argv[1]


#Approval page url
url='https://netaccess.iitm.ac.in/account/approve'

try:
	driver=webdriver.Chrome()
	driver.get(url)
	#Check if already authenticated
	if "approve" not in driver.title:
		auth(driver)
	approve(driver)
	approval_duration(driver,duration)
	
except WebDriverException, e:
	print "Please install drivers"
