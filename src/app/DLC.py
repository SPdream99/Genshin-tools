import requests
import sys
import webbrowser
import shutil
import os
import unicodedata
import codecs
from os import path
if not os.path.isdir('Data'):
   os.makedirs('Data')
if not os.path.isdir('ImageDownloads'):
   os.makedirs('ImageDownloads')
filepath=os.path.dirname(__file__)
filepath=filepath+"/"
g2='0'
url2=('https://fategrandorder.fandom.com/api.php?action=query&prop=imageinfo&titles={}&iiprop=url&format=json'.format(g2))
url = ('https://fategrandorder.fandom.com/api.php?action=query&prop=images&titles=Stheno&imlimit=500&imdir=ascending&format=json')
r = requests.get(url)
response = r.json()
for item in response['query']['pages']:
 print(item)
 g3=item
for item in response["query"]["pages"][g3]["images"]:
 print(item['title'])
 g2=item['title']
 url2=('https://fategrandorder.fandom.com/api.php?action=query&prop=imageinfo&titles={}&iiprop=url&format=json'.format(g2))
 r = requests.get(url2)
 response = r.json()
 for item in response['query']['pages']:
  g4=item
  for item2 in response['query']['pages'][g4]['imageinfo']:
   print(item2['url'])

 
