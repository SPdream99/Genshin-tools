import re
import requests, json, os
import wikiaAPI
from urllib.parse import unquote
from bs4 import BeautifulSoup
import string
link="https://raw.githubusercontent.com/genshindev/api/mistress/assets/data"
def get_character_list():
    l=[]
    ban=['traveler','lumine','aether','crossover characters', 'event-exclusive characters', 'non-wish characters', 'playable characters by region', 'standard wish characters','traveler (unaligned)']
    data=wikiaAPI.get_data("genshin-impact","en","Playable_Characters")
    for i in range(len(data)):
        if(data[i]["title"].lower() not in ban):
            o=data[i]["title"].lower()
            o=o.replace(" ","-").replace("(","").replace(")","")
            l.append(o)
    return l

def get_character_alt_list():
    l={}
    ban=['traveler','lumine','aether','crossover characters', 'event-exclusive characters', 'non-wish characters', 'playable characters by region', 'standard wish characters','traveler (unaligned)']
    data=wikiaAPI.get_data("genshin-impact","en","Playable_Characters")
    for i in range(len(data)):
        if(data[i]["title"].lower() not in ban):
            o=data[i]["title"].lower()
            o=o.replace(" ","-").replace("(","").replace(")","")
            l.update({o:data[i]["url"].split("wiki/")[1]})
    return l

def get_character(name=None):
    if name!=None:
        lo={}
        try:
            if(os.stat("./static/assets/character_list.json").st_size > 0):
                f=open("./static/assets/character_list.json","r")
                lo=json.load(f)
                f.close()
            else:
                lo=update_list()
        except:
            lo=update_list()
        # r = requests.get(lo[name]["link"])
        # o = json.loads(r.text)
        o = lo[name]
        return Character(name,o["name"],get_character_image(o["name"],"Full_Wish","Card"),o["title"] if("title" in o) else "No title",o["vision"],o["weapon"],o["nation"],o["affiliation"],o["rarity"],o["constellation"],get_character_image(o["constellation"],""),o["skillTalents"],o["passiveTalents"],o["constellations"],o["img_list"],o["mats"])
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

def get_asc_tl(c):
    asc=wikiaAPI.get_table("genshin-impact", c, "wikitable ascension-stats")
    asc_l=[]
    asc_o={}
    for i in range(1,7):
        asc_o[i]={}
    tl=wikiaAPI.get_table("genshin-impact", c, "wikitable talent-table", True, 9)
    if not "Talent" in str(tl[0]):
        tl=wikiaAPI.get_table("genshin-impact", c, "wikitable talent-table", True, 8)
        if not "Talent" in str(tl[0]):
            tl = wikiaAPI.get_table("genshin-impact", c, "wikitable talent-table", True, 7)
            if not "Talent" in str(tl[0]):
                tl = wikiaAPI.get_table("genshin-impact", c, "wikitable talent-table", True, 6)
                if not "Talent" in str(tl[0]):
                    tl = wikiaAPI.get_table("genshin-impact", c, "wikitable talent-table", True, 10)
                    if not "Talent" in str(tl[0]):
                        tl = wikiaAPI.get_table("genshin-impact", c, "wikitable talent-table", True, 11)
    tl_o = {}
    for i in range(2,11):
        tl_o[i]={}
    for i in asc:
        if i.has_attr('class'):
            if str(i['class'])=="['ascension', 'mw-collapsible']":
                asc_l.append(i)
    for i in range(len(asc_l)):
        name_l=asc_l[i].find_all("a")
        quantity_l=asc_l[i].find_all("span",{"class":"card-text card-font"})
        for p in range(len(name_l)):
            asc_o[i+1].update({unquote(name_l[p]['href'].split("wiki/")[1].lower()):quantity_l[p].text})
    tl_l = [tl[i] for i in range(len(tl)) if i!=0]
    for i in range(len(tl_l)):
        name_l=tl_l[i].find_all("a")
        r=[]
        for cs in name_l:
            if not cs.parent.has_attr('class'):
                r.append(cs)
        name_l=r
        quantity_l=tl_l[i].find_all("span",{"class":"card-text card-font"})
        for p in range(len(name_l)):
            tl_o[i+2].update({unquote(name_l[p]['href'].split("wiki/")[1].lower()):quantity_l[p].text})
    p={}
    p.update({"asc" : asc_o})
    p.update({"tl": tl_o})
    return p

