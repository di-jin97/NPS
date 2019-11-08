## proj_nps.py
## Skeleton for Project 2 for SI 507
## ~~~ modify this file, but don't rename it ~~~
#from secrets import *
from secrets import google_places_key 
from secrets import mapbox_access_token 
import json
import requests
from bs4 import BeautifulSoup
import plotly.graph_objs as go
import numpy as np


#google_places_key = 'AIzaSyA7SpYbjtVmddhKpJXvgZ32W2uCkAxPI4E'
#mapbox_access_token = "pk.eyJ1IjoicHJpbmNpcGxleiIsImEiOiJjam1taTE3dGowamRjM3FqcG50MGp0anEwIn0.XuaFZy4Tff6aTfjiQUdd9Q"
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
        self.address_street = ''
        self.address_city = ''
        self.address_state = ''
        self.address_zip = ''
        
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


def params_unique_combination(baseurl, params):
    alphabetized_keys = sorted(params.keys())
    res = []
    for k in alphabetized_keys:
        res.append("{}-{}".format(k, params[k]))
    return baseurl + "_" + "_".join(res)
  

def make_request_using_cache(url,params):
    unique_ident = params_unique_combination(url,params)
    ## first, look in the cache to see if we already have this data
    if unique_ident in CACHE_DICTION:
        print("Getting cached data...")
        return CACHE_DICTION[unique_ident]

    ## if not, fetch the data afresh, add it to the cache,
    ## then write the cache to file
    else:
        print("Making a request for new data...")
        # Make the request and cache the new data
        resp = requests.get(url,params)
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
    params = {}
    page_text = make_request_using_cache(baseurl,params)
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
        detail_page = make_request_using_cache(eachurl,params)
        page_soup = BeautifulSoup(detail_page, 'html.parser')
        address = page_soup.find(class_="adr")
        newSite.address_street = address.find(class_="street-address").text.strip()
        newSite.address_city = address.find(itemprop="addressLocality").text.strip()
        newSite.address_state = address.find(class_="region").text.strip()
        newSite.address_zip = address.find(class_="postal-code").text.strip()
        site_list.append(newSite)
    return site_list


    
## Must return the list of NearbyPlaces for the specific NationalSite
## param: a NationalSite object
## returns: a list of NearbyPlaces within 10km of the given site
##          if the site is not found by a Google Places search, this should
##          return an empty list
    
    

def get_nearby_places_for_site(national_site):
    nearby_list = []
    query = national_site.name + ' ' + national_site.type +' '+ national_site.address_street
    queryurl = "https://maps.googleapis.com/maps/api/place/textsearch/json"
    param = {'query':query,'key':google_places_key}
    page_text = make_request_using_cache(queryurl,param)
    page_text = json.loads(page_text)
    result = page_text['results']
    #print(result)
    if not result:
        return nearby_list
    else:
        location = result[0]['geometry']['location']
        
        location_query = str(location['lat'])+', '+str(location['lng'])
        #print(location_query)
        nearby_url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json"
        nearby_param = {'location':location_query, 'radius':'10000','key':google_places_key}
        detail_page = make_request_using_cache(nearby_url,nearby_param)
        #print(detail_page)
        
        
        #nearby_text = requests.get(nearby_url,nearby_param).text
        nearby_text = json.loads(detail_page)
        result = nearby_text['results']
        for each in result:
            nearby = NearbyPlace(each['name'])
            nearby.lat = each['geometry']['location']['lat']
            nearby.lng = each['geometry']['location']['lng']
            #print(nearby.lat,nearby.lng)
            nearby_list.append(nearby)
    return nearby_list

#site2 = NationalSite('National Park','Yellowstone', 'There is a big geyser there.') 
site1 = NationalSite('National Monument','Sunset Crater Volcano', 'A volcano in a crater.')
a = get_nearby_places_for_site(site1)
#for each in a:
#    print(each)

  

