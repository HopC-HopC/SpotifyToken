"""
Implementation of the Token class for managing Spotify developer tokens. 
Created for education; A Level Computer Science teaching.

This class provides functionality for acquiring, storing, and verifying Spotify
developer tokens. The token is stored in a text file, and at scale, exploring
databases for production code is recommended.

Usage:
1. Enter the Spotify client ID and secret from the developer console. Store
   sensitive information in a secure environment (e.g., .env) for production.
2. Create an instance of the Token class to manage the Spotify token.
3. The class will attempt to load an existing saved token, making a new request
   only if the token is missing or expired.

Attributes:
- CLIENT_ID (str): Spotify developer client ID.
- CLIENT_SECRET (str): Spotify developer client secret.

Methods:
- __init__(): Initializes the Token class, loading an existing token if available,
  and updating it if necessary.
- get_token(): Sends a request to Spotify to obtain a new token.
- save_token(): Saves the token and its expiration time to a text file.
- load_token(): Loads the token and its expiration time from the text file.
- token(): Returns the current Spotify token.
- time(): Returns the expiration time of the current token.

Example Usage:
```python
token = Token()
print(token.token())  # Access your current Spotify token
"""

import requests, datetime

CLIENT_ID = '' 
CLIENT_SECRET = ''

class Token:
    # Token class will try to load an existing saved token rather than
    # send unnecessary requests; at scale this would improve performance
    def __init__(self):
        self.__token = None
        self.__time = None
        self.load_token()
        try:
            if self.__time + datetime.timedelta(hours=1) < datetime.datetime.now():
                # token out of time; update
                print('Token out of time')
                self.get_token()
            else:
                print('Token up to date')

        except TypeError:
            # token time is not a datetime object; update
            print('Token time format incorrect')
            self.get_token()
        self.save_token()

    def get_token(self):
        endpoint = "https://accounts.spotify.com/api/token"
        headers = {"Content-Type": "application/x-www-form-urlencoded"}
        body = {
                "grant_type": "client_credentials",
                "client_id": CLIENT_ID,
                "client_secret": CLIENT_SECRET
            }
        response = requests.post(endpoint, headers=headers, data=body)
        self.__token = response.json()['access_token']
        self.__time = datetime.datetime.now()
        self.save_token()

    def save_token(self):
        details = self.__token + ',' + self.__time.strftime("%d-%b-%Y (%H:%M:%S.%f)")
        with open('token.txt', 'w') as file:
            file.write(details)

    def load_token(self):
        try:
            with open('token.txt', 'r') as file:
                result = file.read()
                result = result.strip().split(',')
                self.__token = result[0]
                self.__time = datetime.datetime.strptime(result[1], "%d-%b-%Y (%H:%M:%S.%f)")
        except FileNotFoundError:
            # no token file saved
            print('File not found')
            self.get_token()
        except (ValueError, IndexError):
            # token file corrupted
            print('File corrupt')
            self.get_token()

    def token(self):
        return self.__token

    def time(self):
        return self.__time


token = Token()

print(token.token()) # access your token

