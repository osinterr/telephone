import aiohttp
import asyncio
import phonenumbers
from bs4 import BeautifulSoup
from urllib.request import urlopen as uReq

urls = [
    "https://hands.ru/company/about",
    "https://repetitors.info",
    "https://www.philol.msu.ru/news",
    "https://prodoctorov.ru/moskva/vrach/377691-krivova/",
    "https://bmstu.ru/contacts",
    "https://www.mirea.ru/",
    "https://www.topnomer.ru/blog/federalnye-i-gorodskie-nomera-telefonov.html"
]

async def find_phone_numbers(url, session):
    async with session.get(url) as response:
        page_content = await response.read()

    soup = BeautifulSoup(page_content, 'html.parser')
    text_elements = soup.find_all(string=True)
    phone_numbers = []

    for text in text_elements:
        for match in phonenumbers.PhoneNumberMatcher(text, "RU"):
            phone_numbers.append(phonenumbers.format_number(match.number, phonenumbers.PhoneNumberFormat.E164))

    return url, phone_numbers

async def process_urls(urls):
    async with aiohttp.ClientSession() as session:
        tasks = [find_phone_numbers(url, session) for url in urls]
        results = await asyncio.gather(*tasks)
        return dict(results)

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    result = loop.run_until_complete(process_urls(urls))

    for url, phone_numbers in result.items():
        if phone_numbers:
            print(f"For site {url}, founded numbers are: {phone_numbers}\n")
        else:
            print("No phone numbers found")
