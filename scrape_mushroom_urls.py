# Functions to scrape data from mushroom.world
# If called from the command line, the script prints out a json object of mushroom information
# example:
# python scrape_mushroom_urls.py 'http://www.mushroom.world/show?n=Amanita-virosa' 'http://www.mushroom.world/show?n=Galerina-marginata'
#
# See the comments above the functions for further documentation
# 
# Tuomo Nieminen 10/2017

from bs4 import BeautifulSoup
import requests
import sys
import re
import json

# Scrape mushroom url
#
# scrape_mushroom_url takes as input an url to a page in mushroom.world containing information
# related to a single mushroom and returns a python dictionary of information (including image url's) 
# related to the mushroom.
#
# @param url An url to a mushroom web page in mushroom.world
# 
# @return 
# Returns a python dictionary containing the following keys:
# - name1: (string) Name of the mushroom.
# - name2 (string) Name given in parenthesis. Can be '' if no such name was given
# - images: (list) A list of image urls
# - info: (dict) A dictionary of information related to the mushroom. 
#       keys: Family, Location, Dimensions, Edibility, Description (dict)
#           Description keys: General, Cap, Gills, Stem
# 
# @examples
# 
# from bs4 import BeautifulSoup
# import requests
# 
# url = 'http://www.mushroom.world/show?n=Galerina-marginata'
# mushroom = scrape_mushroom(url)
# print(mushroom)
# 
def scrape_mushroom(url):
    
    # retrive site data as BeautifullSoup object
    data  = requests.get(url).text
    soup = BeautifulSoup(data, 'html.parser')
    
    # etract and parse name, labels (Family, Location, Dimensions, Edibility, Description)
    # and content text related to the labels
    name_content = soup.find(class_ = "caption").find("b").contents
    names = re.sub('[^A-Za-z0-9( ]+', '', name_content[0]).split("(")
    names = [n.strip() for n in names]
    name1 = names[0]
    if(len(names) > 1):
        name2 = names[1]
    else:
        name2 = ''

    labels = soup.find_all(class_ ="labelus")
    labels = [label.contents[0] for label in labels]

    texts = soup.find_all(class_ = "textus")
    texts = [text.contents[0] for text in texts]

    # extract mushroom description as a dictionary
    description = soup.find(class_ = "longtextus").contents
    description = [re.sub('[^A-Za-z0-9,.<> ]+', '', str(d)).strip() for d in description]
    description = [re.sub('<b>', '', d) for d in description if (d != "") & (d != "<br>")]
    description.insert(0, 'General')
    description = dict(zip(description[0::2], description[1::2]))

    texts.append(description)
    assert len(labels) == len(texts)
    
    # find image urls
    images = soup.find(id="mushroom-list").find_all(class_ = "image")
    image_urls = ['http://www.mushroom.world' + image.a["href"] for image in images]

    # contruct the mushroom dictionary
    mushroom = dict(name1 = name1, name2 = name2, images = image_urls, info = dict(),)

    # add labels as keys and text as values
    for i in range(len(labels)):
        mushroom["info"][labels[i]] = texts[i]

    return mushroom


# Get shrooms
# Get shoorm takes as input a list of mushroom urls and scrapes each url using scrape_mushroom().
# 
# @param urls A list of mushroom.world mushroom page urls
#
# @return Returns a list of python dictionaries returned by scrape_mushroom(). 
# See the documentation of scrape_mushroom for details of the dictionaries.
# @examples
#
# urls = ['http://www.mushroom.world/show?n=Amanita-virosa', 'http://www.mushroom.world/show?n=Galerina-marginata']
# shrooms = GetShrooms(urls)
#
# import json
# json.dumps(shrooms)
#
def GetShrooms(urls):
    return [scrape_mushroom(url) for url in urls]


if __name__ == '__main__':
    shrooms = GetShrooms(sys.argv[1:])
    print(json.dumps(shrooms))
