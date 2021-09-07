import sys
import requests
import json
import os
import meraki

from pymongo import MongoClient

def main():
    print('====== Enviromnents ======')
    print(os.environ.get('OPENSHIFT_MONGODB_DB_URL'))
    print(os.environ.get('MONGO_URL'))
    print(os.environ.get('DATABASE_SERVICE_NAME'))

    mongoServiceName = os.environ.get('DATABASE_SERVICE_NAME').upper()

    print(os.environ.get(mongoServiceName + '_SERVICE_HOST'))
    print(os.environ.get(mongoServiceName + '_SERVICE_PORT'))
    print(os.environ.get(mongoServiceName + '_DATABASE'))
    print(os.environ.get(mongoServiceName + '_PASSWORD'))
    print(os.environ.get(mongoServiceName + '_USER'))

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

    client = MongoClient(mongoURL,
                        tls=True,
                        tlsCAFile='./MongoDB-Meraki.ca.crt'
                        )
    print(client[mongoDatabase])
#    for database_name in client.database_names():
#        print(database_name)
    db = client[mongoDatabase]
#    for collection_name in db.list_collection_names():
#        print(collection_name)
    print('====== 2============ ======')
    col = db['customers']
    print(col.find_one())
    print('====== 3============ ======')
    for doc in col.find():
        print(doc['Name'])
        #endPoint = '/api/v0/organizations'
        #mapi = merakiapi(False, doc['APIKey'])
        #res = mapi.get('/api/v0/organizations', {})
        #if res.status_code != 200:
        #    # エラーだった場合
        #    print('error : ' + str(res.status_code))
        #    print('error : ' + str(res.status_code), file=sys.stderr)
        #    print(res.json())
        #    sys.exit(1)
        #else:
        #    # 結果の出力
        #    print(res.json())
        dashboard = meraki.DashboardAPI(
            api_key = doc['APIKey'],
            output_log = False
        )
        res = dashboard.organizations.getOrganizations()
        print(res)

        orgcolname = 'organizations_' + str(doc['customerid'])
        print('orgcolname:' + orgcolname)
        orgcol = db[orgcolname]
        orgcol.delete_many({})
        orgcol.insert_many(res)

        for org in orgcol.find():
            #print(org['id'])
            #res2 = mapi.get('/api/v1/organizations/' + str(org['id']) + '/appliance/security/events', {})
            try:
                res2 = dashboard.appliance.getOrganizationApplianceSecurityEvents(
                    str(org['id']), total_pages='all'
                )
            except:
                print('error: organizationid:' + str(org['id']))
            else:
                if(res2!=[]):
                    print(res2)
                    eventcolname = 'events_' + str(doc['customerid']) + '_' + str(org['id'])
                    print('eventcolname:' + eventcolname)
                    evcol = db[eventcolname]
                    for ev in res2:
                        #print(ev['ts'])
                        evcol.delete_many({'ts': ev['ts']})
                    evcol.insert_many(res2)


#            if res2.status_code == 200:
#                # 結果の出力
#                print(res2.json())
#                eventcolname = 'events_' + str(doc['customerid']) + '_' + str(org['id'])
#                print('eventcolname:' + eventcolname)
#                evcol = db[eventcolname]
#                if res2.json() != []:
#                    print(res2.links)
#                    for ev in res2.json():
#                        #print(ev['ts'])
#                        evcol.delete_many({'ts': ev['ts']})
#
#                    evcol.insert_many(res2.json())
#            elif res2.status_code == 403:
#                print('No Data : organization:' + org['id'] + ' status:' + str(res2.status_code))
#                print(res2.json())
#            elif res2.status_code == 404:
#                print('Forbidden : organization:' + org['id'] + ' status:' + str(res2.status_code))
#                print(res2.json())
#            else:
#                # エラーだった場合
#                print('Error Code:  organization:' + org['id'] + ' status:' + str(res2.status_code))
#                print(res2.json())
#                #sys.exit(1)

    print('====== 4============ ======')
    





if __name__ == "__main__":
    main()
