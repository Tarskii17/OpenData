import asyncio
import requests
from bs4 import BeautifulSoup
import pandas as pd
import json


async def parse(page, dictionary, json_column):
    # Waiting for the data to load (you may need to adjust the waiting time)
    await page.waitForSelector('.maincounter-number')

    await asyncio.sleep(1)
    # Extracting elements with the "maincounter-number" class
    main_counter_elements = await page.querySelectorAll('.maincounter-number')

    # Iterate over the found elements and extract the data
    text = await page.evaluate('(element) => element.textContent', main_counter_elements[0])
    dictionary[json_column] = text.strip()


async def parse_table(url):
    response = requests.get(url)

    if response.status_code == 200:
        # We use BeautifulSoup to parse the HTML code of the page
        soup = BeautifulSoup(response.text, 'html.parser')

        # Find the table on the page (in this case, use the first table)
        table = soup.find_all('table')[0]

        # Using pandas to read HTML tables
        df = pd.read_html(str(table))[0].drop(columns=['#']).to_json(orient='records')
        
        parsed = json.loads(df)
        json.dumps(parsed, indent=4)

        return parsed

    else:
        print("An error occurred while receiving the data. Status code:", response.status_code)
