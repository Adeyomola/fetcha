from flask import Flask, request
import requests

app = Flask(__name__)

class GetLocation:
    def __init__(self) -> None:
        pass

    def get_location():
        if request.headers.getlist("X-Forwarded-For"):
            ip = request.headers.getlist("X-Forwarded-For")[0]
        else:
            ip = request.remote_addr

        ip_info = requests.get(f'https://ipinfo.io/{ip}/json')
        data = ip_info.json()
        location = data.get('country', 'Unknown')
        
        return location
