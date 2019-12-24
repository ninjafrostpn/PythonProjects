from bs4 import BeautifulSoup
import numpy as np
import pandas as pd
import requests
from scipy.stats import rankdata

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
# print(len(wikitables))
# print(*[table.head(3) for table in wikitables], sep="\n")
# print(wikitables[0].shape, wikitables[1].shape)
datatables = wikitables[1:5]
for i, table in enumerate(datatables):
    # Set the unabbreviated names as column names and line up the data with the correct rows
    datatables[i] = pd.DataFrame().assign(**{longnames[shortnames.index(table.iloc[1, col])]: table.iloc[2:, col]
                                             for col in table.columns[1:]})
    # Set the item types as the indices
    datatables[i].index = table.iloc[2:, 0]
    # Remove the NaNs
    datatables[i] = datatables[i].loc[~np.any(np.isnan(np.float16(datatables[i])), axis=1)]

print("Example Bests Per Category:",
      *zip(datatables[0].columns, *[table.index[np.nanargmax(np.float32(table), axis=0)] for table in datatables]),
      sep="\n")

choiceranks = [[rankdata(table[col], "dense") for col in table.columns] for table in datatables]
# print(*choiceranks, sep="\n")
choicescores = [np.sum(ranks, axis=0) for ranks in choiceranks]
# print(*choicescores, sep="\n")
choicefinalranks = [rankdata(scores, "dense") for scores in choicescores]
# print(*choicefinalranks, sep="\n")
print("\nExample Bests All-Rounders:", *[datatables[i].index[np.argmin(ranks)]
                                         for i, ranks in enumerate(choicefinalranks)],
      sep="\n")
