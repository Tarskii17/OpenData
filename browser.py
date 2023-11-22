from pyppeteer import launch
from parser_data import parse, parse_table
import warnings

warnings.filterwarnings("ignore", category=DeprecationWarning)


async def launcher_for_data(url, json_columns):
    dictionary = {}

    browser = await launch(headless=True)
    page = await browser.newPage()

    for i in range(len(json_columns)):
        await page.goto(url + json_columns[i])
        await parse(page, dictionary, json_columns[i])

    await browser.close()

    return dictionary


async def launcher_for_table(url):
    return await parse_table(url)

