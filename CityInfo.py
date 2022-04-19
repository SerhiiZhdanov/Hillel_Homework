import requests


class CityInfo:
    currency_url = 'https://countriesnow.space/api/v0.1/countries/currency'
    population_url = "https://countriesnow.space/api/v0.1/countries/population/cities"

    def __init__(self):
        self.get_currency()
        self.get_population()

    def get_population(self):
        """
        Метод класса CityInfo.

        Получение данных из API.

        :return: Возвращает собранные данные в формате JSON
        """
        population_data = requests.get(self.population_url)
        if 200 <= population_data.status_code <= 299:
            population_data_text = population_data.json()
        else:
            raise ValueError('Получили ошибку от сайта')
        return population_data_text

    def get_currency(self):
        """
        Метод класса CityInfo.

        Получение данных из API.

        :return: Возвращает полученные данные в формате JSON
        """
        currency_data = requests.get(self.currency_url)
        if 200 <= currency_data.status_code <= 299:
            currency_data_text = currency_data.json()
        else:
            raise ValueError('Получили ошибку от сайта')
        return currency_data_text

    def filter_country(self, city):
        """
        Метод класса CityInfo.

        Принимает результат работы метода get_population()
        и обрабатывает данные.

        :param city: Введенное пользователем название города(STR)

        :return: Возвращает обработанные данные в виде списка
        """
        filtered_country = self.get_population().get('data')
        countries = []
        for country in filtered_country:# Итерируем принятый список данных и произвоим поиск по ключевому значению "city"
            if country['city'].capitalize().find(city.capitalize()) != -1:
                countries.append(country)
        return countries

    def add_filter_currency(self, city):
        """
        Метод класса CityInfo.

        Принимает результат работы метода filter_country()
        и обрабатывает данные.

        :param city: Введенное пользователем название города(STR)

        :return: Возвращает обработанные данные в виде списка
        """
        filtered_currency = self.get_currency().get('data')
        countries = self.filter_country(city)
        try:  # Если метод принимает пустой список - тогда ошибка
            if len(countries) == 0:
                raise ValueError
        except ValueError:
            print('-----------------------------------------')
            print()
            print(f'Invalid city name: {city}')
            print('=========================================')
        for country in countries:  # Итерируем полученный список и и список с валютами на наличие совпадений.
            for currency_in_country in filtered_currency:
                if country['country'].capitalize().find(currency_in_country['name'].capitalize()) != -1:
                    country.update({'currency': currency_in_country['currency']}) #если находим совпадение, то добавляем ключ со значением
        return countries

    def print_info(self, city):
        """
        Метод класса CityInfo.

        Вывод данных в консоль.

        :param city: Введенное пользователем название города(STR)

        """
        result_currency = self.add_filter_currency(city)
        for result in result_currency:
            print('-----------------------------------------')
            print(result['city'].capitalize())
            print()
            print(result['country'].capitalize())
            print(result['currency'])
            print(result['populationCounts'][0]['value'])
            print('=========================================')


def main():
    start = CityInfo()
    while True:
        city = input('Введите название города: ')
        start.print_info(city)


if __name__ == '__main__':
    main()
