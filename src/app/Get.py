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
Category="0"
CategoryHistory='0'
Clist='0'
timesearch=1
l=0
UseChoice= input("Do you want to continue last session and load file or manually make new?(Type '1' for new, '2' or anything else to continue and load):")
if UseChoice=='1':
 c=0
 SearchSever=0
 UseChoice= input("Do you want to use search engine or manually type?(Type '1' or anything else for SE, '2' for MT):")
 if UseChoice=='2':
  print('please type * from *.fandom.com')
  web= input('Wikia Page:')
  Language=input("Please type the language(left blank for no):")
  if Language=='':
   Language="fno"
  Category=input('Please type the category:')
 else:
  SearchSever=input('Which sever do you prefer(type 1 to 3)(left blank for 1):')
  while SearchSever!='1' and SearchSever!='2' and SearchSever!='3' and SearchSever!='':
   SearchSever=input('Please type from 1 to 3 or left blank for 1:')
  if SearchSever=='1':
   SearchEngine='https://www.googleapis.com/customsearch/v1?key=AIzaSyDzD5Dvul_q2JWU9H9w8hHO60VCzCkQSqA&cx=008331698482042685776:vjamtz9lq0y&q='
  elif SearchSever=='2':
   SearchEngine='https://www.googleapis.com/customsearch/v1?key=AIzaSyCmlZZfQg-zSwUwy7uibDh7Xw8sAEoV0xw&cx=008331698482042685776:vjamtz9lq0y&q='
  elif SearchSever=='3':
   SearchEngine='https://www.googleapis.com/customsearch/v1?key=AIzaSyDaHW1prjdrmJpsQ0kEsgS__fbdrJH8tU0&cx=008331698482042685776:vjamtz9lq0y&q='
  elif SearchSever=='':
   SearchSever='1'
   SearchEngine='https://www.googleapis.com/customsearch/v1?key=AIzaSyDzD5Dvul_q2JWU9H9w8hHO60VCzCkQSqA&cx=008331698482042685776:vjamtz9lq0y&q='
  print('Sever: Sever '+SearchSever)
  Search=input('please type what wikia you want to find:')
  SearchEngineO=SearchEngine+Search+'&start='+str(timesearch)
  r = requests.get(SearchEngineO)
  response = r.json()
  print('')
  print('Wikia list:')
  if r.status_code == 200:
   for item in response['items']:
    c += 1
    print("No.{} {}".format(str(c),item['title']))
    print("Link: {}".format(item['link']))
    print('')
    later=c
  else:
   sys.stdout = open(filepath+"Data/log.txt", "w", encoding="utf-8")
   print(SearchEngineO)
   print('Sever '+SearchSever+': No response')
   sys.stdout.close()
  NeedWikia=input("please type wikia number you want(type 'n' for next page(page 10 is the last), 'p' for previous page):")
  if NeedWikia!='n' and NeedWikia!='p':
   while int(NeedWikia)>int(later):
    NeedWikia = input("Please type in number in the list:")
  while NeedWikia=='n' or NeedWikia=='p':
   while NeedWikia=='n':
    timesearch=timesearch+10
    SearchEngineO=SearchEngine+Search+'&start='+str(timesearch)
    r = requests.get(SearchEngineO)
    response = r.json()
    print('Page:'+str((timesearch-1)/10+1))
    print('Wikia list:')
    print('')
    if r.status_code == 200:
     c=0
     for item in response['items']:
      c += 1
      print("No.{} {}".format(str(c),item['title']))
      print("Link: {}".format(item['link']))
      print('')
      later=c
    else:
     sys.stdout = open(filepath+"Data/log.txt", "w", encoding="utf-8")
     print(SearchEngineO)
     print('Sever '+SearchSever+': No response')
     sys.stdout.close()
    NeedWikia=input("please type wikia number you want(type 'n' for next page(page 10 is the last), 'p' for previous page):")
   while NeedWikia=='p':
    if timesearch!=1:
     timesearch=timesearch-10
     SearchEngineO=SearchEngine+Search+'&start='+str(timesearch)
     r = requests.get(SearchEngineO)
     response = r.json()
     if ((timesearch-1)/10)!=0:
      print('Page:'+str((timesearch-1)/10+1))
     else:
      print('Page:1.0')
     print('Wikia list:')
     print('')
     if r.status_code == 200:
      c=0
      for item in response['items']:
       c += 1
       print("No.{} {}".format(str(c),item['title']))
       print("Link: {}".format(item['link']))
       print('')
       later=c
     else:
      sys.stdout = open(filepath+"Data/log.txt", "w", encoding="utf-8")
      print(SearchEngineO)
      print('Sever '+SearchSever+': No response')
      sys.stdout.close()
     NeedWikia=input("please type wikia number you want(type 'n' for next page(page 10 is the last), 'p' for previous page):")
    else:
     print('This is the first Page')
     NeedWikia=input("please type wikia number you want(type 'n' for next page(page 10 is the last), 'p' for previous page):")
   while NeedWikia=='n' or NeedWikia=='p' or int(NeedWikia)>int(later):
    NeedWikia = input("Please type the number in the list:")
  c=0
  for item in response['items']:
   c+=1
   if c==int(NeedWikia):
    Search=item['link']
    Search=Search.split("/")[2]
    Search=Search.split(".")[0]
    web=Search
    Search=item['link']
    Search=Search.split("/")[2]
    Search=Search.split("/wiki")[0]
    timesearch=1
    Language=input("Please type the language(left blank for no):")
    if Language=='':
     Language="fno"
    else:
     Search=Search+'/'+Language
    What=input("please type Category you want to find(Left blank if you don't need):")
    SearchEngineO=(SearchEngine+Search+" category: ")
    SearchEngineO=SearchEngineO+What
    r = requests.get(SearchEngineO)
    response = r.json()
    print('')
    print('Category list:')
    c=0
    if r.status_code == 200:
     for item in response['items']:
      c += 1
      Calink=item['link']
      titleCa=item['title']
      titleCa=titleCa.split("|")[0]
      if Search in Calink:
       if 'Category:' in Calink:
        print("No.{} {}".format(str(c),titleCa))
        print("Link: {}".format(item['link']))
        print('')
        laterr=c
    else:
     sys.stdout = open(filepath+"Data/log.txt", "w", encoding="utf-8")
     print(SearchEngineO)
     print('Sever '+SearchSever+': No response')
     sys.stdout.close()
    NeedCategory=input("please type Category number you want(if you want to type manually, type fno)(type 'n' for next page(page 10 is the last), 'p' for previous page):")
    if NeedCategory!="fno" or NeedCategory=='n' and NeedCategory=='p':
     if NeedCategory!='n' and NeedCategory!='p':
      while int(NeedCategory)>int(laterr):
       NeedCategory = input("Please type in number in the list:")
     while NeedCategory=='n' or NeedCategory=='p':
      while NeedCategory=='n':
       timesearch=timesearch+10
       SearchEngineO=(SearchEngine+Search+" category: ")
       SearchEngineO=SearchEngineO+What+'&start='+str(timesearch)
       r = requests.get(SearchEngineO)
       response = r.json()
       print('Page:'+str((timesearch-1)/10+1))
       print('Category list:')
       print('')
       if r.status_code == 200:
        c=0
        for item in response['items']:
         c += 1
         Calink=item['link']
         titleCa=item['title']
         titleCa=titleCa.split("|")[0]
         if Search in Calink:
          if 'Category:' in Calink:
           print("No.{} {}".format(str(c),titleCa))
           print("Link: {}".format(item['link']))
           print('')
           laterr=c
       else:
        sys.stdout = open(filepath+"Data/log.txt", "w", encoding="utf-8")
        print(SearchEngineO)
        print('Sever '+SearchSever+': No response')
        sys.stdout.close()
       NeedCategory=input("please type Category number you want(type 'n' for next page(page 10 is the last), 'p' for previous page):")
      while NeedCategory=='p':
       if timesearch!=1:
        timesearch=timesearch-10
        SearchEngineO=(SearchEngine+Search+" category: ")
        SearchEngineO=SearchEngineO+What+'&start='+str(timesearch)
        r = requests.get(SearchEngineO)
        response = r.json()
        if ((timesearch-1)/10)!=0:
         print('Page:'+str((timesearch-1)/10+1))
        else:
         print('Page:1.0')
        print('Category list:')
        print('')
        if r.status_code == 200:
         c=0
         for item in response['items']:
          c += 1
          Calink=item['link']
          titleCa=item['title']
          titleCa=titleCa.split("|")[0]
          if Search in Calink:
           if 'Category:' in Calink:
            print("No.{} {}".format(str(c),titleCa))
            print("Link: {}".format(item['link']))
            print('')
            laterr=c
        else:
         sys.stdout = open(filepath+"Data/log.txt", "w", encoding="utf-8")
         print(SearchEngineO)
         print('Sever '+SearchSever+': No response')
         sys.stdout.close()
        NeedCategory=input("please type Category number you want(type 'n' for next page(page 10 is the last), 'p' for previous page):")
       else:
        print('This is the first Page')
        NeedCategory=input("please type Category number you want(type 'n' for next page(page 10 is the last), 'p' for previous page):")
      while NeedCategory=='n' or NeedCategory=='p' or int(NeedCategory)>int(laterr):
       NeedCategory = input("Please type the number in the list:")
     print('')
     c=0
     for item in response['items']:
      c+=1
      if c==int(NeedCategory):
       Search=item['title']
       Search=Search.split("|")[0]
       Search=Search.split("Category:")[1]
       Category=Search
    else:
     Category=input('Please type the category:')
  url = ("https://{}.fandom.com/{}/api/v1/Articles/List?expand=1&category={}&limit=10000".format(web,Language,Category))
 CategoryHistory=(Category,"0")
 l=0
 Clist=list(CategoryHistory)
