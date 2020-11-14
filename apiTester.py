import requests

key = 'fc6c5639-7f38-481f-af0c-f86453fda58a'
uuid = 'NoseThe'

f = requests.get('https://api.hypixel.net/player?key='+key+'&name='+uuid).json()
print(list(f['player']['mostRecentGameType']))
