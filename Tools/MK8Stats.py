from bs4 import BeautifulSoup
import numpy as np
import pandas as pd
import requests

shortnames = ["WG", "AC", "ON", "OF", "MT", "SL", "SW", "SA", "SG", "TL", "TW", "TA", "TG"]
longnames = ["Weight", "Acceleration", "On-Road traction", "(Off-Road) Traction", "Mini-Turbo", "Ground Speed",
             "Water Speed", "Anti-Gravity Speed", "Air Speed", "Ground Handling", "Water Handling",
             "Anti-Gravity Handling", "Air Handling"]

wikiurl = "https://www.mariowiki.com/Mario_Kart_8_in-game_statistics"

wikihtml = requests.get(wikiurl).text
wikisoup = BeautifulSoup(wikihtml)
# print(wikisoup.prettify())

# This feels like cheating, but...
wikitables = pd.read_html(wikisoup.prettify())
print(len(wikitables))
# print(*[table.head(3) for table in wikitables], sep="\n")
# print(wikitables[0].shape, wikitables[1].shape)
datatables = wikitables[1:5]
for i, table in enumerate(datatables):
    datatables[i] = pd.DataFrame().assign(**{longnames[shortnames.index(table.iloc[1, col])]: table.iloc[2:, col]
                                             for col in table.columns[1:]})
    datatables[i].index = table.iloc[2:, 0]

print("Example Bests Per Category",
      *zip(datatables[0].columns, *[table.index[np.nanargmax(np.float32(table), axis=0)] for table in datatables]),
      sep="\n")
