from os import error
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
DEFAULT_JSON_FILE = "players_data.json"
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


def save_json(dict_, file_name=DEFAULT_JSON_FILE):
    #Serializing to json
    json_object = json.dumps(dict_, indent = 4)
    with open(file_name, "w") as outfile:
        outfile.write(json_object)

def open_json(file_name=DEFAULT_JSON_FILE):
    """Open and convert JSON to dict"""
    with open(file_name, "r") as infile:
        dict_ = infile.read()
    return json.loads(dict_)
    

def update_players(fixed= False, json_file=DEFAULT_JSON_FILE):
    """Updates prices for players and save to JSON"""
    players_dict = open_json(json_file) 
    update_optimal_prices(players_dict, fixed)
    save_json(players_dict, json_file)

   
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


def set_price(response, price) -> int:
    """Sets deafult player price"""
    try:
        price = int(price)
        if (price == 0 or price == 10000): # In case if price is 0 or exacly 10000, get the avarage from ps and xbox prices
            price_ps = int(response.html.find('#ps-lowest-2', first=True).text.replace(",","")) 
            price_xbox = int(response.html.find('#xbox-lowest-2', first=True).text.replace(",","")) 
            price = (price_ps + price_xbox) // 2
        return price
    except:
        raise Exception(f"Something was wrong with response {response}")


def set_buy_price(price) -> int:
    """Sets suggested buing price"""
    if price < 700:
        return 350 # 350 default
    elif price < 860:
        return 450 # 400 default
    elif price < 1200:
        return 550 # 500 default
    elif price < 1700:
        return 650 # 600 default
    return 700

def set_fixed_sell_price(price):
    """In case market is on fire set minimum selling price"""
    if price < 850:
        return 750
    else:
        return set_sell_price(price)


def set_sell_price(price) -> int:
    """Sets suggested selling price"""
    lng = len(str(price))
    new_price = int((price - (price * .05)) // 100 * 100)
    if lng < 4 or price == 1000: return new_price + 50
    return new_price - 100


def update_optimal_prices(dict_, fixed = False):
    """Updates dictionaries prices for sell and buy"""    
  
    for player in dict_['players']:
        player['sugBuy'] = set_buy_price(player['price'])
        if fixed:
            player['sugSell'] = set_fixed_sell_price(player['price'])
        else:
            player['sugSell'] = set_sell_price(player['price'])





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

def scrap_player_page(url, times=3, seconds=10):
    """Scraps player page for important data and returs dictionary object"""
    player = {
            "id": "",
            "name": "",
            "price": 0,
            "overall": 0,
            "sugBuy": 0,
            "sugSell": 0    
        }
    for _ in range(times):
        r = session.get(url)
        if (r.status_code == 200):
            r.html.render()
            id = r.html.find('.player-ids.hidden')
            player["id"] = id[0].attrs['data-player-id']
            player["name"] = r.html.find('.pcdisplay-name', first=True).text    
            player["overall"] = r.html.find('.pcdisplay-rat', first=True).text
            price = r.html.find('#pc-lowest-1', first=True).text.replace(",","")
            if price == "-": # Sometimes page don't load properly so we want to try again
                time.sleep(seconds)
                continue
            player["price"] = set_price(r, price)
            return player
        time.sleep(seconds)
    raise Exception(f'Sorry, there was an error with scraping page {url}') 
    



# def main():
#     start_time = time.time()   

#     get_pages(pages)
#     scraped_pages = list_of_profiles(pages)
#     num = 1
#     for link in scraped_pages:
#         try:
#             players_dict["players"].append(scrap_player_page(link))
#         except Exception as e: print(e)

#         printProgressBar(num, len(scraped_pages), prefix = f'Progres w budowaniu slownika:', suffix = 'wszystkich wpisów', length = 50)
#         num += 1
#     update_optimal_prices(players_dict)
#     save_json(players_dict)
#     end_time = time.time() - start_time
#     print(f'It took {end_time:.2f} seconds to execute.')


# if __name__ == '__main__':
#     main()



update_players(True)
    
