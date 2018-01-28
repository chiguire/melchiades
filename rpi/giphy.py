import time
import giphy_client
from giphy_client.rest import ApiException
from pprint import pprint

def read_giphy_api_key():
    txt = open("../giphy_key.txt")
    key = txt.read().strip()
    return key

def giphy_translate(t):
    # create an instance of the API class
    api_instance = giphy_client.DefaultApi()
    api_key = read_giphy_api_key() # str | Giphy API Key.

    try: 
        # Translate Endpoint
        api_response = api_instance.gifs_translate_get(api_key, t)
    except ApiException as e:
        print("Exception when calling DefaultApi->gifs_translate_get: %s\n" % e)
        return None

    #pprint(api_response)
    try:
        data = api_response.data
        images = data.images
        original = images.original
        url = original.url
    except:
        return None
    return url
