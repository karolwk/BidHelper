import re
import time
import requests
from bs4 import BeautifulSoup, element
"""
Scraping futbin for player data
"""

pages = [] # List of pages to scrap
domain = "https://www.futbin.com/players?page=" # domain for scraping
players_dict = {'players': []} # dictionary with players ready for JSON conversion


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


def find_user(user, finders):    
    for link in finders:
        if link['href'] == user:
            print(f'Znalazlem cie na stronie:')
            return True
    return False


def get_pages(pages):
    """ Gets list of pages to scrap and fills array"""    
    with open("lista.txt", "r") as my_file:
        for n in my_file:
            pages.append(n.rstrip())
   


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


def build_list(tags, list_):
    """Builds list of links to player profile"""

    for link in tags:
        try:
            list_.append(link['href'])
        except:
            pass



def main(pages):
    my_list = []
    for link in pages:
        max_pages = find_number_of_pages(link)
        for i in range(1, max_pages + 1):
            endpoint = link.find("&")
            actual_page = f'{domain}{i}{link[endpoint:]}' # construct link to visit
            player_tags = get_page_elements(actual_page, "a", "player_name_players_table") # list of hrefs to each player page
            time.sleep(2) # we need tu use timeout to not get 403's error
            build_list(player_tags, my_list)
            printProgressBar(i, max_pages, prefix = f'Progres w poszukiwaniu strony{link}:', suffix = 'wszystkich wpisów', length = 50)
    print(len(my_list))




        




get_pages(pages)
main(pages)













# search = '/users/'
# inp = input('Wprowadz nick użytkownia na SPOJu ')

# search += inp + '/'

    
# for i in range(0, 60000, 25):
#     r = requests.get(f'https://pl.spoj.com/ranks2/?start={i}', timeout=10)
#     soup = BeautifulSoup(r.content, 'html.parser')
#     finders = soup.find_all("a")
#     if find_user(search, finders):
#         print(r.url)
#         break
#     printProgressBar(i, 60000, prefix = 'Przeszukuje ranking:', suffix = 'wszystkich wpisów', length = 50)
    
    
            
    









    
