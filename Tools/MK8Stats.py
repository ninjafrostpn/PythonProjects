from bs4 import BeautifulSoup
import pandas as pd
import requests

wikiurl = "https://www.mariowiki.com/Mario_Kart_8_in-game_statistics"

wikihtml = requests.get(wikiurl).text
wikisoup = BeautifulSoup(wikihtml)
print(wikisoup.prettify())

# This feels like cheating, but...
wikitables = pd.read_html(wikihtml)
print(len(wikitables))
print(*[table.head(2) for table in wikitables], sep="\n")
