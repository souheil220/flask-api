import requests
import base64


def test():
    data = {"ad_2000":"hadjhabib_s","password":"Machen220-714"
            
                    }
    res = requests.post('http://localhost:5000/api/AD/ad_2000', json=data)
    if res.ok:
        ad_2000 = res.json()['message']["ad_2000"]
        mail = res.json()['message']["mail"]
        name = res.json()['message']["name"]
        thumbnailPhoto = base64.b64decode(res.json()['message']["thumbnailPhoto"])
        with open(f"{ad_2000}.png", "wb") as fh:
                    fh.write(thumbnailPhoto)

if __name__ == '__main__':
    
    print(test())