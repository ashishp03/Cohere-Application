import requests
from requests.exceptions import RequestException, JSONDecodeError

class MLBackend:

    def __init__(self, api_key):
        self.api_key = api_key
    def replace_spaces_with_pluses(self, sample):
        """Returns a string with each space being replaced with a plus so the email hyperlink can be formatted properly"""
        return sample.replace(' ', '+').replace('\n', '+')
