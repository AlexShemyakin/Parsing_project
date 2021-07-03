import sqlite3
import bs4
from selenium import webdriver
from selenium.common.exceptions import ElementNotInteractableException, NoSuchElementException
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

cursor = None

def get_first_page(query):
    chrome_options = Options()
    #chrome_options.add_argument('user-data-dir=selenium')
    chrome_options.add_argument("--headless")
    driver = webdriver.Chrome(ChromeDriverManager().install(), options=chrome_options)
    driver.get('https://spb.hh.ru/')


    search_box = driver.find_element_by_name("text")
    #ловим exception в случая открытия главной страницы в другом виде
    try:
        search_box.send_keys(query)
    except ElementNotInteractableException:
        search_box = driver.find_element_by_xpath("/html/body/div[5]/div[3]/div/div[1]/div[3]/div/div/ol/li[2]/a")
        search_box.click()
        search_box = driver.find_element_by_name("text")
        search_box.send_keys(query)
    search_box.submit()
    search_box = driver.find_elements_by_class_name("g-user-content")
    list_of_key_word = []

    def parsing():
        # ВРЕМЕННАЯ СТРОКА!!!
        #driver.switch_to.window(driver.window_handles[1])
        for count in search_box:
            if count.tag_name == 'span':
                count.click()
                driver.switch_to.window(driver.window_handles[-1])
                try:
                    search_box_2 = driver.find_elements_by_class_name("bloko-tag__section")
                except NoSuchElementException:
                    driver.close()
                    # [0] - if headless - ON, [1] - if headless - OFF
                    driver.switch_to.window(driver.window_handles[0])
                    continue
                for i in search_box_2:
                    list_of_key_word.append(i.text)
                driver.close()
                # [0] - if headless - ON, [1] - if headless - OFF
                driver.switch_to.window(driver.window_handles[0])
        return

    parsing()

    while True:
        try:
            search_box = driver.find_element_by_xpath("/html/body/div[6]/div/div[1]/div[4]/div/div/div[3]/div[2]/div/div[8]/div/span[3]/a")
        except NoSuchElementException:
            break
        search_box.click()
        search_box = driver.find_elements_by_class_name("g-user-content")
        parsing()

    def dict_from_list(lst):
        dictionary = {key: lst.count(key) for key in set(lst)}
        dictionary = sorted(dictionary.items(), key=lambda item: -item[1])
        return dictionary

    dictionary = dict_from_list(list_of_key_word)

    conn = sqlite3.connect("database.db")
    global cursor
    cursor = conn.cursor()
    cursor.execute("""DROP TABLE log""")
    cursor.execute("""CREATE TABLE log
    (name text, count text);
    """)
    log = []
    for i in dictionary:
        log.append((f'{i[0]}', f'{i[1]}'))
    cursor.executemany("""INSERT INTO log VALUES(?,?);""", log)
    conn.commit()

    return
