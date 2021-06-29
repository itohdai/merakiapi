#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
from merakiapi import mapi

def main():
    print('test')
    endPoint = '/api/v0/organizations'

    api = mapi(mapi.isProduction)
    res = api.get('/api/v0/organizations', {})
    if res.status_code != 200:
        # エラーだった場合
        print('error : ' + str(res.status_code))
        print('error : ' + str(res.status_code), file=sys.stderr)
        print(res.json())
        #sys.exit(1)
    else:
        # 結果の出力
        print(res.json())


main()

