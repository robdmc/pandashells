#! /usr/bin/env python

# --- standard library imports
import os
import sys
import argparse
import json
import urllib
import csv

# ############ dev only.  Comment out for production ######################
sys.path.append('../..')
# #########################################################################

from pandashells.lib import module_checker_lib

# --- import required dependencies
modulesOkay = module_checker_lib.check_for_modules([
    'numpy',
    'pandas',
    'requests'])

if not modulesOkay:
    sys.exit(1)

import requests
import numpy as np
import pandas as pd

# --- define the google geocoding end-point
URL = 'https://maps.googleapis.com/maps/api/geocode/json'


# ============================================================================
def geocode(address, dry_run=False):
    """
    Run the address from the input string through the publicly available
    google geocoder.
    """

    # --- set the default output
    out = {
        'input_address': address,
        'lat': np.NaN,
        'lon': np.NaN,
        'clean_address': '',
        'county': '',
        'status': '',
        'clean_street': '',
        'clean_city': '',
        'clean_state': '',
        'clean_zip': ''}

    # --- call google geocoder
    params = urllib.urlencode({'address': address, 'sensor': 'false'})
    if dry_run:
        return 'curl ' + repr('{}?{}'.format(URL, params))
    try:
        resp_obj = json.loads(requests.get(URL, params=params).text)
    except:
        out['status'] = "cant_reach_google"
        return out

    # --- return if bad status
    if resp_obj['status'] != 'OK':
        out['status'] = 'unexpected_google_status'
        return out

    # --- return if no results found
    res_list = resp_obj.get('results', [])
    if not res_list:
        out['status'] = 'no_google_results'
        return out

    # --- try pulling out google info
    try:
        # --- get the lat/lon
        geom = res_list[0]['geometry']
        out['lat'] = float(geom['location']['lat'])
        out['lon'] = float(geom['location']['lng'])

        # --- if geom has bounds, then this is a region, not a point
        if 'bounds' in geom:
            # --- store the bounding box
            out['lat_min'] = geom['bounds']['southwest']['lat']
            out['lat_max'] = geom['bounds']['northeast']['lat']
            out['lon_min'] = geom['bounds']['southwest']['lat']
            out['lon_max'] = geom['bounds']['northeast']['lat']
            out['formatted_address'] = res_list[0]['formatted_address']
            out['status'] = 'ok'

            # --- if no  street address return what you've got so far
            got
            if 'street_address' not in res_list[0]['types']:
                return out

        # --- parse the components of the street address
        ad_list = res_list[0]['address_components']
        ad_dict = {}
        for ad in ad_list:
            key = '__'.join(ad['types'])
            val = ad['short_name']
            ad_dict[key] = val

        # --- create clean address components
        out['clean_street'] = '{} {}'.format(
            ad_dict['street_number'],
            ad_dict['route']).upper()
        out['clean_city'] = ad_dict['locality__political'].upper()
        out['clean_state'] = ad_dict[
            'administrative_area_level_1__political'].upper()
        out['clean_zip'] = ad_dict['postal_code']

        # --- create clean address
        out['clean_address'] = '{} {}, {} {} {}'.format(
            ad_dict['street_number'],
            ad_dict['route'],
            ad_dict['locality__political'],
            ad_dict['administrative_area_level_1__political'],
            ad_dict['postal_code']).upper()

        # --- add the county
        out['county'] = ad_dict[
            'administrative_area_level_2__political'].upper()
    except:
        out['status'] = 'parsing_problem'
        return out

    out['status'] = 'ok'
    return out
