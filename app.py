import sys
import requests
import json
import os

from pymongo import MongoClient

class merakiapi:
    isStage = True
    isProduction = False

    #def __init__(self, isStage: bool):
    #    if isStage:
    #        #検証用
    #        self.base_url = 'https://api.meraki.com'
    #        self.apikey = 'b4c81b63e7712da44f79b80cb9164759f5e368ff'
    #        print("pymeraki stage")
    #    else:
    #        self.base_url = 'https://api.meraki.com'
    #        self.apikey = 'b4c81b63e7712da44f79b80cb9164759f5e368ff'
    #        print("pymeraki production")
	
    def __init__(self, isStage: bool, APIKey: str):
        if isStage:
            #検証用
            self.base_url = 'https://api.meraki.com'
            self.apikey = APIKey
            print("pymeraki stage")
        else:
            self.base_url = 'https://api.meraki.com'
            self.apikey = APIKey
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

def main():
    print('====== Enviromnents ======')
    print(os.environ.get('OPENSHIFT_MONGODB_DB_URL'))
    print(os.environ.get('MONGO_URL'))
    print(os.environ.get('DATABASE_SERVICE_NAME'))
    mongoServiceName = os.environ.get('DATABASE_SERVICE_NAME').upper()
    mongoHost = os.environ.get(mongoServiceName + '_SERVICE_HOST')
    mongoPort = os.environ.get(mongoServiceName + '_SERVICE_PORT')
    mongoDatabase = os.environ.get(mongoServiceName + '_DATABASE')
    mongoPassword = os.environ.get(mongoServiceName + '_PASSWORD')
    mongoUser = os.environ.get(mongoServiceName + '_USER')
    mongoURLLabel = mongoURL = 'mongodb://'
    mongoURL += mongoUser + ':' + mongoPassword + '@'
    mongoURLLabel += mongoHost + ':' + mongoPort + '/' + mongoDatabase
    mongoURL += mongoHost + ':' +  mongoPort + '/' + mongoDatabase

    print(mongoURL)
    print(mongoURLLabel)
    print('====== 1============ ======')

    client = MongoClient(mongoURL)
    print(client[mongoDatabase])
    #for database_name in client.database_names():
    #    print(database_name)
    db = client[mongoDatabase]
    for collection_name in db.list_collection_names():
        print(collection_name)
    print('====== 2============ ======')
    col = db['customers']
    print(col.find_one())
    print('====== 3============ ======')
    for doc in col.find():
        print(doc['Name'])
        endPoint = '/api/v0/organizations'
        mapi = merakiapi(False, doc['APIKey'])
        res = mapi.get('/api/v0/organizations', {})
        if res.status_code != 200:
            # エラーだった場合
            print('error : ' + str(res.status_code))
            print('error : ' + str(res.status_code), file=sys.stderr)
            print(res.json())
            sys.exit(1)
        else:
            # 結果の出力
            print(res.json())
        
        orgcolname = 'organizations_' + str(doc['customerid'])
        print('orgcolname:' + orgcolname)
        orgcol = db[orgcolname]
        orgcol.delete_many()
        #orgcol.insert_many(res.json())

        sys.exit(1)

        orgs = res.json()

        for org in orgs:
            print(org['id'])
            res2 = mapi.get('/api/v1/organizations/' + org['id'] + '/appliance/security/events', {})
            if res2.status_code == 200:
                # 結果の出力
                print(res2.json())
            elif res2.status_code == 403:
                print('No Data : organization:' + org['id'] + ' status:' + str(res2.status_code))
                print(res2.json())
            elif res2.status_code == 404:
                print('Forbidden : organization:' + org['id'] + ' status:' + str(res2.status_code))
                print(res2.json())
            else:
                # エラーだった場合
                print('Error Code:  organization:' + org['id'] + ' status:' + str(res2.status_code))
                print(res2.json())
                #sys.exit(1)

    print('====== 4============ ======')
    





if __name__ == "__main__":
    main()
