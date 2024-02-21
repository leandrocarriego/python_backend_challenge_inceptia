import requests


class GeoAPI:
    API_KEY = "d81015613923e3e435231f2740d5610b"
    LAT = "-35.836948753554054"
    LON = "-61.870523905384076"

    @classmethod
    def is_hot_in_pehuajo(cls) -> bool:
        hot_temp = 28.0
        unit_type = 'metric'
        url = f'https://api.openweathermap.org/data/2.5/weather?lat={cls.LAT}&lon={cls.LON}&appid={cls.API_KEY}&units={unit_type}'

        try:
            response = requests.get(url)
            response.raise_for_status()

            data = response.json()

            # Aca se verifica que sea exactamente 200 y que exista 'temp' en la respuesta
            if response.status_code == 200 and data['main']['temp']:
                current_temp = data['main']['temp']

                return current_temp > hot_temp

            else:
                print("Respuesta no esperada")
                return False

        except requests.exceptions.RequestException as e:
            print(f"Error en la solicitud HTTP: {e}")
            return False


# Ejemplo de uso
'''
api = GeoAPI()

print(api.is_hot_in_pehuajo())
'''

