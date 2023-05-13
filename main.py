from bs4 import BeautifulSoup
from urllib.request import urlopen
import ssl
import csv
import pandas as pd
import sqlite3

# Ignore SSL certificate errors
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

url = "https://www.billboard.com/charts/hot-100/"
html = urlopen(url, context=ctx).read()
soup = BeautifulSoup(html, "html.parser")
tags = soup.find_all("div", {"class": "o-chart-results-list-row-container"})

songs = [tag.find("h3", {"class": "c-title"}) for tag in tags]
song_names = [song.text.strip() for song in songs]

artists = [tag.select("span.c-label.a-no-trucate.a-font-primary-s")[0].text.strip() for tag in tags]

list_items = []
item = ()
for i in range(100):
    item = (i + 1, artists[i], song_names[i])
    list_items.append(item)
print(list_items)

with open("top_100.csv", "w", newline="") as file:
    writer = csv.writer(file)
    writer.writerow(["Ranking", "Artist", "Song"])
    for row in list_items:
        writer.writerow(row)

df = pd.read_csv("top_100.csv")
pd.set_option("display.max_columns", None)
#print(df)
filtered_df = df.loc[(df["Ranking"] <= 10)]
filter_df = df.loc[(df["Artist"] == "Morgan Wallen")]
filtered_df.to_csv('top_10.csv', index=False)

con = sqlite3.connect("billboard.db")
df.to_sql('top_100', con, if_exists='replace', index=False)
con.close()