else:
 Data = os.listdir(filepath+'Data')
 p=0
 print('List of file:')
 for TXT in Data:
  if TXT!='log.txt' and TXT!='Last.txt':
   if '.txt' in TXT:
    p+=1
    print(str(p)+"."+TXT.split('.txt')[0])
 TXTFile=input('What file do you want to open(please type name)(Left blank for auto):')
 if TXTFile!='':
  TXTFile=TXTFile+".txt"
  if path.exists(filepath+"Data/"+TXTFile):
   with open(filepath+"Data/"+TXTFile,'r', encoding='utf8') as f:
    web=f.readline()
    web=web.split("\n")[0]
    Language=f.readline()
    Language=Language.split("\n")[0]
    Category=f.readline()
    Category=Category.split("\n")[0]
    l=f.readline()
    l=int(l)
    file_lines = f.read()
    Clist = file_lines.split("\n")
   print("web: "+web)
   print("Language: "+Language)
   print("Category: "+Category)
   print("History Category: "+str(l))
   print(Clist)
  else:
   sys.stdout = open(filepath+"Data/log.txt", "w", encoding="utf-8")
   print('no file exists')
   sys.stdout.close()
 else:
  if path.exists(filepath+'Data/Last.txt'):
   with open(filepath+'Data/Last.txt','r', encoding='utf8') as f:
    web=f.readline()
    web=web.split("\n")[0]
    Language=f.readline()
    Language=Language.split("\n")[0]
    Category=f.readline()
    Category=Category.split("\n")[0]
    l=f.readline()
    l=int(l)
    file_lines = f.read()
    Clist = file_lines.split("\n")
   print("web: "+web)
   print("Language: "+Language)
   print("Category: "+Category)
   print("History Category: "+str(l))
   print(Clist)
  else:
   sys.stdout = open(filepath+"Data/log.txt", "w", encoding="utf-8")
   print('no file exists')
   sys.stdout.close()
