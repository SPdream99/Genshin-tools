import requests, json, os
import wikiaAPI
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
        return Character(name,o["name"],get_character_image(o["name"],"Full_Wish","Card"),o["title"] if("title" in o) else "No title",o["vision"],o["weapon"],o["nation"],o["affiliation"],o["rarity"],o["constellation"],get_character_image(o["constellation"],""),o["skillTalents"],o["passiveTalents"],o["constellations"],o["img_list"])
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
        try:
            r = requests.get('{}/characters/{}/en.json'.format(link,data[i]))
            if(r.text!="404: Not Found"):
                o=json.loads(r.text)
                o.update({'img_list':get_skill_image(o),'link':'{}/characters/{}/en.json'.format(link,data[i]),'f_img':get_character_image(o["name"],"Full_Wish","Card"),'img':get_character_image(o["name"],"Card","Full_Wish"),'c_img':get_character_image(o["constellation"],"")})
                lo.update({data[i]:o})
            else:
                r = requests.get('{}/characters/{}/{}.json'.format(link,data[i],data[i]))
                if(r.text!="404: Not Found"):
                    o=json.loads(r.text)
                    o.update({'img_list':get_skill_image(o),'link':'{}/characters/{}/{}.json'.format(link,data[i],data[i]),'f_img':get_character_image(o["name"],"Full_Wish","Card"),'img':get_character_image(o["name"],"Card","Full_Wish"),'c_img':get_character_image(o["constellation"],"")})
                    lo.update({data[i]:o})
                else:
                    if("-" in data[i]):
                        r = requests.get('{}/characters/{}/en.json'.format(link,data[i].split("-")[1]))
                        if(r.text!="404: Not Found"):
                            o=json.loads(r.text)
                            o.update({'img_list':get_skill_image(o),'link':'{}/characters/{}/en.json'.format(link,data[i].split("-")[1]),'f_img':get_character_image(o["name"],"Full_Wish","Card"),'img':get_character_image(o["name"],"Card","Full_Wish"),'c_img':get_character_image(o["constellation"],"")})
                            lo.update({data[i]:o})
                        else:
                            if("-" in data[i]):
                                r = requests.get('{}/characters/{}/{}.json'.format(link,data[i].split("-")[1],data[i].split("-")[1]))
                                if(r.text!="404: Not Found"):
                                    o=json.loads(r.text)
                                    o.update({'img_list':get_skill_image(o),'link':'{}/characters/{}/{}.json'.format(link,data[i].split("-")[1],data[i].split("-")[1]),'f_img':get_character_image(o["name"],"Full_Wish","Card"),'img':get_character_image(o["name"],"Card","Full_Wish"),'c_img':get_character_image(o["constellation"],"")})
                                    lo.update({data[i]:o})
                                else:
                                    if("-" in data[i]):
                                        r = requests.get('{}/characters/{}/en.json'.format(link,data[i].split("-")[0]))
                                        if(r.text!="404: Not Found"):
                                            o=json.loads(r.text)
                                            o.update({'img_list':get_skill_image(o),'link':'{}/characters/{}/en.json'.format(link,data[i].split("-")[0]),'f_img':get_character_image(o["name"],"Full_Wish","Card"),'img':get_character_image(o["name"],"Card","Full_Wish"),'c_img':get_character_image(o["constellation"],"")})
                                            lo.update({data[i]:o})
                                    else:
                                        if("-" in data[i]):
                                            r = requests.get('{}/characters/{}/{}.json'.format(link,data[i].split("-")[1],data[i].split("-")[0]))
                                            if(r.text!="404: Not Found"):
                                                o=json.loads(r.text)
                                                o.update({'img_list':get_skill_image(o),'link':'{}/characters/{}/{}.json'.format(link,data[i].split("-")[1],data[i].split("-")[0]),'f_img':get_character_image(o["name"],"Full_Wish","Card"),'img':get_character_image(o["name"],"Card","Full_Wish"),'c_img':get_character_image(o["constellation"],"")})
                                                lo.update({data[i]:o})
        except:
            pass
    if len(o)>0:
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

class Character:
  def __init__(self,i, name, img, title, vision, weapon, nation, aff, rarity, constellation,constellation_img,skillTalents,passiveTalents,constellations,img_list):
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
    talent=[f"Talent_{(x['name'].replace(' ','_'))}.png" for x in char["skillTalents"]]
    talent[0]=f"{char['weapon_type'].capitalize()}_{char['vision_key'].capitalize()}.png"
    # talent=[f"""{''.join([y for y in x if y in string.ascii_letters + '_'+"'"+"-"+"!"])}.png""" for x in talent]
    # change(replace,talent)

    p_talent=[f"Talent_{(x['name'].replace(' ','_'))}.png" for x in char["passiveTalents"]]
    # p_talent=[f"""{''.join([y for y in x if y in string.ascii_letters + '_'+"'"+"-"+"!"])}.png""" for x in p_talent]
    # change(replace,p_talent)

    c=[f"Constellation_{(x['name'].replace(' ','_'))}.png" for x in char["constellations"]]
    # c=[f"""{''.join([y for y in x if y in string.ascii_letters + '_'+"'"+"-"+"!"])}.png""" for x in c]
    c=change(replace,c)
    print(talent[0])
    return {
        "weapon": wikiaAPI.get_image("gensin-impact",f"Icon_{(char['weapon_type']).capitalize()}.png"),
        "skillTalents":[wikiaAPI.get_image("gensin-impact",x) for x in talent],
        "passiveTalents":[wikiaAPI.get_image("gensin-impact",x) for x in p_talent],
        "constellations":[wikiaAPI.get_image("gensin-impact",x) for x in c],
        }
# print(get_skill_image(get_character("klee")))
# update_list()
