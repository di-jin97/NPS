## proj_nps.py
## Skeleton for Project 2 for SI 507
## ~~~ modify this file, but don't rename it ~~~
from secrets import *
import json
import requests
from bs4 import BeautifulSoup



google_places_key = 'AIzaSyA7SpYbjtVmddhKpJXvgZ32W2uCkAxPI4E'
## you can, and should add to and modify this class any way you see fit
## you can add attributes and modify the __init__ parameters,
##   as long as tests still pass
##
## the starter code is here just to make the tests run (and fail)
class NationalSite():
    def __init__(self, type, name, desc, url=None):
        self.type = type
        self.name = name
        self.description = desc
        self.url = url

        # needs to be changed, obvi.
        self.address_street = '123 Main St.'
        self.address_city = 'Smallville'
        self.address_state = 'KS'
        self.address_zip = '11111'
        
        self.lat = 0
        self.lng = 0
        
        
    def __str__(self):
        return self.name +" (" + self.type + "): " + self.address_street + ", " + self.address_city + ", " + self.address_state + " " + self.address_zip
    

## you can, and should add to and modify this class any way you see fit
## you can add attributes and modify the __init__ parameters,
##   as long as tests still pass
##
## the starter code is here just to make the tests run (and fail)
class NearbyPlace():
    def __init__(self, name):
        self.name = name
        self.lat = 0
        self.lng = 0
    
    def __str__(self):
        return self.name




#Caching Part
CACHE_FNAME = 'cache.json'
try:
    cache_file = open(CACHE_FNAME, 'r')
    cache_contents = cache_file.read()
    CACHE_DICTION = json.loads(cache_contents)
    cache_file.close()

# if there was no file, no worries. There will be soon!
except:
    CACHE_DICTION = {}

# A helper function that accepts 2 parameters
# and returns a string that uniquely represents the request
# that could be made with this info (url + params)

def get_unique_key(url):
  return url  

def make_request_using_cache(url):
    unique_ident = get_unique_key(url)

    ## first, look in the cache to see if we already have this data
    if unique_ident in CACHE_DICTION:
        print("Getting cached data...")
        return CACHE_DICTION[unique_ident]

    ## if not, fetch the data afresh, add it to the cache,
    ## then write the cache to file
    else:
        print("Making a request for new data...")
        # Make the request and cache the new data
        resp = requests.get(url)
        CACHE_DICTION[unique_ident] = resp.text
        dumped_json_cache = json.dumps(CACHE_DICTION)
        fw = open(CACHE_FNAME,"w")
        fw.write(dumped_json_cache)
        fw.close() # Close the open file
        return CACHE_DICTION[unique_ident]



## Must return the list of NationalSites for the specified state
## param: the 2-letter state abbreviation, lowercase
##        (OK to make it work for uppercase too)
## returns: list of all of the NationalSites
##        (e.g., National Parks, National Heritage Sites, etc.) that are listed
##        for the state at nps.gov
def get_sites_for_state(state_abbr):
    site_list = []
    state_abbr = state_abbr.lower()
    baseurl = f"https://www.nps.gov/state/{state_abbr}/index.htm"
    page_text = make_request_using_cache(baseurl)
    page_soup = BeautifulSoup(page_text, 'html.parser')
    content = page_soup.find(id="list_parks")
    parklist = content.find_all(class_="clearfix")
    for each in parklist:
        cate = each.find("h2").text
        name = each.find("h3").text
        desc = each.find("p").text
        newSite = NationalSite(cate,name,desc)
        eachabbr = each.find('a')['href'] 
        eachurl = f'https://www.nps.gov{eachabbr}index.htm'
        newSite.url = eachurl
        detail_page = make_request_using_cache(eachurl)
        page_soup = BeautifulSoup(detail_page, 'html.parser')
        address = page_soup.find(class_="adr")
        newSite.address_street = address.find(class_="street-address").text.strip()
        newSite.address_city = address.find(itemprop="addressLocality").text.strip()
        newSite.address_state = address.find(class_="region").text.strip()
        newSite.address_zip = address.find(class_="postal-code").text.strip()
        site_list.append(newSite)
    return site_list
    #for each in site_list:
    #    print(each)
    
a = get_sites_for_state("mi")
b = a[0]
## Must return the list of NearbyPlaces for the specific NationalSite
## param: a NationalSite object
## returns: a list of NearbyPlaces within 10km of the given site
##          if the site is not found by a Google Places search, this should
##          return an empty list
    
    

def get_nearby_places_for_site(national_site):
    nearby_list = []
    query = national_site.name + ' ' + national_site.type + ' ' + national_site.address_street
    queryurl = "https://maps.googleapis.com/maps/api/place/textsearch/json"
    param = {'query':query,'key':google_places_key}
    page_text = requests.get(queryurl,param).text
    page_text = json.loads(page_text)

    location = page_text['results'][0]['geometry']['location']
   
    location_query = str(location['lat'])+', '+str(location['lng'])
    print(location_query)
    #lng = location['lng']
    
    nearby_url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json"
    nearby_param = {'location':location_query, 'radius':'15000','key':google_places_key}
    nearby_text = requests.get(nearby_url,nearby_param).text
    nearby_text = json.loads(nearby_text)
    result = nearby_text['results']
    for each in result:
        nearby = NearbyPlace(each['name'])
        nearby_list.append(nearby)
    return nearby_list
get_nearby_places_for_site(b)


  

## Must plot all of the NationalSites listed for the state on nps.gov
## Note that some NationalSites might actually be located outside the state.
## If any NationalSites are not found by the Google Places API they should
##  be ignored.
## param: the 2-letter state abbreviation
## returns: nothing
## what it needs to do: launches a page with a plotly map in the web browser
def plot_sites_for_state(state_abbr):
    pass

## Must plot up to 20 of the NearbyPlaces found using the Google Places API
## param: the NationalSite around which to search
## returns: nothing
## what it needs to do: launches a page with a plotly map in the web browser
def plot_nearby_for_site(site_object):
    pass