InfoChoice=input("Do you want to print info?(Type 'y' or anything else for yes, left blank for no):")
if InfoChoice=='':
    InfoChoice="n"
WebChoice=input("Do you want to open page?(Type 'y' or anything else for yes, left blank for no):")
if WebChoice=='':
    WebChoice="n"
webbrowser.register('firefox',
	None,
	webbrowser.BackgroundBrowser("/usr/bin/firefox"))
url = ("https://{}.fandom.com/{}/api/v1/Articles/List?expand=1&category={}&limit=10000".format(web,Language,Category))
if Language=='fno':
 url=(url.replace('/fno',''))
print('Link: {}'.format(url))
r = requests.get(url)
response = r.json()
# print response
urlname=0
idname=0
Titlenameee='0'
UC='n'
rname=0
Durl=0
Dlink="No Download"
Hchoice=0
Allow='n'
historyrun='false'
Filename=0
Choice=0
Hchoice=0
m=0
Hgo='false'
Printok='true'
NeedImage=0
a = 0
Fileu=0
Imagenameee=0
d=0
n=0
def Historyfind():
 n=0
 for CH in Clist:
  n+=1
  if n==Hchoice:
   Historyfind.Category=Clist[n-1]
def History():
 n=0
 print('Category History:')
 for CH in Clist:
  n+=1
  if (n-1)<=l:
   print(str(n)+"."+CH)
 History.last=n-1
 print('type * to go to the category you want, * is number of that category')
