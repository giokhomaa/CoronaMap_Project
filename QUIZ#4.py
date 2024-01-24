import folium
import requests
from bs4 import BeautifulSoup
import pandas

def radius_gen(tcases):
    return tcases ** 0.2

def color_gen(tcases):
    if tcases < 50000:
        return "blue"
    elif tcases < 100000:
        return "green"
    elif tcases < 300000:
        return "purple"
    elif tcases < 600000:
        return "pink"
    elif tcases < 9000000:
        return "yellow"
    else:
        return "red"

r = requests.get("https://www.worldometers.info/coronavirus/")

c = r.content

soup = BeautifulSoup(c, "html.parser")

#print(soup)
data = soup.find("tbody")

rows = data.find_all("tr", {"style role":""})


d = {}

for item in rows:
    tcases = item.find_all("td")[2].txt

    d[item.find_all("td")[1].text] = int(tcases.replace(",", ""))

cdata = pandas.read_csv("countries.csv")

lat = list(cdata["latitude"])
lon = list(cdata["longitude"])
cname = list(cdata["name"])


map = folium.Map(location = [41.69, 81.09], zoom_start = 3, tiles = "Stamen Terrain")

fg = folium.FeatureGroup(name = "Countries")

for lt, ln, cn in zip(lat, lon, cname):

    if cn in d.keys():
         fg.add_child(folium.CircleMarker(location = [lt, ln], popup=str(cn) + "\n" + str(d[cn]),
            radius = radius_gen(d[cn]), fill_color = color_gen(d[cn]), color = "green", fill_opacity = 0.7))


map.add_child(fg)

map.save("CoronaMap.html")