def update_list():
    alt_data=get_character_alt_list()
    data = get_character_list()
    lo={}
    for i in range(len(data)):
            o={}
            r = requests.get('{}/characters/{}/en.json'.format(link,data[i]))
            no=alt_data[data[i]]
            if "traveler" in no.lower():
                no="Traveler"
            if(r.text!="404: Not Found"):
                o=json.loads(r.text)
                o.update({'img_list':get_skill_image(o),'link':'{}/characters/{}/en.json'.format(link,data[i]),'f_img':get_character_image(o["name"],"Full_Wish","Card"),'img':get_character_image(o["name"],"Card","Full_Wish"),'c_img':get_character_image(o["constellation"],"")})
                o.update({"mats":get_asc_tl(no)})
                lo.update({data[i]:o})
            else:
                r = requests.get('{}/characters/{}/{}.json'.format(link,data[i],data[i]))
                if(r.text!="404: Not Found"):
                    o=json.loads(r.text)
                    o.update({'img_list':get_skill_image(o),'link':'{}/characters/{}/{}.json'.format(link,data[i],data[i]),'f_img':get_character_image(o["name"],"Full_Wish","Card"),'img':get_character_image(o["name"],"Card","Full_Wish"),'c_img':get_character_image(o["constellation"],"")})
                    o.update({"mats":get_asc_tl(alt_data[data[i]])})
                    lo.update({data[i]:o})
                else:
                    if("-" in data[i]):
                        r = requests.get('{}/characters/{}/en.json'.format(link,data[i].split("-")[1]))
                        if(r.text!="404: Not Found"):
                            o=json.loads(r.text)
                            o.update({'img_list':get_skill_image(o),'link':'{}/characters/{}/en.json'.format(link,data[i].split("-")[1]),'f_img':get_character_image(o["name"],"Full_Wish","Card"),'img':get_character_image(o["name"],"Card","Full_Wish"),'c_img':get_character_image(o["constellation"],"")})
                            o.update({"mats":get_asc_tl(alt_data[data[i]])})
                            lo.update({data[i]:o})
                        else:
                            if("-" in data[i]):
                                r = requests.get('{}/characters/{}/{}.json'.format(link,data[i].split("-")[1],data[i].split("-")[1]))
                                if(r.text!="404: Not Found"):
                                    o=json.loads(r.text)
                                    o.update({'img_list':get_skill_image(o),'link':'{}/characters/{}/{}.json'.format(link,data[i].split("-")[1],data[i].split("-")[1]),'f_img':get_character_image(o["name"],"Full_Wish","Card"),'img':get_character_image(o["name"],"Card","Full_Wish"),'c_img':get_character_image(o["constellation"],"")})
                                    o.update({"mats":get_asc_tl(alt_data[data[i]])})
                                    lo.update({data[i]:o})
                                else:
                                    if("-" in data[i]):
                                        r = requests.get('{}/characters/{}/en.json'.format(link,data[i].split("-")[0]))
                                        if(r.text!="404: Not Found"):
                                            o=json.loads(r.text)
                                            o.update({'img_list':get_skill_image(o),'link':'{}/characters/{}/en.json'.format(link,data[i].split("-")[0]),'f_img':get_character_image(o["name"],"Full_Wish","Card"),'img':get_character_image(o["name"],"Card","Full_Wish"),'c_img':get_character_image(o["constellation"],"")})
                                            o.update({"mats":get_asc_tl(alt_data[data[i]])})
                                            lo.update({data[i]:o})
                                    else:
                                        if("-" in data[i]):
                                            r = requests.get('{}/characters/{}/{}.json'.format(link,data[i].split("-")[1],data[i].split("-")[0]))
                                            if(r.text!="404: Not Found"):
                                                o=json.loads(r.text)
                                                o.update({'img_list':get_skill_image(o),'link':'{}/characters/{}/{}.json'.format(link,data[i].split("-")[1],data[i].split("-")[0]),'f_img':get_character_image(o["name"],"Full_Wish","Card"),'img':get_character_image(o["name"],"Card","Full_Wish"),'c_img':get_character_image(o["constellation"],"")})
                                                o.update({"mats":get_asc_tl(alt_data[data[i]])})
                                                lo.update({data[i]:o})

    if len(lo)>0:
        f = open("./static/assets/character_list.json", "w")
        json.dump(lo, f)
        f.close()
    else:
        print("None")
    return lo

