import os

from bs4 import BeautifulSoup as bs
import requests

def get_link_to_retell(url: str) -> dict:
  endpoint = 'https://300.ya.ru/api/sharing-url'
  response = requests.post(
      endpoint,
      json = {
        'article_url': url
      },
      headers = {'Authorization': f'OAuth {os.environ["YANDEX_API"]}'}
      )
  return response.json()

def get_retell(link_to_retell: str):
  r = requests.get(link_to_retell)
  r.encoding='utf-8'
  soup = bs(r.text, 'lxml')
  main_block = soup.find("div", class_='container').find_all("div", class_='content')[-1]
  title = main_block.find("div", class_='content-title').text.strip()
  content = [f'• {i.text.strip()}' for i in main_block.find("div", class_='content-theses').find_all('li')]


  return {"title":title,
          "content": content}

if __name__ == '__main__':
  get_retell('https://300.ya.ru/PORvfLcd')