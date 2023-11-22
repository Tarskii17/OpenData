import asyncio
import requests
from bs4 import BeautifulSoup
import pandas as pd
import json


async def parse(page, dictionary, json_column):
    # Ждем, пока данные загрузятся (может потребоваться настроить время ожидания)
    await page.waitForSelector('.maincounter-number')

    await asyncio.sleep(1)
    # Извлекаем элементы с классом "maincounter-number"
    main_counter_elements = await page.querySelectorAll('.maincounter-number')

    # Итерируемся по найденным элементам и извлекаем данные
    text = await page.evaluate('(element) => element.textContent', main_counter_elements[0])
    dictionary[json_column] = text.strip()


async def parse_table(url):
    response = requests.get(url)

    if response.status_code == 200:
        # Используем BeautifulSoup для парсинга HTML-кода страницы
        soup = BeautifulSoup(response.text, 'html.parser')

        # Находим таблицу на странице (в данном случае, используем первую таблицу)
        table = soup.find_all('table')[0]

        # Используем pandas для чтения HTML-таблицы
        df = pd.read_html(str(table))[0].drop(columns=['#']).to_json(orient='records')
        
        parsed = json.loads(df)
        json.dumps(parsed, indent=4)

        return parsed

    else:
        print("Ошибка при получении данных. Код статуса:", response.status_code)
