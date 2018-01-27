#!/usr/bin/env python3

import time
import giphy_client
from giphy_client.rest import ApiException
from pprint import pprint

def read_giphy_api_key():
    txt = open("../../giphy_key.txt")
    key = txt.read().strip()
    return key

# create an instance of the API class
api_instance = giphy_client.DefaultApi()
api_key = read_giphy_api_key() # str | Giphy API Key.
q = 'Who will I marry in the future?' # str | Search query term or prhase.

try: 
    # Translate Endpoint
    api_response = api_instance.gifs_translate_get(api_key, q)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling DefaultApi->gifs_translate_get: %s\n" % e)

