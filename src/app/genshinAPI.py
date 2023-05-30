import requests
def get_character_list():
    with urllib.request.urlopen('https://api.genshin.dev/characters/') as r:
        text = r.read()
        dict = json.loads(text)
    return dict

print(get_character_list())