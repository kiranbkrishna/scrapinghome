from tesseract import get_num_from_screenshot

from selenium import webdriver
from selenium.webdriver.common.keys import Keys

driver = webdriver.Chrome()
driver.get("https://www.justdial.com/Bangalore/Car-Washing-Services/nct-10079017")
# import pdb; pdb.set_trace()
parse_page(driver)


def parse_page(driver):
	links = driver.find_elements_by_class_name('tabsM').find_elements_by_tag_name('a')

#result = get_num_from_screenshot("") 
