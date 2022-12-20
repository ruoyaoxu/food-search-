import json
import requests
from bs4 import BeautifulSoup
import time
import plotly.graph_objs as go
import webbrowser
import re

import plotly.express as px
import numpy


def load_cache(cache_file_name):
    try:
        cache_file = open(cache_file_name, 'r')
        cache_file_contents = cache_file.read()
        cache = json.loads(cache_file_contents)
        cache_file.close()
    except:
        cache = {}
    return cache


def save_cache(cache, cache_file_name):
    cache_file = open(cache_file_name, 'w')
    contents_to_write = json.dumps(cache)
    cache_file.write(contents_to_write)
    cache_file.close()

CACHE_FILE = 'cache.json'
CACHE_DICT = load_cache(CACHE_FILE)

def request_with_cache(url):
    cache_dict = load_cache()
    if url in cache_dict.keys():
        print("Using Cache")
        response = cache_dict[url]
    else:
        print("Fetching")
        response = requests.get(url).text
        save_cache(cache_dict)
    return response

def getJson(parameter):
    url = "https://api.yelp.com/v3/businesses/search"
    KEY = "flss26tKSfgW3t4xsYcXIIbIhuh9bwh2Lmi1YfutTuI6F95hpE0rYz-iQciDk4TGiAVerBgTjASqkKw0HPL5s_IXpacTDFcRbjLkJZMiwr1d7W6Sd0LmZpUm_QugY3Yx"
    HEADERS = {'Authorization': 'bearer %s' % KEY}
    data = requests.get(url = url,
                        params = parameter,
                        headers = HEADERS).json()
    return data



area_you_search = []
def inputterm():
    parameter = {'limit': 50}
    term = input("Please enter a term you want to search(food, drink, hotel etc.): ")
    if term:
        parameter['term'] = term
        location = input("Search by location or longitude and latitude(Enter 1 or 2):")
        try:
            if int(location) == int(1):
                location = input("Enter you location here:")
                area_you_search.append(location)
                parameter['location'] = location
            elif int(location) == int(2):
                long= input("Enter longitude:")
                la = input("Enter latitude:")
                parameter['longitude'] = long
                parameter['latitude'] = la
        except:
            print("error, try once")
            return inputterm()
    return parameter

def area_another(parameter):
    question = input("Do you want to search another area?(yes/no)")
    if question == "yes":
        location2 = input("Search by location or longitude and latitude(Enter 1 or 2):")
        try:
            if int(location2) == int(1):
                location = input("Enter you location here:")
                area_you_search.append(location)
                parameter['location'] = location
            elif int(location2) == int(2):
                long= input("Enter longitude:")
                la = input("Enter latitude:")
                parameter['longitude'] = long
                parameter['latitude'] = la
        except:
            print("error, try once")
            return area_another(parameter)
    elif question == "no":
        print("OK, let's go.")
        return None
    else:
        print("Error")
        return area_another(parameter)
    return parameter

def rating(data):
    question = input("Do you want to select you rating?(enter (1.0 - 5.0) or no): ")
    if question == "no":
        print("Ok, let's go")
        items = [i['name'] for i in data]
        for i in range(len(items)):
            print(i+1 , ":", items[i])
    else:
        question = float(question)
        if float(question) <= 5 and float(question > 0):
            items = [i['name'] for i in data if i['rating'] == question]
            for i in range(len(items)):
                print(i+1 , ":", items[i])
        else:
            print("Range error, try once")
            rating(data)
    return items

def getwebsite(name, data):
    for i in data:
        if name == i['name']:
            print(i['url'])
            return i['url']

def select(items):
    input2 = input("Do you want to select a business?(yes/no): ")
    if input2 == "no":
        print("OK, lets go")
    elif input2 == "yes":
        number = input("Please enter a business you want to see(number): ")
        try:
            if int(number) > 0 and int(number) < int(len(items)+1):
                return items[int(number)-1]
            else:
                print("Range error, try again")
                return select(items)
        except:
            print("Error, try once")
            return select(items)
    else:
        print("error, try once")
        return select(items)

