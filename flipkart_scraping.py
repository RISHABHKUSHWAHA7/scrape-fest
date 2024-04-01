import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup

url = "https://www.flipkart.com/mobile-phones-store?fm=neo%2Fmerchandising&iid=M_1c16a7a7-30d8-4ef7-89c9-f24951357f17_1_372UD5BXDFYS_MC.ZRQ4DKH28K8J&otracker=hp_rich_navigation_2_1.navigationCard.RICH_NAVIGATION_Mobiles_ZRQ4DKH28K8J&otracker1=hp_rich_navigation_PINNED_neo%2Fmerchandising_NA_NAV_EXPANDABLE_navigationCard_cc_2_L0_view-all&cid=ZRQ4DKH28K8J"

driver = webdriver.Chrome()

try:
    driver.get(url)

    while True:
        try:
            load_more_button = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, "//button[contains(text(),'Load More')]")))
            load_more_button.click()
        except:
            break

    page_source = driver.page_source

    soup = BeautifulSoup(page_source, 'html.parser')
    
    data = []

    anchor_tags = soup.find_all("a", class_="s1Q9rs")
    prices = soup.find_all("div", class_="_30jeq3")
    discount_divs = soup.find_all("div", class_="_3Ay6Sb")
    actual_prices_divs = soup.find_all("div", class_="_3I9_wc")

    for i in range(len(anchor_tags)):
        mobile_data = {}
        mobile_data["Name"] = anchor_tags[i].text.strip()
        mobile_data["Price"] = prices[i].text.strip().replace("\u20b9", "")  # Remove the ₹ symbol
        mobile_data["Actual_Price"] = actual_prices_divs[i].text.strip().replace("\u20b9", "") if i < len(actual_prices_divs) else None
        mobile_data["Discount"] = discount_divs[i].text.strip() if i < len(discount_divs) else None
        mobile_data["Link"] = "https://www.flipkart.com" + anchor_tags[i].get("href")
        data.append(mobile_data)

    with open("flipkart_mobile_sale_data.json", "w") as json_file:
        json.dump(data, json_file, indent=4)
        
    print("Data saved to mobile_data.json successfully!")

except Exception as e:
    print("An error occurred:", e)

finally:
    driver.quit()
