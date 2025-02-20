import requests, json, hashlib
import urllib3
from bs4 import BeautifulSoup
from urllib.parse import unquote
def get_data(fandom, language,category):
    url = ("https://{}.fandom.com/{}/api/v1/Articles/List?expand=1&category={}&limit=10000".format(fandom,language,category))
    r = requests.get(url)
    response = r.json()
    return response["items"]

def get_detail(fandom,link):
    url = ("https://{}.fandom.com/api.php?action=query&prop=pageprops&titles={}&format=json".format(fandom,link))
    r = requests.get(url)
    response = r.json()
    return response

def get_image(fandom,n):
    a=hashlib.md5(n.encode()).hexdigest()
    image_formats = ("image/png", "image/jpeg", "image/jpg", "image/webp")
    image=f"https://static.wikia.nocookie.net/{fandom}/images/{a[0]}/{a[:2]}/{n}"
    r = requests.head(image)
    if r.headers["content-type"] in image_formats:
        if r.status_code!=404:
            return image
        else:
            return False
    else:
        return False

def get_table(fandom,page,classname,next=None,number=None):
    link="https://{}.fandom.com/wiki/{}".format(fandom,page)
    # http = urllib3.PoolManager()
    # run = http.request('GET', link)
    # web = run.data

    page = requests.get(link)
    web=page.text

    table = unquote(web)
    table = BeautifulSoup(table, 'html.parser')
    table = table.find('table', {'class': classname})
    if next:
        table = table.parent.find_all('table')[number]
    table = table.find_all('tr')
    return table