def findName():
 b=0
 for item in response['items']:
  b+=1
  if str(b)==NeedImage:
   findName.namee=item['title']
def getlist():
 b=0
 getlist.last=0
 for item in response['items']:
  b+=1
  if 'type' in item:
   if item['type']!='category':
    print("No.{} {}".format(str(b),item['title']))
   else:
    print("No.{}(Category) {}".format(str(b),item['title']))
  else:
   print("No.{}(Category) {}".format(str(b),item['title']))
  getlist.last=b
print("Here is the list of contents:")
getlist()
print("Please use number on the list above")
NeedImage = input("Enter Image number you want to download(if you don't want, type 'n')(type 'h' to open History):")
if NeedImage=="n":
 print("As you want")
elif NeedImage=="h":
 History()
 Hchoice=input("Please Choose category to go:")
 while int(Hchoice)>int(History.last):
  Hchoice = input("Please type in number in the list:")
  if Hchoice=='':
   break
 if Hchoice!='':
  Hchoice=int(Hchoice)
  Hgo='true'
  Historyfind()
  NeedImage=0
  Category=Historyfind.Category
  url = ("https://{}.fandom.com/{}/api/v1/Articles/List?expand=1&category={}&limit=10000".format(web,Language,Category))
  r = requests.get(url)
  response = r.json()
  historyrun='true'
else:
 while int(NeedImage)>int(getlist.last):
  NeedImage = input("Please type in number in the list:")
 findName()
 print("You want {}'s Image, is it right?(Type 'y' or anything else for yes, 'n' for no)".format(findName.namee))
 Choice= input("Choice:")
 if Choice=="n" or Choice=="y":
  if Choice=="n":
   print("Then type again please:")
   while Choice=="n":
    NeedImage = input("Enter Image number you want to download(if you don't want any type 'n')(type 'h' to open History):")
    if NeedImage=="n":
     print("As you want")
     Choice="y"
    elif NeedImage=="h":
     History()
     Hchoice=input("Please Choose category to go:")
     while int(Hchoice)>int(History.last):
      Hchoice = input("Please type in number in the list:")
      if Hchoice=='':
       break
     if Hchoice!='':
      Hchoice=int(Hchoice)
      Hgo='true'
      Historyfind()
      NeedImage=0
      Category=Historyfind.Category
      url = ("https://{}.fandom.com/{}/api/v1/Articles/List?expand=1&category={}&limit=10000".format(web,Language,Category))
      r = requests.get(url)
      response = r.json()
      historyrun='true'
      Choice="y"
    else:
     while int(NeedImage)>int(getlist.last):
      NeedImage = input("Please type in number in the list:")
     findName()
     print("You want {}'s Image, is it right?(Type 'y' or anything else for yes, 'n' for no)".format(findName.namee))
     Choice= input("Choice:")
a=0
if historyrun=='true':
 NeedImage='1'
