from selenium import webdriver
from lxml.html import fromstring
import json
import time

def main(agent):
    def first_page():
        # объект Селениум, через который мы взаимодействуем с веббраузером
        agent.get('https://www.enterpriseai.news/')

        source_code = fromstring(agent.page_source)
        title_list = source_code.xpath("//div[@class='news-listing-title']//a")
        href = title_list[0].get('href')
        return href
        # a = driver.find_element_by_xpath("//div[@class='news-listing-title']//a")
        # a.click()

    def urls():
        url = first_page()
        agent.get(url)
        source_code = fromstring(agent.page_source)
        time.sleep(1)
        title = source_code.xpath("//h1[@class='entry-title-single']")[0].text_content()
        author = source_code.xpath("//a[@href='https://www.enterpriseai.news/author/george/']")[0].text_content()
        date = source_code.xpath("//span[@class='entry-date']")[0].text_content()
        time.sleep(3)
        text = source_code.xpath("//div[@id='post-41849']")[0].text_content()[95:2771]
        time.sleep(3)

        dict_to_json = {'title' : title, 
        'author': author,
        'date' : date,
        'text' : text}

        with open('data.json', 'w', encoding='UTF-8') as outfile:
            json.dump(dict_to_json, outfile)
        print('ok')
    
    urls()
  

if __name__ == '__main__':
    driver = webdriver.Firefox(executable_path='geckodriver',  
                    firefox_binary='/Applications/Firefox Developer Edition.app/Contents/MacOS/firefox-bin')
    main(driver)
    driver.quit()