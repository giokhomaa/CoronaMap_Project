# 1 sacdeli
#import folium  # folium ფუნქციას გამოაქვს რუკები და ადგილმდებარეობები

# # გამოაქვს ლოკაცია, ზუმის დონე, და რუკის ტიპი
# map = folium.Map(location = [41.69, 81.09], zoom_level = 50, tiles = "Stamen Terrain")
#
# fg = folium.FeatureGroup(name = "MY Markers")
#
# for item in [[41.89, 81.19], [41.59, 81.29], [41.80, 81.30]]:
#     fg.add_child(folium.Marker(location = item, popup="Test Marker"))
#
#
# #map.add_child(folium.Marker([41.89, 81.19], popup = "Test Marker"))  # გამოიყენება პინის დასასმელად (სათითაოდ) და პინზე ინფორმაციის დასატანად
#
# #fg.add_child(folium.Marker([41.89, 81.19], popup = "Test Marker"))  # გამოაქვს პინები ჯგუფურად
#
# map.add_child(fg)
#
# map.save("CoronaMap.html")




# 2 project
import folium # სხვადასხვა ტიპის რუკის წამოღება
import requests  # ინფორმაციის წამოღება
from bs4 import BeautifulSoup
import pandas  # ტექსტური ფაილიდან ინფორმაციის გარჩევა და დამუშავება

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

c = r.content  # c-ს მოაქვს მთელი ინფორმაცია საიტიდან (html, css, javascript და ა.შ.)

soup = BeautifulSoup(c, "html.parser")  # BeautifulSoup ფუნქციით ჩვენ ვპარსავთ c-ს და მოგვაქვს მარტო html კოდი (ამ შემთხვევაში მოდის მთლიანი საიტის html კოდი)
# მთლიანი საიტის html კოდი კიდევ გასაპარსია, რადგან წამოიღოს კონკრეტული ინფორმაცია
#print(soup)
data = soup.find("tbody")  # დაინფიცირებულთ ცხრილი html კოდში იწყება <tbody> ხაზით, ჩვენ კი მოვაძებნინებთ ამ <tbody>-ს
#print(data)  # გამოაქვს მხოლოდ ცხრილის html კოდი

# მაგრამ ჩვენ ვეძებთ მხოლოდ ქვეყნებში ინფიცირებულთ რაოდენობას, ამიტომ data კიდევ გასაპარსია

# find_all() ფუნქციით ვფილტრავთ <tr style role - ით და მოგვაქვს მხოლოდ ქვეყნების ინფორმაცია კოვიდთან დაკავშირებით
rows = data.find_all("tr", {"style role":""}) # მოაქვს სია
#print(rows[0])  # გამოაქვს მხოლოდ პირველი სტრიქონის ინფორმაცია ანუ usa-ს ინფორმაცია

d = {}

for item in rows:
# tr -ში მოძებნოს td(td-ში მოთავსებულია ინფიცირებულთა რაოდენობა) და გამოიტანოს, [2] რაოდენობა არის მესამე row ამიტომ ვწერთ [2]-ს
    tcases = item.find_all("td")[2].txt  #.text-ის საშუალებით მოაქვს მხოლოდ რიცხვები, მის გარეშ წამოიღებს მთლიან კოდს

# d ლექსიკონში key არის ქვეყნის სახელი ხოლო value არის tcases ანუ რაოდენობა.
# replace ფუნქციით ვეძებთ ციფრებში მძიმეებს და ვანაცვლებთ სიცარიელით ანუ: 74,633 ==> 74633
    d[item.find_all("td")[1].text] = int(tcases.replace(",", ""))

#print(d)

# pandas ფუნქცია კითხულობს ფაილებს და არჩვს მათ, მძიმეების გამოყოფილ ინფორმაციას ყოფს
# აუცილებელია იყოს csv გაფართოების ფაილი
cdata = pandas.read_csv("countries.csv")

lat = list(cdata["latitude"])
lon = list(cdata["longitude"])
cname = list(cdata["name"])


map = folium.Map(location = [41.69, 81.09], zoom_start = 3, tiles = "Stamen Terrain")

fg = folium.FeatureGroup(name = "Countries")

# lt, ln, cn ცვლადები დაივლიან lat, lon, cname ცვლადებში
for lt, ln, cn in zip(lat, lon, cname):

    if cn in d.keys():  # თუ ქვეყნის დასახელები არის ლექსიკონის key-ში
         fg.add_child(folium.CircleMarker(location = [lt, ln], popup=str(cn) + "\n" + str(d[cn]),
            radius = radius_gen(d[cn]), fill_color = color_gen(d[cn]), color = "green", fill_opacity = 0.7))


map.add_child(fg)

map.save("CoronaMap.html")










