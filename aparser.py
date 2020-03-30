from selenium import webdriver
from lxml.html import fromstring
import json
from datetime import datetime

def get_source_code(agent, url):
  agent.get(url)
  source_code = fromstring(agent.page_source)
  return source_code


# this func parses all the elements of the article and puts them into dict
def article_parser(agent, source_code):
  article_data = {}  # dict for json
  
  # title
  title = source_code.xpath("//h1/text()")[0]
  title = title.strip()
  article_data['title'] = title
  
  # text
  text_lxml = source_code.xpath("//div[@class='entry-content']//p")
  text = ''
  for elem in text_lxml:
    if elem.get('class'):
      elem = ''
    else:
      text += str(elem.text_content())
  text = text.strip()
  article_data['text'] = text
  
  # author
  if source_code.xpath("//div[@class='entry-meta']/a[2]"):
    author = source_code.xpath("//div[@class='entry-meta']/a[2]/text()")[0]
    author_url = source_code.xpath("//div[@class='entry-meta']/a[2]/@href")[0]
    article_data['author'] = [author, author_url]
  else:
    author = 'no author'
    author_url = 'no url'
  
  # date
  date = source_code.xpath("//span[@class='entry-date']/text()")[0]
  date = date.split(' ')
  date = date[0][0:3] + ' ' + date[1].strip(',') + ' ' + date[2]
  date_datetime = str(datetime.strptime(date, '%b %d %Y'))
  article_data['date'] = date_datetime
  
  # categories
  if source_code.xpath("//div[@class='cat-links']/a/text()"):
    cats = source_code.xpath("//div[@class='cat-links']/a/text()")
    cat_urls = source_code.xpath("//div[@class='cat-links']/a/@href")
    article_data['cats'] = cats
    article_data['cat_urls'] = cat_urls
  
  # tags
  if source_code.xpath("//div[@class='tag-link']/a/text()"):
    tags = source_code.xpath("//div[@class='tag-link']/a/text()")
    tag_urls = source_code.xpath("//div[@class='tag-link']/a/@href")
    article_data['tags'] = tags
    article_data['tag_urls'] = tag_urls
  
  # pictures
  pic_urls = source_code.xpath("//div[@class='entry-content']//img")
  pic_urls_data = []
  for elem in pic_urls:
    pic_urls_data.append(elem.get('src'))
  article_data['pic_urls'] = pic_urls_data
  
  return article_data


# reads article url from articles.json file (see qparser.py)
with open ('articles.json', 'r') as f:
  article_link_data = f.read()
article_link_data = json.loads(article_link_data)

if __name__ == '__main__':
    driver = webdriver.Firefox(executable_path='geckodriver',  
                    firefox_binary='/Applications/Firefox Developer Edition.app/Contents/MacOS/firefox-bin')
    
    # every article content is put into json file
    for i in range(len(article_link_data)):
      url = article_link_data[str(i)]
      source_code = get_source_code(driver, url)
      article_data = article_parser(driver, source_code)
      with open('articles/article{}.json'.format(i), 'w') as f:
        json.dump(article_data, f, indent=4)
    
    driver.quit()
  