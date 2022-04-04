from datetime import datetime
import json
from time import sleep
import requests
from random import randint
from settings import TOKEN

class Status:

    def __init__(self, emoji_name: str=None, text: str=None, expires_at: str=None) -> None:
        self.emoji_name = emoji_name
        self.text = text
        self.expires_at = expires_at
    
    @property
    def dict(self) -> dict:
        return self.__dict__
    
    def __str__(self) -> str:
        return str(self.__dict__)


class Status_changer:
    url = "https://discord.com/api/v9/users/@me/settings"
    headers = {
        "Content-Type": "application/json",
        "Authorization": None,
    }

    def __init__(self, token) -> None:
        self.headers["Authorization"] = token

    def gen_body(self, status: Status) -> str:
        args = {key: value for key, value in status.dict.items() if value is not None}

        body = {
            'custom_status': args or None
        }
        return json.dumps(body)

    def set_status(self, status: Status) -> requests.Response:
        body = self.gen_body(status)
        response = requests.patch(self.url, headers=self.headers, data=body)
        return response
    
    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.set_status(Status())

def ticker():
    text = "ооочеееень длииинная строка с очень много букаф. "
    looped = text * 2
    status_len = 20
    offset = 0

    with Status_changer(TOKEN) as session:
        while True:
            status = Status(text=looped[offset:offset+status_len])
            response = session.set_status(status)
            print(response.status_code)
            
            offset += 1
            if offset == len(text):
                offset = 0
            
            sleep(0.1)


def time_now():
    session = Status_changer(TOKEN)
    while True:
        now = datetime.now()
        text = str(now.ctime())
        status = Status(text=text)
        response = session.set_status(status)
        print(response.status_code)
        sleep(1)
    


def main():
    with Status_changer(TOKEN) as session:
        offset = 0
        while True:
            text = ''.join([chr(i+offset) for i in range(128)])

            status = Status(text=text)
            response = session.set_status(status)

            if response.status_code != 200:
                parsed = json.loads(response.text)
                pretty = json.dumps(parsed, indent=4)
                print(pretty)
                input()
            
            offset += 1



if __name__ == "__main__":
    ticker()
