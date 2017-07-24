import vk_api
import datetime
import time
import requests
from settings import token, weather_key

vk = vk_api.VkApi(token=token)
vk.auth()

values = {'out': 0, 'count': 100, 'time_offset': 60}
response = vk.method('messages.get', values)
k = ['привет', 'прив', 'дратуйти', 'hi', 'hello', 'превед']
hello = ['да', 'ды', 'ок', 'давай', 'помоги', 'можешь']
no  = ['нет', 'неа', 'не', 'no']

def write_msg(user_id, s):
    vk.method('messages.send', {'user_id': user_id, 'message': s})


while True:
    response = vk.method('messages.get', values)
    if response['items']:
        values['last_message_id'] = response['items'][0]['id']
    for item in response['items']:
        if response['items'][0]['body'].lower() in k:
            write_msg(item['user_id'], 'Привет! Я, могу тебе помочь узнать погоду за окном?')
        elif response['items'][0]['body'].lower() in hello:
            write_msg(item['user_id'], 'Введи название города.')
        elif response['items'][0]['body'].lower() in no:
            write_msg(item['user_id'], 'Как надумаешь, обращайся.')
        elif response['items'][0]['body']:
            city = response['items'][0]['body']

            response = requests.get('http://api.openweathermap.org/data/2.5/forecast/daily?q='
                                    + city
                                    + '&units=metric'
                                    + '&cnt='
                                    + str(7)
                                    + '&appid=' + weather_key)
            j = response.json()

            try:
                n = 0
                while n < 7:
                    udate = j["list"][n]["dt"]
                    date = datetime.datetime.fromtimestamp(int(udate)).strftime('%d-%m-%Y')
                    temp_min = j['list'][n]['temp']['min']
                    temp_max = j['list'][n]['temp']['max']
                    temp_night = j['list'][n]['temp']['night']
                    temp_day = j['list'][n]['temp']['day']
                    weather = j['list'][n]['weather'][0]['main']
                    n += 1
                    write_msg(item['user_id'], date + '\n' + ' min t = ' + str(temp_min) + '°C,'
                              + ' max t = ' + str(temp_max) + '°C\n'
                              + ' ночью t = ' + str(temp_night) + '°C,' + ' днем t = ' + str(temp_day) + '°C\n'
                              + weather
                              + '\n\n')
                write_msg(item['user_id'], 'Я могу еще чем-то помочь?')
            except:
                write_msg(item['user_id'], 'Я тебя не понял.')

    time.sleep(1)



