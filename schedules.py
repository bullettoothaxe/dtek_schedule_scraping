import time

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from functools import cache

from selenium.webdriver.chrome.service import Service as BraveService
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.core.utils import ChromeType

from env import CITY, STREET, HOUSE


def class_name_to_message(class_name):
    if class_name == 'cell-non-scheduled':
        return '✅'  # '💡'  # light
    elif class_name == 'cell-scheduled-maybe':
        return '🤷'  # maybe
    elif class_name == 'cell-scheduled':
        return '🚫'  # '🕯'  # shutdown


schedule_time = [
    '00-01',
    '01-02',
    '02-03',
    '03-04',
    '04-05',
    '05-06',
    '06-07',
    '07-08',
    '08-09',
    '09-10',
    '10-11',
    '11-12',
    '12-13',
    '13-14',
    '14-15',
    '15-16',
    '16-17',
    '17-18',
    '18-19',
    '19-20',
    '20-21',
    '21-22',
    '22-23',
    '23-24',
]


def get_scheduled_signals(tds):
    messages = []

    for td in tds:
        class_name = td['class'][0]
        if class_name == 'current-day':
            messages.append(td.text.strip())
        else:
            messages.append(class_name_to_message(class_name))

    return messages


def prepare_client_message(signals):
    message = f"{signals[0]}:\n\n"

    for index, period in enumerate(schedule_time):
        message += f"{period}: {signals[index+1]} \n"

    return message


def get_html_to_scrape():
    url = "https://www.dtek-oem.com.ua/ua/shutdowns"

    options = webdriver.ChromeOptions()

    # options.add_argument("--headless")
    # options.add_argument("--disable-extensions")
    # options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--no-sandbox")

    driver = webdriver.Chrome(options=options)

    # driver = webdriver.Chrome(service=BraveService(ChromeDriverManager(chrome_type=ChromeType.BRAVE).install()),
    #                           options=options)

    driver.get(url)

    time.sleep(3)

    city = driver.find_element(By.ID, "city")
    city.click()
    city.send_keys(CITY)
    driver.find_element(By.ID, "cityautocomplete-list").click()

    time.sleep(3)

    street = driver.find_element(By.ID, "street")
    street.click()
    street.send_keys(STREET)
    driver.find_element(By.ID, "streetautocomplete-list").click()

    time.sleep(3)

    house = driver.find_element(By.ID, "house_num")
    house.click()
    house.send_keys(HOUSE)
    driver.find_element(By.ID, "house_numautocomplete-list").click()

    time.sleep(3)

    html = driver.page_source

    driver.close()
    driver.quit()

    return html


@cache
def get_schedule_message(date):
    html = get_html_to_scrape()
    soup = BeautifulSoup(html, 'lxml')
    today_row = soup.find(id="tableRenderElem").find(class_="yesterday-row").find_next('tr')
    tds = today_row.find_all('td')
    signals = get_scheduled_signals(tds)
    message = prepare_client_message(signals)
    final_message = f"{date}\n\n{message}"

    return final_message