for item in response['items']:
 a += 1
 if str(a) == NeedImage:
  categorytype='category'
  if 'type' in item or historyrun=='true':
   if item['type']=='category' or historyrun=='true':
    while item['type']=='category' or historyrun=='true':
      if Hgo!='true':
       a=0
       for item in response['items']:
        a += 1
        if str(a) == NeedImage:
         Category=item['title']
       r = requests.get(url)
       response = r.json()
       if not Category in Clist:
        l+=1
        Clist[l]=Category
        Clist.insert(l+1,'0')
       url = ("https://{}.fandom.com/{}/api/v1/Articles/List?expand=1&category={}&limit=10000".format(web,Language,Category))
      else:
       url = ("https://{}.fandom.com/{}/api/v1/Articles/List?expand=1&category={}&limit=10000".format(web,Language,Category))
       Hgo='false'
      r = requests.get(url)
      response = r.json()
      print('This is a category, here is the content inside:')
      getlist()
      print("Please use number on the category list above")
      NeedImage = input("Enter Image number you want to download(if you don't want, type 'n')(type 'h' to open History):")
      if NeedImage=="n":
       print("As you want")
      elif NeedImage=="h":
       History()
       Hchoice=input("Please Choose category to go:")
       while int(Hchoice)>int(History.last):
        Hchoice = input("Please type in number in the list:")
        if Hchoice=='':
         break
       if Hchoice!='':
        Hchoice=int(Hchoice)
        Hgo='true'
        Historyfind()
        NeedImage=0
        Category=Historyfind.Category
      else:
       while int(NeedImage)>int(getlist.last):
        NeedImage = input("Please type in number in the list:")
       findName()
       print("You want {}'s Image, is it right?(Type 'y' or anything else for yes, 'n' for no)".format(findName.namee))
       Choice= input("Choice:")
       if Choice=="n" or Choice=="y":
        if Choice=="n":
         print("Then type again please:")
         while Choice=="n":
          NeedImage = input("Enter Image number you want to download(if you don't want any type 'n')(type 'h' to open History):")
          if NeedImage=="n":
           print("As you want")
           Choice="y"
          elif NeedImage=="h":
           History()
           Hchoice=input("Please Choose category to go:")
           while int(Hchoice)>int(History.last):
            Hchoice = input("Please type in number in the list:")
            if Hchoice=='':
             break
           if Hchoice!='':
            Hchoice=int(Hchoice)
            Hgo='true'
            Historyfind()
            NeedImage=0
            Category=Historyfind.Category
           Choice="y"
          else:
           while int(NeedImage)>int(getlist.last):
            NeedImage = input("Please type in number in the list:")
           findName()
           print("You want {}'s Image, is it right?(Type 'y' or anything else for yes, 'n' for no)".format(findName.namee))
           Choice= input("Choice:")
      a=0
      if NeedImage=="n":
       break
      if Hgo!='true':
       for item in response['items']:
        a += 1
        if str(a) == NeedImage:
         if 'type' in item:
          if item['type']=='category':
           categorytype='category'
          else:
           categorytype=0
           historyrun='false'
           break
         else:
           categorytype=0
           historyrun='false'
           break
a=0
print("Working...")
url = ("https://{}.fandom.com/{}/api/v1/Articles/List?expand=1&category={}&limit=10000".format(web,Language,Category))
if Language=='fno':
 url=(url.replace('/fno',''))
print('Link: {}'.format(url))
r = requests.get(url)
response = r.json()
for item in response['items']:
    a += 1
    if str(a) == NeedImage:
     if item['thumbnail'] is not None:
      Durl=item['thumbnail']
      Dlink = Durl.split("/smart")[0]
      if Language!='fno':
       Dlink=Dlink+('?path-prefix={}'.format(Language))
      if 'path-prefix=' in item['thumbnail']:
       if Language!='fno':
        Dlink=Dlink+('&path-prefix={}'.format(item['thumbnail'].split('path-prefix=')[1]))
       else:
        Dlink=Dlink+('?path-prefix={}'.format(item['thumbnail'].split('path-prefix=')[1]))
      Printok='true'
     else:
      Printok='false'
     Imagenameee=str(item['title'])
     Titlenameee=str(item['title'])
     if WebChoice!='n':
      webbrowser.get('firefox').open("https://{}.fandom.com{}".format(web,item['url']))
