import requests, json

def get_character_list():
    r = requests.get('https://api.genshin.dev/characters')
    data = r.text
    return json.loads(data)

def get_character_img():
    d=get_character_list()
    data=[]
    for i in range(len(d)):
        data.append("https://api.genshin.dev/characters/{}/card".format(d[i]))
    return data
class Character:
  def __init__(self, name, age):
    self.name = name
    self.age = age

def get_character_info():
    return []

def get_element_img(list):
    if list!=None:
        return list
    return []