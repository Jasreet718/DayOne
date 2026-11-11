"""Put the WaPo Dallas homicides on a map, colored by whether anyone was arrested."""

import pandas as pd                   # pandas reads the CSV into a table
import folium                         # folium builds the map as an html file

w = pd.read_csv("data/wapo_dallas.csv")        # 1,567 Dallas cases, 2007 to 2017

# A row with no lat or lon cannot be drawn, so drop it and say how many went.
before = len(w)
w = w.dropna(subset=["lat", "lon"])
print(f"dropped {before - len(w)} rows with no coordinates")

# location is the middle of Dallas. zoom_start 11 fits the whole city.
m = folium.Map(location=[32.78, -96.80], zoom_start=11, tiles="cartodbpositron")

for _, row in w.iterrows():           # one turn per case
    # orange if nobody was ever arrested, green if the case closed
    color = "orange" if row.disposition == "Open/No arrest" else "green"
    folium.CircleMarker(
        location=[row.lat, row.lon],  # where to put the dot
        radius=3, color=color, fill=True, fill_opacity=0.6, weight=1,
    ).add_to(m)                       # stick this dot on the map

# A map with no key is not evidence, so the legend says what the colors mean.
legend = """
<div style="position:fixed;bottom:30px;left:30px;background:white;padding:8px 12px;
border:1px solid #999;font-family:sans-serif;font-size:13px;z-index:9999">
<b>Dallas homicides 2007&ndash;2017</b><br>
<span style="color:orange">&#9679;</span> Open / no arrest (676)<br>
<span style="color:green">&#9679;</span> Closed (891)<br>
Source: Washington Post Unsolved Homicide Database
</div>"""
m.get_root().html.add_child(folium.Element(legend))

m.save("reports/dallas_map.html")     # save it, same as the chart. it opens in any browser.
print(f"wrote reports/dallas_map.html with {len(w)} markers")