if NeedImage!="n":
 UC=input("This is just a thumbnail, do you want to get more image from this page(type 'y' for yes, 'n' and anything else for no):")
 if UC=='y':
  urlmore1=('https://{}.fandom.com/api.php?action=query&prop=images&titles={}&imlimit=500&imdir=ascending&format=json'.format(web,Imagenameee))
  r = requests.get(urlmore1)
  response = r.json()
  for item in response['query']['pages']:
   TitleID=item
  print('Here is the list of images related to the page:')
  print(urlmore1)
  for item in response["query"]["pages"][TitleID]["images"]:
   m+=1
   print("No."+str(m)+" "+item['title'])
  NeedImage=input('What file do you want?:')
  while int(NeedImage)>m:
   NeedImage=input('Please type number in the list:')
  m=0
  ImageN='0'
  for item in response["query"]["pages"][TitleID]["images"]:
   m+=1
   if m==int(NeedImage):
    ImageN=item['title'].split('File:')[1]
    if '.png' in ImageN or '.webp' in ImageN:
     if '.png' in ImageN:
      Imagenameee=ImageN.split('.png')[0]+" of "+Titlenameee
     else:
      Imagenameee=ImageN.split('.webp')[0]+" of "+Titlenameee
    else:
     Imagenameee=ImageN+" of "+Titlenameee
    urlmore2=('https://{}.fandom.com/api.php?action=query&prop=imageinfo&titles={}&iiprop=url&format=json'.format(web,item['title']))
    Allow=input("You want {}, is it right?(type 'y' or anything else for yes, 'n' for no):".format(Imagenameee))
    if Allow!='n':
     r = requests.get(urlmore2)
     response = r.json()
     for item in response['query']['pages']:
      ImageID=item
     for item in response['query']['pages'][ImageID]['imageinfo']:
      Dlink=item['url']
    else:
     while Allow=='n':
      NeedImage=input('What file do you want?:')
      while int(NeedImage)>m:
       NeedImage=input('Please type number in the list:')
      m=0
      for item in response["query"]["pages"][TitleID]["images"]:
       m+=1
       if m==int(NeedImage):
        ImageN=item['title'].split('File:')[1]
        if '.png' in ImageN or '.webp' in ImageN:
         if '.png' in ImageN:
          Imagenameee=ImageN.split('.png')[0]+" of "+Titlenameee
         else:
          Imagenameee=ImageN.split('.webp')[0]+" of "+Titlenameee
        else:
         Imagenameee=ImageN+" of "+Titlenameee
        urlmore2=('https://{}.fandom.com/api.php?action=query&prop=imageinfo&titles={}&iiprop=url&format=json'.format(web,item['title']))
        Allow=input("You want {}, is it right?(type 'y' or anything else for yes, 'n' for no):".format(Imagenameee))
        if Allow!='n':
         r = requests.get(urlmore2)
         response = r.json()
         for item in response['query']['pages']:
          ImageID=item
         for item in response['query']['pages'][ImageID]['imageinfo']:
          Dlink=item['url']
 print("Download Link:"+Dlink)
 Fileu=Imagenameee+".png"
 Filename=Imagenameee+".png"
 if Printok=='true':
  r = requests.get(Dlink, stream = True)
  if r.status_code == 200:
   while path.exists(filepath+"ImageDownloads/"+Fileu):
    d+=1
    FileChoice=input("{} already exists, do you want to replace?(Type 'y' for yes, 'n' or anything else for no):".format(Fileu))
    if FileChoice!='y':
     Filename=Imagenameee+str(d)+".png"
     Fileu=Filename
    else:
     Filename=Imagenameee+".png"
     break
   r.raw.decode_content = True
   with open(filepath+"ImageDownloads/"+Filename,'wb') as f:
    shutil.copyfileobj(r.raw, f)
   print('Image sucessfully Downloaded:',Filename)
  else:
   print('{} couldn\'t be retreived'.format(Filename))
 else:
  print("{} wasn't exists".format(Filename))
print("Write Log...")
TXTSave=input('Which name do you want to name your new profile(left blank for no):')
TXTSave=TXTSave+".txt"
if TXTSave!='':
 with open(filepath+"Data/"+TXTSave, 'w', encoding='utf-8') as f:
    f.write(web)
    f.write('\n')
    f.write(Language)
    f.write('\n')
    f.write(Category)
    f.write('\n')
    f.write(str(l))
    f.write('\n')
    f_lines = "\n".join(Clist)
    f.write(f_lines)
    f.close()
with open(filepath+'Data/Last.txt', 'w', encoding='utf-8') as f:
   f.write(web)
   f.write('\n')
   f.write(Language)
   f.write('\n')
   f.write(Category)
   f.write('\n')
   f.write(str(l))
   f.write('\n')
   f_lines = "\n".join(Clist)
   f.write(f_lines)
   f.close()
sys.stdout = open(filepath+"Data/log.txt", "w", encoding="utf-8")
print('===Lists===')
a=0
r = requests.get(url)
response = r.json()
for item in response['items']:
    a += 1
    print("No.{} {} {}".format(str(a),item['title'],item['id']))
    if str(a) == NeedImage:
     print('Download Image link:')
     print(Dlink)
    idname=item['id']
    urlname="https://{}.fandom.com/{}/api/v1/Articles/Details?ids={}&abstract=90".format(web,Language,str(idname))
    rname = requests.get(urlname)
    response = rname.json()
    if InfoChoice!='n':
     print("Info: {}".format(item['abstract']))
     print('')
print('===Downloads===')
if Printok=='false':
 print("{} wasn't exists".format(Filename))
else:
 if NeedImage!="n":
  if r.status_code == 200:
   print('Image sucessfully Downloaded:',Filename)
  else:
   print('{} couldn\'t be retreived'.format(Filename))
 else:
  print("No Download")
print('===Urls===')
print(url.split("/api")[0])
print(url)
if UC=='y':
 print(urlmore1)
 print(urlmore2)
print(Dlink)
sys.stdout.close()
