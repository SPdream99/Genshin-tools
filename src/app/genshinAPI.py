import requests, json, os

def get_character_list():
    r = requests.get('https://api.genshin.dev/characters')
    data = r.text
    return json.loads(data)

def get_character(name=None):
    if name!=None:
        r = requests.get('https://api.genshin.dev/characters/{}'.format(name))
        o=json.loads(r.text)
        return Character(o["name"],"https://api.genshin.dev/characters/{}/portrait".format(name),o["title"],o["vision"],o["weapon"],o["nation"],o["affiliation"],o["rarity"],o["constellation"])
    else:
        try:
            if(os.stat("./static/assets/character_list.json").st_size > 0):
                f=open("./static/assets/character_list.json","r")
                lo=json.load(f)
                f.close()
                return lo
            else:
                lo=update_list()
                return lo
        except:
            lo=update_list()
            return lo

def update_list():
    data = get_character_list()
    lo={}
    for i in range(len(data)):
        r = requests.get('https://api.genshin.dev/characters/{}'.format(data[i]))
        o=json.loads(r.text)
        lo.update({data[i]:o})
    f = open("./static/assets/character_list.json", "w")
    json.dump(lo, f)
    f.close()
    return lo

def get_weapon_list():
    r = requests.get('https://api.genshin.dev/weapons')
    data = r.text
    return json.loads(data)

class Character:
  def __init__(self, name, img, title, vision, weapon, nation, aff, rarity, constellation):
    self.name = name
    self.img = img
    self.title = title
    self.vision = vision
    self.weapon = weapon
    self.nation = nation
    self.aff = aff
    self.rarity = rarity
    self.constellation = constellation
class Weapon:
  def __init__(self, name):
    self.name = name

def get_element_list():
    r = requests.get('https://api.genshin.dev/elements')
    data = r.text
    return json.loads(data)

# update_list()