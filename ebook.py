from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from docx import Document
import time
from bs4 import BeautifulSoup

# Set up Chrome WebDriver with options
chrome_options = Options()
chrome_options.add_argument("--start-maximized")  # Maximize the browser window
chrome_options.add_argument("--disable-blink-features=AutomationControlled")  # Disable browser automation detection
chrome_options.add_argument("--force-device-scale-factor=0.7")  # Set zoom level to 60%
driver = webdriver.Chrome(options=chrome_options)

# Open the URL
url = "https://ifac-digital-standards-pub.web.app/?sid=session123&nid=4034555&memtype=WEB&name=test&admin=iesba"
driver.get(url)

# Function to click elements and wait for a certain time
def click_and_wait(xpath, wait_time=10):
    try:
        element = WebDriverWait(driver, wait_time).until(EC.element_to_be_clickable((By.XPATH, xpath)))
        element.click()
        return True
    except Exception as e:
        print(f"Error occurred while clicking: {e}")
        return False

# Click accept button
accept_button_xpath = "/html/body/div/div/div[1]/div/p[4]/label/input"
click_and_wait(accept_button_xpath)

# Handle browser pop-up asking for permission to copy content
try:
    alert = driver.switch_to.alert
    alert.accept()  # Accept the alert (Allow)
    print("Permission to copy content was allowed.")
except:
    print("No pop-up asking for permission to copy content found.")

# Wait for the content to load
time.sleep(20)

# Click another accept button
accept_button1_xpath = "/html/body/div/div/div[1]/div/button"
click_and_wait(accept_button1_xpath)

# Wait for the content to load
time.sleep(20)

# Click IAASB button
iaasb_button_xpath = "/html/body/div[1]/div/div/div[2]/div/div[4]/div[1]/ul/li[1]/button"
click_and_wait(iaasb_button_xpath)

# Wait for the content to load
time.sleep(20)

# Click volume1 button
iaasb_button_xpath = "/html/body/div/div/div[1]/aside[1]/div[3]/div/div[1]/a"
click_and_wait(iaasb_button_xpath)

# Wait for the content to load
time.sleep(20)

# Get the HTML content of the specific element on the page
page_content_element = driver.find_element(By.XPATH, "//*[@id='root']/div/div[1]/main/article/div")
page_html = page_content_element.get_attribute("outerHTML")

# Read formatted text from local Word file
word_formatted_text = ""
try:
    doc = Document("A002 2022 IAASB Handbook Changes - Changes of Substance WBcomments.docx")
    for paragraph in doc.paragraphs:
        # Extract formatted text from each paragraph
        formatted_text = ""
        for run in paragraph.runs:
            formatted_text += run.text  # Extract text from the run
            # Check formatting attributes and apply them as needed
            if run.bold:
                formatted_text = f"<strong>{formatted_text}</strong>"
            if run.italic:
                formatted_text = f"<em>{formatted_text}</em>"
            if run.underline:
                formatted_text = f"<u>{formatted_text}</u>"
            # You can add more formatting checks here based on your requirements
        # Add the formatted text of the paragraph to the overall text
        word_formatted_text += formatted_text + "<br>"
except Exception as e:
    print("Error occurred while reading local Word file:", e)

# Compare HTML content with formatted text
soup_page = BeautifulSoup(page_html, "html.parser")
soup_word = BeautifulSoup(word_formatted_text, "html.parser")

print(soup_page)
print(soup_word)

# Compare text formatting
page_elements = soup_page.find_all(["p", "h1", "h2", "h3", "h4", "h5", "h6", "li", "strong", "em", "u"])
word_elements = soup_word.find_all(["p", "h1", "h2", "h3", "h4", "h5", "h6", "li", "strong", "em", "u"])

def compare_format(page_elem, word_elem):
    # Compare formatting attributes such as tag and text
    return page_elem.name == word_elem.name and page_elem.text == word_elem.text

for page_elem, word_elem in zip(page_elements, word_elements):
    if not compare_format(page_elem, word_elem):
        print("Formatting does not match.")
        print("Page:", page_elem)
        print("Word:", word_elem)
        print()  # Empty line for readability
    else:
        print("Formatting matches.")

# Close the browser
driver.quit()
