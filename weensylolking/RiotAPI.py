import Consts as Consts
import requests


class RiotAPI(object):
    def __init__(self, api_key, region=Consts.REGIONS['north_america']):
        self.api_key = api_key
        self.region = region

    def _request(self, api_url):
        args = {'api_key': self.api_key}

        response = requests.get(Consts.URL['base'].format(proxy=self.region, region=self.region, url=api_url),
                                params=args)
        #print response.url
        #print response.status_code
        if response.status_code == 200:
            return response.status_code, response.json()
        else:
            return response.status_code, 0

    def get_summoner_by_name(self, name):
        api_url = Consts.URL['summoner_by_name'].format(version=Consts.API_VERSIONS['summoner'], names=name)
        self.region = Consts.REGIONS['north_america']
        return self._request(api_url)

    def get_summoner_rank(self, id):
        api_url = Consts.URL['summoner_by_rank'].format(version=Consts.API_VERSIONS['league'], sumID=id)
        return self._request(api_url)
