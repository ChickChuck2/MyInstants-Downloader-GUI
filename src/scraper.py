from bs4 import BeautifulSoup
import requests
import re

HEADERS = {
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Methods': 'GET',
    'Access-Control-Allow-Headers': 'Content-Type',
    'Access-Control-Max-Age': '3600',
    'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0'
}

def get_audio_size_kb(url):
    try:
        r = requests.get(url, headers=HEADERS, timeout=5)
        return round(len(r.content) / 1024, 1)
    except:
        return 0.0

def extract_color(tag):
    try:
        div = tag.parent.find('div', class_='small-button-background')
        style = div.get('style', '')
        if 'background-color:' in style:
            return style.split('background-color:')[1].split(';')[0].strip()
    except:
        pass
    return '#888888'

def parse_items(soup):
    url_list = []
    l = soup.find_all(class_="small-button")
    c = 0
    for k in l:
        u = k['onclick']
        title = re.findall(str(re.escape('Play'))+"(.*)"+str(re.escape('sound')), k.get('title', ''))
        if title:
            title = title[0].strip()
        else:
            title = "Sound"
            
        color = extract_color(k)
        
        o = u.split('\'')
        if len(o) > 1:
            url = f'https://www.myinstants.com{o[1]}'
            size = get_audio_size_kb(url)
            url_list.append({
                'url': url,
                'title': title,
                'color': color,
                'size_kb': size
            })
            c += 1
            if c > 9: # Limit to 10 for performance since size download is synchronous
                break
    return url_list

def searchq(query:str):
    query = query.replace(' ','+')
    u = f'https://www.myinstants.com/en/search/?name={query}'
    content = requests.get(url=u, headers=HEADERS).content
    soup = BeautifulSoup(content, 'html.parser')
    return parse_items(soup)

def getPage(page: str):
    if int(page) == 1:  
        u = f'https://www.myinstants.com/en/index/us/?page={page}'
    else:
        u = f'https://www.myinstants.com/en/trending/us/?page={page}'
    content = requests.get(url=u, headers=HEADERS).content
    soup = BeautifulSoup(content, 'html.parser')
    return parse_items(soup)
