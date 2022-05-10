from flask import Flask, render_template, redirect, request, make_response, jsonify
import requests
from random import choice as ch

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'

CITIES = ['Москва', 'Санкт-Петербург', 'Вашингтон', 'Краснодар', 'Стамбул', 'Хабаровск', 'Берлин', 'Стокгольм',
          'Хельсинки', 'Осло', 'Амстердам', 'Химки', 'Анталия']
# response = requests.get(api_server)
city = ch(CITIES)
right = None

@app.route('/', methods=['POST', 'GET'])
@app.route('/index', methods=['POST', 'GET'])
def index():
    global right, city
    if request.method == 'GET':
        geocoder_request = f"http://geocode-maps.yandex.ru/1.x/?apikey=40d1649f-0493-4b70-98ba-98533de7710b&geocode=" \
                           f"{city}&format=json"
        response = requests.get(geocoder_request)
        if response:
            json_response = response.json()
            toponym = json_response["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]
            lat, long = toponym["Point"]["pos"].split()
        else:
            print("Ошибка выполнения запроса:")
            print(geocoder_request)
            print("Http статус:", response.status_code, "(", response.reason, ")")
        img1 = f"http://static-maps.yandex.ru/1.x/?ll={lat},{long}&spn=0.02,0.00619&l=sat,skl"
        img2 = f"http://static-maps.yandex.ru/1.x/?ll={lat},{long}&spn=0.016457,0.049&l=sat"
        img3 = f"http://static-maps.yandex.ru/1.x/?ll={lat},{long}&spn=0.016457,0.00619&l=map"
        return render_template('index.html', img1=img1, img2=img2, img3=img3, cities=CITIES, r=right)
    else:
        if request.form['class'] == city:
            right = True
            city = ch(CITIES)
        else:
            right = False
        return redirect('/')



def main():
    app.run()


if __name__ == '__main__':
    main()
