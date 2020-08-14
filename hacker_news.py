#!/usr/bin/env python3
"Scrapes the data from the Hacker News obeying the robots.txt"

from datetime import datetime as dnt
import requests
from bs4 import BeautifulSoup


def create_custom_hackernews(links, subtext, min_points):
    """Returns a list of dictionaries with title,
    link and votes from Hacker News."""
    hacker_news = []
    for idx, itm in enumerate(links):
        title = itm.getText()
        href = itm.get('href', None)
        vote = subtext[idx].select('.score')
        if len(vote) > 0:
            points = int(vote[0].getText().split()[0])
            if points > min_points:
                hacker_news.append({'title': title, 'link': href, 'votes': points})
    return hacker_news

def main(pages):
    "Returns a list of the entire news depending on the threshold points."
    news = list()
    threshold_points = int(input('Minimum points: '))
    for page in range(pages):
        response = requests.get(f'https://news.ycombinator.com/news?p={page + 1}')
        html = BeautifulSoup(response.text, 'html.parser')
        links = html.select('.storylink')
        subtext = html.select('.subtext')
        news += create_custom_hackernews(links, subtext, threshold_points)
    return sorted(news, key=lambda k: k['votes'], reverse=True)

if __name__ == '__main__':
    with open(f'news@{dnt.now().strftime("%Y-%m-%d_%X")}.txt', 'w') as file:
        for item in main(int(input('Number of pages to scrape: '))):
            file.write(''.join(['[Title] : ' + item['title'], '\n',
                                '[Link]  : ' + item['link'], '\n',
                                '[Votes] : ' + str(item['votes']), '\n\n']))
        print(' '.join([f'Checkout the file <news@{dnt.now().strftime("%Y-%m-%d_%X")}.txt',
                        'in the present working directory!']))
