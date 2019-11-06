## proj_nps.py
## Skeleton for Project 2 for SI 507
## ~~~ modify this file, but don't rename it ~~~
from secrets import *
import json
import requests
from bs4 import BeautifulSoup



google_places_key = 'AIzaSyD68GvQhww_vaKhrB-1GVNqPH4MYWhWMfU'
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

## you can, and should add to and modify this class any way you see fit
## you can add attributes and modify the __init__ parameters,
##   as long as tests still pass
##
## the starter code is here just to make the tests run (and fail)
class NearbyPlace():
    def __init__(self, name):
        self.name = name

## Must return the list of NationalSites for the specified state
## param: the 2-letter state abbreviation, lowercase
##        (OK to make it work for uppercase too)
## returns: list of all of the NationalSites
##        (e.g., National Parks, National Heritage Sites, etc.) that are listed
##        for the state at nps.gov
def get_sites_for_state(state_abbr):
    state_abbr = state_abbr.lower()
    baseurl = f"https://www.nps.gov/state/{state_abbr}/index.htm"
    page_text = requests.get(baseurl).text
    page_soup = BeautifulSoup(page_text, 'html.parser')
    content = page_soup.find(id="list_parks")
    parklist = content.find_all(class_="clearfix")
    for each in parklist:
        category = each.find("h2")
        name = each.find("h3")
        desc = each.find("p")
        print(name.text,category.text,desc.text)
        eachabbr = each.find('a')['href'] 
        eachurl = f'https://www.nps.gov{eachabbr}index.htm'
        detail_page = requests.get(eachurl).text
        page_soup = BeautifulSoup(detail_page, 'html.parser')
        address = page_soup.find(class_="adr").text
        address = address.replace('\n', ', ')
        print(address)
        
    
get_sites_for_state("mi")

## Must return the list of NearbyPlaces for the specific NationalSite
## param: a NationalSite object
## returns: a list of NearbyPlaces within 10km of the given site
##          if the site is not found by a Google Places search, this should
##          return an empty list
def get_nearby_places_for_site(national_site):
    return []

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
