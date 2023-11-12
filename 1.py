import requests
import phonenumbers
from bs4 import BeautifulSoup
import re
import time
from requests_html import HTMLSession
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

def find_phone_numbers(url):
    uClient  = uReq(url)  
    page_content = uClient.read()  
    uClient.close() 
    soup = BeautifulSoup(page_content, 'html.parser')
    text_elements = soup.find_all(string=True)
    phone_numbers = []
    for text in text_elements:
        for match in phonenumbers.PhoneNumberMatcher(text, "RU"):
            phone_numbers.append(phonenumbers.format_number(match.number, phonenumbers.PhoneNumberFormat.E164))
  
    return phone_numbers


if __name__ == '__main__':
    for url in urls:
        phone_numbers = list(set(find_phone_numbers(url)))
        if phone_numbers:
            print("For site ", url, "founded numbers are: ", phone_numbers, '\n')
        else:
            print("No phone numbers found")



