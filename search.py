import sys
from io import BytesIO
import requests
from PIL import Image
from map_scale import calculate_spn

def main():
    if len(sys.argv) < 2:
        print("Usage: python search.py <address>")
        return
    
    toponym_to_find = " ".join(sys.argv[1:])
    
    geocoder_api_server = "http://geocode-maps.yandex.ru/1.x/"
    geocoder_params = {
        "apikey": "8013b162-6b42-4997-9691-77b7074026e0",
        "geocode": toponym_to_find,
        "format": "json"
    }

    response = requests.get(geocoder_api_server, params=geocoder_params)
    
    if not response:
        print("Ошибка выполнения запроса к геокодеру:")
        print(response.url)
        print(f"HTTP статус: {response.status_code} ({response.reason})")
        return
    
    try:
        json_response = response.json()
        toponym = json_response["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]
    except (KeyError, IndexError):
        print("Не удалось найти указанный адрес")
        return
    
    toponym_coordinates = toponym["Point"]["pos"]
    toponym_longitude, toponym_latitude = toponym_coordinates.split(" ")
    
    spn = calculate_spn(toponym)
    
    map_params = {
        "ll": f"{toponym_longitude},{toponym_latitude}",
        "spn": spn,
        "l": "map",
        "pt": f"{toponym_longitude},{toponym_latitude},pm2dgl"  # Добавляем метку
    }
    
    # Запрос к StaticAPI
    map_api_server = "https://static-maps.yandex.ru/1.x"
    response = requests.get(map_api_server, params=map_params)
    
    if not response:
        print("Ошибка выполнения запроса к StaticAPI:")
        print(response.url)
        print(f"HTTP статус: {response.status_code} ({response.reason})")
        return
    
    try:
        im = BytesIO(response.content)
        opened_image = Image.open(im)
        opened_image.show()
    except Exception as e:
        print("Ошибка при отображении карты:", e)

if __name__ == "__main__":
    main()