def webopen(url):
    question4 = input("Do you want to open the website?(yes/no) : ")
    if question4 == "yes":
        webbrowser.open(url)
    elif question4 == "no":
        print("Ok, lets go")
    else:
        print("Wrong answer")
        webopen(url)




def fetch(url):
    question2 = input("Do you want to see information here? ( yes/no): " )
    if question2 == "yes":
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        name = soup.find('h1').text
        print(name)

        rating_tag = soup.find('div', attrs={'aria-label': re.compile('star rating')})
        rating = rating_tag['aria-label']
        print(rating)

        review_count = soup.find('span', text=re.compile('reviews')).text

        print(review_count)

        website_business = soup.find('p', text="Business website")
        if website_business :
            website = website_business.next_sibling.text
            print(website)

        phone= soup.find('p', text="Phone number")
        if phone:
            phone_no = phone.next_sibling.text
            print(phone_no)

        address = soup.find('a', text="Get Directions")
        if address:
            address = address.parent.next_sibling.text

    elif question2 == "no":
        print("Ok, let's go")
    else:
        print("Error, try again.")
        return fetch(url)


number_of_delivery_transaction_each_area = []

def transaction(data):
    list_delivery = [i['name'] for i in data if 'delivery' in i['transactions']]
    number_of_delivery_transaction_each_area.append(len(list_delivery))
    return number_of_delivery_transaction_each_area

def show_graph(xvals, yvals):
    bar_data = go.Bar(x=xvals, y=yvals)
    basic_layout = go.Layout(title="A Bar Graph")
    fig = go.Figure(data=bar_data, layout=basic_layout)

    fig.show()

def pie_chart(value, names):
    fig = px.pie(values=value, names=names)
    fig.show()


class food():
    def __init__(self, name="None", url="None", location_address="", rating= 0, transactions=None, state=None, json=None):
        self.name = name
        self.url = url
        self.location_addresss = location_address
        self.rating = rating
        self.transactions = transactions
        if json:
            self.name = json['name']
            self.url = json['url']
            self.rating = json['rating']
            self.transactions = json['transactions']

    def transaction(transactions):
        if len(transactions) == 0:
            print("No source find.")
        else:
            print([i for i in transactions])



def main():

    CACHE_FILE = 'cache.json'
    CACHE_DICT = load_cache(CACHE_FILE)




    parameter = inputterm()
    data = getJson(parameter)['businesses']
    items = rating(data)
    business_name = select(items)
    if business_name != None:
        url = getwebsite(business_name, data)
        fetch(url)
        webopen(url)
    transaction(data)



    n = 0
    bulin = True
    while n < 10 and bulin == True:
        parameter = area_another(parameter)
        if parameter != None:
            data2 = getJson(parameter)['businesses']
            transaction(data2)
            items = rating(data2)
            business_name = select(items)
            if business_name != None:
                url = getwebsite(business_name, data2)
                fetch(url)
                webopen(url)
            data.append(data2)
        else:
            break
        n += 1

    save_cache(data, CACHE_FILE)

    print(area_you_search)
    print(number_of_delivery_transaction_each_area)

    answer = input("Do you want to see the bar chart of the number of the delivery allowed businesses those areas you search?(yes/no)")
    if answer == "yes":
        print("Please wait 5 seconds....")
        time.sleep(5)
        show_graph(area_you_search, number_of_delivery_transaction_each_area)
    else:
        print("OK, let' go.")

    name = ['Business that has delivery in this area', 'Business do not have delivery in this area']

    n = len(number_of_delivery_transaction_each_area)
    while n > 0:
        answer2 = input("Do you want to see the graph of the percent of delivery businesses in one area?(yes/no)")
        if answer2 == "yes":
            answer3 = input("Which area? ")
            if answer3 in area_you_search:
                index1 = area_you_search.index(answer3)
                value = [number_of_delivery_transaction_each_area[index1], 50 - number_of_delivery_transaction_each_area[index1]]
                pie_chart(value, name)
            else:
                print("Error.")
        elif answer2 == "no":
            print('End!Bye')
            break
        n = n - 1

if __name__ == '__main__':
    main()










