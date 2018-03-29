#!/usr/bin/python3

import re
import requests
from bs4 import BeautifulSoup

# works because of the stored cookie

# url = 'https://www.criticker.com/signin.php'
url1 = 'https://www.criticker.com/films/?filter=e44312'

def get_watchlist():
    # session = requests.Session()
    # r = session.get(url1)
    r = requests.get(url1)
    print(r.text)
    soup = BeautifulSoup(r.text, "html.parser")
    tags = soup.find_all('div', 'fl_name')
    prob_scores = soup.find_all("div", "fl_titlelist_score")
    if len(prob_scores) != len(tags):
        print('Warning: number of titles differs from number of titles; {} != {}'.format(len(tags), len(prob_scores)))
    return [_.text for _ in tags], [_.text for _ in prob_scores]

def get_formated_string(watchlist):
    header = 'Watch List:\n'
    max_title_len = max(len(title) for title in watchlist[0])
    body = ''
    for title, score in zip(watchlist[0], watchlist[1]):
        body += '{} {}: {}\n'.format(title, ' '*(max_title_len-len(title)), score)
    return header + body


if __name__ == '__main__':
    wl = get_watchlist()
    output = get_formated_string(wl)
    print(output)


#     session.post(url, data=dict(
#     email="me@domain.com",
#     password="secret_value"
#     ))
