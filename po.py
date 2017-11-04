from selenium import webdriver

driver = webdriver.Chrome()
driver.get("https://www.gymzv.sk/sk/obsah/ucitelia_zoznam")

tbody = driver.find_element_by_xpath('/html/body/div[2]/div/div[3]/table/tbody')
for i in tbody:
    print(i.text)

