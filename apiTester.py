import requests

key = '' // Api key
uuid = 'NoseThe'

f = requests.get('https://api.hypixel.net/player?key='+key+'&name='+uuid).json()
print(list(f['player']['mostRecentGameType']))
