import os
import time
import requests
from bs4 import BeautifulSoup
import json

headers = {
    "Access-Control-Allow-Origin": "*",
    "Access-Control-Allow-Methods": "GET",
    "Access-Control-Allow-Headers": "Content-Type",
    "Access-Control-Max-Age": "3600",
    "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0",
}

urls = [
    {
        "id": 1,
        "category": "mulla_stories",
        "url": "https://www.tamilsurangam.in/general_knowledge/mulla_stories/index.html",
    },
    {
        "id": 2,
        "category": "brahmartha_guru_stories",
        "url": "https://www.tamilsurangam.in/general_knowledge/brahmartha_guru_stories/index.html",
    },
    {
        "id": 3,
        "category": "akbar_birbal_stories",
        "url": "https://www.tamilsurangam.in/general_knowledge/akbar_birbal_stories/index.html",
    },
    {
        "id": 4,
        "category": "aesop_fables_stories",
        "url": "https://www.tamilsurangam.in/general_knowledge/aesop_fables/index.html",
    },
    {
        "id": 5,
        "category": "mariyadai_raman_stories",
        "url": "https://www.tamilsurangam.in/general_knowledge/mariyadai_raman_stories/index.html",
    },
    {
        "id": 6,
        "category": "short_stories",
        "url": "https://www.tamilsurangam.in/general_knowledge/short_stories/index.html",
    },
]


def run_scrapper(urls: list):
    for index, item in enumerate(urls):
        print(f"Scraping category: {index+1}...")
        req = requests.get(item["url"], headers)
        soup = BeautifulSoup(req.content, "html.parser")
        stories_list = get_story_list(soup, item["category"], item["url"])
        save_as_json(stories_list, item["category"])
        time.sleep(10)


def get_story_list(soup: BeautifulSoup, category, url: str):
    base_url = url.split("index.html")[0]
    stories_list = []
    list_items = soup.find("div", "print-div").blockquote.ul.find_all("li")
    for index, item in enumerate(list_items):
        stories_list.append(
            {
                "story_id": index + 1,
                "story_category": category,
                "story_title": item.a.string,
                "url": f"{base_url}{item.a['href']}",
            }
        )
    return stories_list


def save_as_json(dictionary_list, name):
    directory = os.getcwd() + "/stories"
    if not os.path.exists(directory):
        os.makedirs(directory)
    with open(directory + f"/{name}.json", "w") as outfile:
        # ensure_ascii=False to support Tamil string
        json.dump(dictionary_list, outfile, ensure_ascii=False, indent=2)


run_scrapper(urls)