def get_character_image(name,need,alt="Noway"):
    data=wikiaAPI.get_image("gensin-impact",(f"{'Character_' if ('Full_Wish' in need) else ''}{name.replace(' ','_')}{'_' if (need!='') else ''}{need}.png"))
    if data!=False:
        return data
    else:
        data=wikiaAPI.get_image("gensin-impact",(f"{'Character_' if ('Full_Wish' in alt) else ''}{name.replace(' ','_')}{'_' if (alt!='') else ''}{alt}.png"))
        if data!=False:
            return data
        else:
            if "Card" not in need and "Full_Wish" not in need:
                need="Constellation"
            return "/static/assets/images/no_{}.png".format(need)

def get_weapon_list():
    r = requests.get('https://api.genshin.dev/weapons')
    data = r.text
    return json.loads(data)

def get_mats_list():
    lo={}
    if(os.stat("./static/assets/material_list.json").st_size > 0):
        f=open("./static/assets/material_list.json","r")
        lo=json.load(f)
        f.close()
    else:
        lo=update_mats_list()
    return lo

def get_need_mats(l):
    o_list=get_mats_list()
    o={}
    g=[]
    for i in l:
        if i in o_list:
            o.update({i:o_list[i]})
            g.append(i)
    o.update({"meta":g})
    return o

class Character:
  def __init__(self,i, name, img, title, vision, weapon, nation, aff, rarity, constellation,constellation_img,skillTalents,passiveTalents,constellations,img_list,mats):
    self.id = i
    self.name = name
    self.img = img
    self.title = title
    self.vision = vision
    self.weapon = weapon
    self.nation = nation
    self.aff = aff
    self.rarity = rarity
    self.constellation = constellation
    self.constellation_img=constellation_img
    self.skillTalents=skillTalents
    self.passiveTalents=passiveTalents
    self.constellations=constellations
    self.img_list=img_list
    self.uplist=mats
    o=[]
    for i in self.uplist["asc"]:
        for r in self.uplist["asc"][i]:
            o.append(r)
    for i in self.uplist["tl"]:
        for r in self.uplist["tl"][i]:
            o.append(r)
    o.append("exp")
    o=list(set(o))
    self.mats=o

class Weapon:
  def __init__(self, name):
    self.name = name

def get_element_list():
    r = requests.get('https://api.genshin.dev/elements')
    data = r.text
    return json.loads(data)

def get_skill_image(char):
    def change(r,t):
        for i in range(len(r)):
            for x in range(len(t)):
                if t[x] in r[i]:
                    t[x]=r[i][1]
        return t
    replace=[["Constellation_A-Another_Round?.png","Constellation_A—Another_Round?.png"],["Constellation_Chained_Reaction.png","Constellation_Chained_Reactions.png"]]
    talent=[f"Talent_{(x['name'].replace(' ','_')).replace(':','')}.png" for x in char["skillTalents"]]
    talent[0]=f"{char['weapon_type'].capitalize()}_{char['vision_key'].capitalize()}.png"
    # talent=[f"""{''.join([y for y in x if y in string.ascii_letters + '_'+"'"+"-"+"!"])}.png""" for x in talent]
    # change(replace,talent)

    p_talent=[f"Talent_{(x['name'].replace(' ','_')).replace(':','')}.png" for x in char["passiveTalents"]]
    # p_talent=[f"""{''.join([y for y in x if y in string.ascii_letters + '_'+"'"+"-"+"!"])}.png""" for x in p_talent]
    # change(replace,p_talent)

    c=[f"Constellation_{(x['name'].replace(' ','_')).replace(':','')}.png" for x in char["constellations"]]
    # c=[f"""{''.join([y for y in x if y in string.ascii_letters + '_'+"'"+"-"+"!"])}.png""" for x in c]
    c=change(replace,c)
    return {
        "weapon": wikiaAPI.get_image("gensin-impact",f"Icon_{(char['weapon_type']).capitalize()}.png"),
        "skillTalents":[wikiaAPI.get_image("gensin-impact",x) for x in talent],
        "passiveTalents":[wikiaAPI.get_image("gensin-impact",x) for x in p_talent],
        "constellations":[wikiaAPI.get_image("gensin-impact",x) for x in c],
        }

