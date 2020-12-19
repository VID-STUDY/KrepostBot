import requests

longWay = requests.get('https://api.routing.yandex.net/v2/route?waypoints=41.31463053204946, 69.24791482238928|41.32230476770413,69.30297459579195&apikey=424e9981-9ff1-44c3-ba6e-60c7669b25f3')
print(longWay.json())