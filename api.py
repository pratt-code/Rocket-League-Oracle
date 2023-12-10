import requests
import config

class ballchasing:
    def __init__(self):
        self.token = config.ballchasing_token
        self.header = {'Authorization': self.token}

    def ping(self):
        r = requests.get('https://ballchasing.com/api/', headers=self.header)
        r.raise_for_status()
        return r
    
    def get_replay(self, id):
        r = requests.get(f'https://ballchasing.com/api/replays/{id}', headers=self.header)
        r.raise_for_status()
        return r.json()
    
    def get_group(self, params):
        r = requests.get('https://ballchasing.com/api/replays', headers={'Authorization': config.ballchasing_token}, params=params)
        r.raise_for_status()
        return r.json()
    
    def get_with_link(self, link):
        r = requests.get(link, headers=self.header)
        r.raise_for_status()
        return r.json()

# Unused for now
class octanegg:
    def __init__(self):
        pass

    def ping(self):
        r = requests.get('https://zsr.octane.gg/')
        r.raise_for_status()
        return r

