import requests
import json

appid = 'bbcf00e8fd39b3bfdedace784dd36893'
service = 'https://samples.openweathermap.org/data/2.5/weather'
req = requests.get(f'{service}?q=London,uk&appid={appid}')
data = json.loads(req.text)
print(f"В городе {data['name']} {data['main']['temp']} градусов по Кельвину")

# https://samples.openweathermap.org/data/2.5/weather?q=London,uk&appid=bbcf00e8fd39b3bfdedace784dd36893