## Must plot all of the NationalSites listed for the state on nps.gov
## Note that some NationalSites might actually be located outside the state.
## If any NationalSites are not found by the Google Places API they should
##  be ignored.
## param: the 2-letter state abbreviation
## returns: nothing
## what it needs to do: launches a page with a plotly map in the web browser
def plot_sites_for_state(state_abbr):
    site_list = get_sites_for_state(state_abbr)
    for national_site in site_list:
        query = national_site.name + ' ' + national_site.type +' '+ national_site.address_street
        queryurl = "https://maps.googleapis.com/maps/api/place/textsearch/json"
        param = {'query':query,'key':google_places_key}
        page_text = make_request_using_cache(queryurl,param)
        page_text = json.loads(page_text)
        result = page_text['results']
        if result:
            location = result[0]['geometry']['location']
            #location_query = str(location['lat'])+', '+str(location['lng'])
            national_site.lat = location['lat']
            national_site.lng = location['lng']
            #print (national_site.lat)
    for national_site in site_list:
        #print(national_site.lat,national_site.lng)
        if national_site.lat == 0:
            site_list.remove(national_site)
    
    lat_list=[]
    lng_list=[]
    name_list=[]
    for national_site in site_list:
        lat_list.append(national_site.lat)
        lng_list.append(national_site.lng)
        name_list.append(national_site.name)
          
    data = [
        go.Scattermapbox(
            lat=lat_list,
            lon=lng_list,
            mode='markers',
            marker=go.scattermapbox.Marker(
                size=9
            ),
            text=name_list,
        )
    ]

    layout = go.Layout(
        autosize=True,
        hovermode='closest',
        mapbox=go.layout.Mapbox(
            accesstoken=mapbox_access_token,
            bearing=0,
            center=go.layout.mapbox.Center(
                lat=np.mean(lat_list),
                lon=np.mean(lng_list)
            ),
            pitch=0,
            zoom=5
        ),
    )

    fig = go.Figure(data=data, layout=layout)
    fig.show()
    #py.iplot(fig, filename='Sites in the state '+state_abbr, auto_open=True)
    
        
#plot_sites_for_state("mi")
## Must plot up to 20 of the NearbyPlaces found using the Google Places API
## param: the NationalSite around which to search
## returns: nothing
## what it needs to do: launches a page with a plotly map in the web browser
def plot_nearby_for_site(site_object):
    nearby_lat = []
    nearby_lng = []
    nearby_name = []
    site_lat = []
    site_lng = []
    
    nearby_places = get_nearby_places_for_site(site_object)
    
    query = site_object.name + ' ' + site_object.type +' '+ site_object.address_street
    queryurl = "https://maps.googleapis.com/maps/api/place/textsearch/json"
    param = {'query':query,'key':google_places_key}
    page_text = make_request_using_cache(queryurl,param)
    page_text = json.loads(page_text)
    result = page_text['results']
    if result:
        location = result[0]['geometry']['location']
        if location['lat']:
            site_lat.append(location['lat'])
            site_lng.append(location['lng'])
        else:
            return
        
    for each in nearby_places:
        nearby_name.append(each.name)
        nearby_lat.append(each.lat)
        nearby_lng.append(each.lng)
    
    
    data = [
        go.Scattermapbox(
            lat=nearby_lat,
            lon=nearby_lng,
            mode='markers',
            marker=go.scattermapbox.Marker(
                size=7
            ),
            text=nearby_name,
        ),
        go.Scattermapbox(
            lat=site_lat,
            lon=site_lng,
            mode='markers',
            marker=go.scattermapbox.Marker(
                size=10,
                symbol='star'
            ),
            text=site_object.name,
        )
    ]

    layout = go.Layout(
        autosize=True,
        hovermode='closest',
        mapbox=go.layout.Mapbox(
            accesstoken=mapbox_access_token,
            bearing=0,
            center=go.layout.mapbox.Center(
                lat=site_lat[0],
                lon=site_lng[0]
            ),
            pitch=0,
            zoom=10
        ),
    )

    fig = go.Figure(data=data, layout=layout)
    fig.show()
    
plot_nearby_for_site(site1)


