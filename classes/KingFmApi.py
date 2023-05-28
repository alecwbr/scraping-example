import requests
from typing import List, Dict

class KingFmApi:
    """Defines a class for interacting with the KingFM private API"""

    def __init__(self):
        self.__url = "https://kingfm.com/rest/carbon/api/nowplaying/playertype/wo"
        self.__http_method = "get"
        self.__api_dict = self.__get_json_as_dict()

        self.__playlist_data = self.__api_dict['widgets']['now-playing']['dataDetails']['wo']
        self.tracks: List[Dict[str, str]] = self.__playlist_data['track']
        self.fetched_songs_num = self.__playlist_data['fetchedSongs']
    
    def __get_json_as_dict(self):
        # Returns a dictionary of the json-encoded response, if any
        response = requests.request(self.__http_method, self.__url)
        return response.json()
