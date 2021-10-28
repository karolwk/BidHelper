import re
import json
import time
import requests
from requests_html import HTMLSession


from bs4 import BeautifulSoup, element
"""
Scraping futbin for player data
"""
session = HTMLSession()
pages = [] # List of pages to scrap
domain = "https://www.futbin.com/players?page=" # domain for scraping
players_dict = {'players': []} # dictionary with players ready for JSON conversion
scraped_pages = []


def printProgressBar (iteration, total, prefix = '', suffix = '', decimals = 1, length = 100, fill = '█', printEnd = "\r"):
    """
    Call in a loop to create terminal progress bar
    @params:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        length      - Optional  : character length of bar (Int)
        fill        - Optional  : bar fill character (Str)
        printEnd    - Optional  : end character (e.g. "\r", "\r\n") (Str)
    """
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)
    print(f'\r{prefix} |{bar}| {percent}% {suffix}', end = printEnd)
    # Print New Line on Complete
    if iteration == total: 
        print()

def get_pages(pages):
    """ Gets list of pages to scrap and fills array"""    
    with open("lista.txt", "r") as my_file:
        for n in my_file:
            pages.append(n.rstrip())


def save_json(dict_):


    #Serializing to json
    json_object = json.dumps(dict_, indent = 4)

    with open("sample.json", "w") as outfile:
        outfile.write(json_object)

  
    

   
def get_player_data(soup, tag, tag_class =""):
    """Returns one specified element with tag class"""
    if(tag_class):
        return soup.find(tag, tag_class)
    else:
        return soup.find(tag)
   

def get_page_elements(url, tag, tag_class = ""):
    """Return specified tag elements"""
    r = requests.get(url, timeout=10)
    soup = BeautifulSoup(r.content, 'html.parser')   
    if(tag_class):                     
        return soup.find_all(tag, tag_class)
    else:
        return soup.find_all(tag)


def find_number_of_pages(url):
    """Returns max pages to search"""
    elements = get_page_elements(url, "a", "page-link") # Searching for tag "a" and class "page-link"
    numbers = []   
    for ele in elements:        
        try:
            number = int(ele.string)
            numbers.append(number)            
        except:
            pass
    return (max(numbers))


def append_list(tags, list_):
    """Appends list of links to player profiles"""
    domain = "https://www.futbin.com"
    for link in tags:
        try:
            list_.append(f'{domain}{link["href"]}')
        except:
            pass


def set_price(price):
    """Sets deafult player price"""
    try:
        new_price = int(price)
        return new_price
    except:
        return 0




def list_of_profiles(pages):
    """Builds a list of links to each player profile page"""
    my_list = []
    for link in pages:
        max_pages = find_number_of_pages(link)
        for i in range(1, max_pages + 1):
            endpoint = link.find("&")
            actual_page = f'{domain}{i}{link[endpoint:]}' # construct link to visit
            player_tags = get_page_elements(actual_page, "a", "player_name_players_table") # list of hrefs to each player page
            time.sleep(2) # we need tu use timeout to not get 403's error
            append_list(player_tags, my_list)
            printProgressBar(i, max_pages, prefix = f'Progres w poszukiwaniu strony {link}:', suffix = 'wszystkich wpisów', length = 50)

    return my_list

def scrap_player_page(url):
    """Scraps player page for important data and returs dictionary object"""
    r = session.get(url)
    r.html.render()
   
    player = {
        "name": "",
        "price": 0,
        "overall": 0,
        "sugBuy": 0,
        "sugSell": 0    
    }

    player["name"] = r.html.find('.pcdisplay-name', first=True).text
    player["price"] = int(r.html.find('#pc-lowest-2', first=True).text.replace(",","")) 
    if (player["price"] == 0): # In case if price is 0 get the avarage from ps and xbox prices
        price_ps = int(r.html.find('#ps-lowest-2', first=True).text.replace(",","")) 
        price_xbox = int(r.html.find('#xbox-lowest-2', first=True).text.replace(",","")) 
        player["price"] = (price_ps + price_xbox) // 2
    player["overall"] = r.html.find('.pcdisplay-rat', first=True).text
    print(player)
    return player


get_pages(pages)
scraped_pages = list_of_profiles(pages)
num = 1
for link in scraped_pages:
    players_dict["players"].append(scrap_player_page(link))
    printProgressBar(num, len(scraped_pages), prefix = f'Progres w budowaniu slownika:', suffix = 'wszystkich wpisów', length = 50)
    num += 1
save_json(players_dict)









