import os
import requests
from bs4 import BeautifulSoup
import json

from dotenv import load_dotenv
load_dotenv()

USERNAME = os.getenv("UEK_LOGIN")
PASSWORD = os.getenv("UEK_PASSWORD")

if not USERNAME or not PASSWORD:
    raise RuntimeError("UEK_LOGIN or UEK_PASSWORD not set")

# Create authenticated session
session = requests.Session()
session.auth = (USERNAME, PASSWORD)

# Base URL
url = "https://planzajec.uek.krakow.pl/"
response = session.get(url)
response.raise_for_status()
response.encoding = "utf-8"

soup = BeautifulSoup(response.text, "html.parser")

group_div = soup.find_all("div", {"class": "kategorie"})[1]

group_folder = {}

for group in group_div.find_all("a"):
    group_name_param = group["href"].split("=")[-1]
    group_url = f"https://planzajec.uek.krakow.pl/index.php?typ=G&grupa={group_name_param}"

    response = session.get(group_url)
    response.raise_for_status()
    response.encoding = "utf-8"

    group_soup = BeautifulSoup(response.text, "html.parser")

    group_name = group_soup.find_all("div", {"class": "grupa"})[0].text
    group_folder[group_name] = []

    for group_col in group_soup.find_all("div", {"class": "kolumny"}):
        for group_row in group_col.find_all("a"):
            group_id = group_row["href"].split("=")[-2].split("&")[0]
            group_sub_name = group_row.text
            group_folder[group_name].append((group_sub_name, group_id))

with open("group_folder.json", "w", encoding="utf-8") as json_file:
    json.dump(group_folder, json_file, ensure_ascii=False, indent=4)

print("Data saved to group_folder.json")
