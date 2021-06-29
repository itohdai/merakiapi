#!/usr/bin/env python
# -*- coding: utf-8 -*-
import requests
import json

class mapi:
    isStage = True
    isProduction = False

    def __init__(self, isStage: bool):
        if isStage:
            #検証用
            self.base_url = 'https://api.meraki.com'
            self.apikey = 'b4c81b63e7712da44f79b80cb9164759f5e368ff'
            print("pymeraki stage")
        else:
            self.base_url = 'https://api.meraki.com'
            self.apikey = 'b4c81b63e7712da44f79b80cb9164759f5e368ff'
            print("pymeraki production")
	
    def get(self, endpoint: str, param: dict):
        response = requests.get(
            self.base_url + endpoint,
            params = param,
            headers={'X-Cisco-Meraki-API-Key': self.apikey,
                'Content-Type': 'application/json'})
        return response
	
    def delete(self, endpoint: str, param: dict):
        response = requests.delete(
            self.base_url + endpoint,
            params = param,
            headers={'X-Cisco-Meraki-API-Key': self.apikey,
                'Content-Type': 'application/json'})
        return response
	
    def put(self, endpoint: str, param: dict):
        response = requests.put(
            self.base_url + endpoint,
            params = param,
            headers={'X-Cisco-Meraki-API-Key': self.apikey,
                'Content-Type': 'application/json'})
        return response

    def post(self, endpoint: str, param: dict):
        response = requests.post(
            self.base_url + endpoint,
            headers={'X-Cisco-Meraki-API-Key': self.apikey,
                'Content-Type': 'application/json'},
            data=json.dumps(param)
        )
        return response

