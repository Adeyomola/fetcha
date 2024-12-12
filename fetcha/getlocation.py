from flask import Flask, request
import requests

app = Flask(__name__)

class GetLocation:
    def __init__(self) -> None:
        pass

    def get_location():
        xff =  request.headers.getlist("X-Forwarded-For")
        if xff:
            ip = xff[0].split(",")[0]
        else:
            ip = request.remote_addr

        ip_info = requests.get(f'https://ipinfo.io/{ip}/json')
        data = ip_info.json()
        location = data['country']
        
        return location
