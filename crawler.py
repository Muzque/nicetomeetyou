import requests
from bs4 import BeautifulSoup
import json


def get_mainweb(url):
    res = requests.get(url=url)
    if res.status_code == 200:
        return res.text
    else:
        raise res.raise_for_status()


def etl_news_link(res):
    urls = list()
    soup = BeautifulSoup(res, "lxml")
    for s in soup.select("div[id='news_body'] a"):
        urls.append(s['href'])
    return urls


def etl_news_detail(res):
    news = dict()
    soup = BeautifulSoup(res, "lxml")
    s = soup.find("script", type='application/ld+json')
    info = json.loads(s.text)
    news['headline'] = info['headline']
    news['image'] = info['thumbnailUrl']
    news['keywords'] = info['keywords']
    news['story_id'] = float('.'.join(info['url'].split('/')[-2:]))
    news['datePublished'] = info['datePublished']
    news['dateModified'] = info['dateModified']
    news['author'] = info['author']['name']
    news['publisher'] = info['publisher']['name']
    news['logo'] = info['publisher']['logo']['url']
    n = 0
    news['context'] = ''
    for s in soup.select("div[id='story_body_content'] span p"):
        line = s.text
        if n == 0:
            news['figcaption'] = line.strip(' ')
            n = 1
        else:
            if len(line) > 0:
                news['context'] += line
    return news


def store_news(news):
    url_news = "http://127.0.0.1:8000/api/news/"
    res = requests.post(url=url_news, data=news)
    if res.status_code == 201:
        print('Success: id={}'.format(news['story_id']))
    else:
        print('Error: status_code={}, id={}'.format(res.status_code, news['story_id']))


def main():
    url = "https://nba.udn.com/nba/index?gr=www"
    res = get_mainweb(url=url)
    urls = etl_news_link(res)
    for pattern in urls:
        url = "https://nba.udn.com" + pattern
        res = requests.get(url=url)
        if res.status_code == 200:
            news = etl_news_detail(res.text)
            store_news(news)
        else:
            raise res.raise_for_status()


if __name__ == "__main__":
    main()
