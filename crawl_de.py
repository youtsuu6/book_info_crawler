import requests
import json
import re
import datetime
from bs4 import BeautifulSoup


def convert_release_date(release_date):
    date_str = re.sub(r'年|月', '-', release_date).replace('日', '').rstrip('発売')
    split_str = date_str.split('-')
    result = datetime.date(int(split_str[0]), int(split_str[1]), int(split_str[2]))
    return str(result)


def get_html(html, class_name):
    soup = BeautifulSoup(html.text, "html.parser")
    tag = soup.find_all('li', attrs={'class': class_name})
    url = tag[1].find("a").get("href")
    return requests.get(url)


def get_books(tags):
    result = {'books': []}
    for tag in tags:
        detail_link = tag.find('h2', attrs={'class': 'p-books-media__title'})
        details = tag.find('table', attrs={'class': 'p-books-media02__info d-none d-md-table'})
        detail = details.find_all('tr')
        release_date = convert_release_date(detail[2].find('td').string)

        result['books'].append(
            {
                'title': detail_link.a.string,
                'url': detail_link.a.get("href"),
                'release_date': release_date
            }
        )
    return result


class_names = ['p-new-magazine-topicpath__item', 'p-new-magazine-topicpath__item -next']
top_html = requests.get('https://dengekibunko.jp/')

for class_name in class_names:

    soup = BeautifulSoup(get_html(top_html, class_name).text, "html.parser")

    book_tags = soup.find_all('div', attrs={'class': 'media'})

    books = get_books(book_tags)
    print(books)

    # API呼び出し
    api_url = 'http://localhost/api/books'
    headers = {"Content-Type": "application/json"}
    json_data = json.dumps(books).encode("utf-8")
    loaded_r = json.loads(json_data)
    print(loaded_r)

    r_post = requests.post(api_url, headers=headers, json=loaded_r)

    print(r_post)
    print(r_post.text)
