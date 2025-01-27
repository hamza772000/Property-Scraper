#!/usr/local/bin/python3
import requests
from bs4 import BeautifulSoup
from scraper_common import *

def get_rooms_info(rooms_soup, previous_rooms=[]):
    '''
    Iterate rooms & return object list
    '''
    rooms = set()
    links_file = "seen_links.json"
    previous_rooms = load_existing_links(links_file)
    try:
        for room in rooms_soup.find_all('article'):
            room_id = int(room.find("a")['href'].split("flatshare_id=")[1].split("&")[0])
            rooms.add(room_id)
        
        new_rooms = rooms - previous_rooms
        previous_rooms.update(new_rooms)
        if new_rooms:
            save_links(links_file, previous_rooms)
        return [f"https://www.spareroom.co.uk/flatshare/flatshare_detail.pl?flatshare_id={room_id}" for room_id in new_rooms]
    except Exception as e:
        print("Catch exception: ", e)

def spareroom_main():
    url = "https://www.spareroom.co.uk/flatshare/index.cgi?search_id=1344571808&mode=list"
    r = requests.get(url, allow_redirects=False)
    soup = BeautifulSoup(r.content, 'html.parser')
    pages = int(soup.find(id="results_header").find_all('strong')[1].text.strip()) // 10
    outputs = []
    # Spareroom only shows 10 results per page, so we need to loop through all pages
    for i in range(0, (pages+1) * 10, 10):
        url = f"https://www.spareroom.co.uk/flatshare/index.cgi?offset={i}&search_id=1344571808&mode=list"
        r = requests.get(url, allow_redirects=False)
        soup = BeautifulSoup(r.content, 'html.parser')
        outputs.extend(get_rooms_info(soup))
    return outputs

if __name__ == "__main__":
    spareroom_main()
