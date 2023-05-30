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