import requests
from bs4 import BeautifulSoup

headers = {
    "Referer": "https://umd.libcal.com/spaces?lid=2552&gid=23067&c=0"
}

bookId = 'cs_NMLKV1cV'
payload = {
    "id": bookId
}

baseUrl = 'https://umd.libcal.com/equipment/cancel'
html = requests.get(baseUrl, params=payload)
soup = BeautifulSoup(html.text, 'html.parser')

all_tr = soup.find_all("tr")
secret = ""
for tr in all_tr:
    id = tr.get('id')
    if id and id[:7] == "booking":
        secret=id[8:]

print(secret)