# -*- coding: utf-8 -*-
from requests import get
from requests.exceptions import RequestException
from contextlib import closing
from bs4 import BeautifulSoup
from datetime import datetime

def get_html(url):

    header = {
                 "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.75 Safari/537.36",
                 "X-Requested-With": "XMLHttpRequest"
             }
    try:
        with closing(get(url, stream=True, headers=header)) as resp:
            if quality_response(resp):
                return resp.content
            else:
                return None
    except RequestException as re:
        print(f"There was an error during requests to {url} : {str(re)}")
        return None

def quality_response(resp):

    content_type = resp.headers["Content-Type"].lower()
    return (resp.status_code == 200 and content_type is not None and content_type.find("html") > - 1)

def get_weather(weather):

    response = get_html(weather)

    if response is not None:
        soup = BeautifulSoup(response, "html.parser")

        temp = soup.find("div",attrs={"class":"current-temp"})
        phrase = soup.find("div",attrs={"class":"conditions-extra"})
        feels = soup.find("div",attrs={"class":"feels-like"})
        #data.append((high_val, low_val, last_price_val, change_val))
    else:
        raise Exception(f"There was an error retrieving contents at {weather}")
    return temp,phrase,feels

def fahrenheit_to_celcius(fr):
    f = int(fr)
    celcius = (f-32)*(5/9)

    return celcius

if __name__ == "__main__":
    print("####### Welcome to Weather Report Generator #######\n")
    place = input("Enter the City: ")
    weather_st = "https://www.wunderground.com/weather/in/"+place.lower()


    print("Getting todays weather report...")
    today_temp , today_phrase, today_feels= get_weather(weather_st)
    print(".../done")
    print('\n')
    
    temp_celcius = fahrenheit_to_celcius(today_temp.text.split()[0])
    temp_feel_celcius = fahrenheit_to_celcius(today_feels.text.split()[1].split(u'\N{DEGREE SIGN}')[0])
    print(place.upper()+"'s temperature "+'%.2f'%temp_celcius+u'\N{DEGREE SIGN}'+'C')
    print("Feels like "+'%.2f'%temp_feel_celcius+u'\N{DEGREE SIGN}'+'C')
    print("Description: " + today_phrase.text.split('N')[0])


   