def update_mats_list():
    def remove_tags(text):
        CLEANR = re.compile('<.*?>|&([a-z0-9]+|#[0-9]{1,6}|#x[0-9a-f]{1,6});')
        cleantext = re.sub(CLEANR, '', text)
        return cleantext
    data=wikiaAPI.get_data("genshin-impact","en","Character_Development_Items")
    ban=["Category:Character Development Items by Type","Character Development Item","Material"]
    lo={
  "exp": {
    "id": "exp",
    "name": "Character EXP",
    "desciption": "Character EXP, used to level up characters.",
    "source": [
      "Quests",
      "Character EXP Material",
      "Defeating Enemies",
      "Claiming Ley Line Blossoms from Bosses"
    ],
    "img": "exp"
  },
  "mora": {
    "id": "mora",
    "name": "Mora",
    "desciption": "Common currency. The one language everybody speaks.",
    "source": [
      "Blossoms of Wealth",
      "Quest",
      "Monsters",
      "Chests",
      "Events",
      "Ekaterina",
      "HoYoLAB Community Daily Check-In",
      "Investigation",
      "Expeditions",
      "Parametric Transformer"
    ],
    "img": "mora"
  },
  "crown-of-insight": {
    "id": "crown-of-insight",
    "name": "Crown of Insight",
    "desciption": "Once a medium for the storage and transfer of wisdom in ancient times. Now wisdom is found in ancient texts and in profound speech. Nevertheless, this Crown of Insight must still be able to impart some transcendent power and wisdom to its bearer.",
    "source": ["Events", "Offering Systems"],
    "img": "https://static.wikia.nocookie.net/gensin-impact/images/0/04/Item_Crown_of_Insight.png"
  }
}
    for i in range(len(data)):
        if not data[i]["title"] in ban and not "Category" in data[i]["title"]:
            id=data[i]["id"]
            r = wikiaAPI.get_detail("genshin-impact",data[i]["url"].split("wiki/")[1])
            if "pageprops" in r["query"]["pages"][str(id)]:
                o=json.loads(r["query"]["pages"][str(id)]["pageprops"]["infoboxes"])
                o=o[0]["data"]
                s={}
                n=(unquote(data[i]["url"].split("wiki/")[1])).replace('"',"").lower()
                s.update({"id":n})
                s.update({"name":(unquote(remove_tags([a["data"]["value"] for a in o if a['type'] == "title"][0])))})
                b=""
                for a in o:
                    if a["type"]=="group":
                        if "'label': 'Description'," in str(a):
                            b=a["data"]["value"][0]["data"]["value"][0]["data"]["value"][0]["data"]["value"]
                            break
                s.update({"desciption": unquote(remove_tags(b))})
                l = []
                for a in o:
                    if a["type"] == "group":
                        if "'label': 'How to Obtain'," in str(a):
                            b = a["data"]["value"][0]["data"]["value"][0]["data"]["value"]
                            for c in b:
                                l.append(unquote(remove_tags(c["data"]["value"])))
                            break
                s.update({"source": l})
                s.update({"img": [a["data"][0]["url"] for a in o if a['type'] == "image"][0].split("/revision")[0]})
                lo.update({n:s})
                print("ok")
    data=wikiaAPI.get_data("genshin-impact","en","Materials")
    for i in range(len(data)):
        if not data[i]["title"] in ban and not "Category" in data[i]["title"]:
            id=data[i]["id"]
            r = wikiaAPI.get_detail("genshin-impact",data[i]["url"].split("wiki/")[1])
            if "pageprops" in r["query"]["pages"][str(id)]:
                o=json.loads(r["query"]["pages"][str(id)]["pageprops"]["infoboxes"])
                o=o[0]["data"]
                s={}
                n=(unquote(data[i]["url"].split("wiki/")[1])).replace('"',"").lower()
                s.update({"id":n})
                s.update({"name":(unquote(remove_tags([a["data"]["value"] for a in o if a['type'] == "title"][0])))})
                b=""
                for a in o:
                    if a["type"]=="group":
                        if "'label': 'Description'," in str(a):
                            b=a["data"]["value"][0]["data"]["value"][0]["data"]["value"][0]["data"]["value"]
                            break
                s.update({"desciption": unquote(remove_tags(b))})
                l = []
                for a in o:
                    if a["type"] == "group":
                        if "'label': 'How to Obtain'," in str(a):
                            b = a["data"]["value"][0]["data"]["value"][0]["data"]["value"]
                            for c in b:
                                l.append(unquote(remove_tags(c["data"]["value"])))
                            break
                s.update({"source": l})
                ls=[a["data"][0]["url"] for a in o if a['type'] == "image"]
                if len(ls)>0:
                    s.update({"img": [a["data"][0]["url"] for a in o if a['type'] == "image"][0].split("/revision")[0]})
                else:
                    s.update({"img": "mora"})
                lo.update({n:s})
                print("ok")
    if len(lo)>0:
        f = open("./static/assets/material_list.json", "w")
        json.dump(lo, f)
        f.close()
    else:
        print("None")
    return lo
# print(get_skill_image(get_character("klee")))
# update_list()
# update_mats_list()