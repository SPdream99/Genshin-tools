import requests, json, hashlib
def get_data(fandom, language,category):
    url = ("https://{}.fandom.com/{}/api/v1/Articles/List?expand=1&category={}&limit=10000".format(fandom,language,category))
    r = requests.get(url)
    response = r.json()
    return response["items"]

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