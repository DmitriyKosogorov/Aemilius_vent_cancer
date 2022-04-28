import requests

API_key='7bc74e67ab92d8b035ce120f678a5799'

s_city=input()
#s_city='Irkutsk'
shown=False
answer=requests.get("http://api.openweathermap.org/data/2.5/find",params={'q': s_city, 'type': 'like', 'units': 'metric', 'APPID': API_key})
if(str(answer)=='<Response [200]>'):
    data=answer.json()
    print(data)
    #print(data['list'[0])
    for i in range(len(data['list'])):
        if(data['list'][i]['name']==s_city):
            print('temperature = ',data['list'][i]['main']['temp'])
            print('feels like = ',data['list'][i]['main']['feels_like'])
            print('pressure = ',data['list'][i]['main']['pressure'])
            print('weather = ',data['list'][i]['weather'][0]['description'])
            break
else:
    print('connection error')
