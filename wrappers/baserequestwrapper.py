import json
import requests

class BaseRequestWrapper:
    URL = "https://weightxreps.net/wxr-server-2/graphql"
    query = None
    raw = None

    def __init__(self) -> None:
        if self.query == None:
            raise NotImplementedError("Subclasses must define 'query' attribute.") 

        self.data = None

    def get(self):
        r = requests.post(self.URL, json=self.query)
        r.raise_for_status()
        self.raw = r.text
        self.data = json.loads(r.text)['data']
        self.parse()

    def parse(self):
        raise NotImplementedError