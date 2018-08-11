import hmac
import base64
import requests
import json
import datetime
import time


api_key = ''
secret_key = ''
passphrase = ''


CONTENT_TYPE = 'Content-Type'
OK_ACCESS_KEY = 'OK-ACCESS-KEY'
OK_ACCESS_SIGN = 'OK-ACCESS-SIGN'
OK_ACCESS_TIMESTAMP = 'OK-ACCESS-TIMESTAMP'
OK_ACCESS_PASSPHRASE = 'OK-ACCESS-PASSPHRASE'
APPLICATION_JSON = 'application/json'  

#timestamp = datetime.datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S')+'.000Z'

#exit(0)
########################################################################
class Oktop:
    """"""
    def __init__(self):
        """Constructor"""
        self.base_url = 'https://www.ok.top'
        self.passphrase = passphrase
        self.api_key = api_key
        self.secret_key = secret_key            

    def timestamp(self):
        """"""
        return datetime.datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S')+'.000Z'        
    
    # signature
    def signature(self, method, request_path, body, secret_key):
        if str(body) == '{}' or str(body) == 'None':
            body = ''
        message = self.timestamp() + str.upper(method) + request_path + str(body)
        mac = hmac.new(bytes(secret_key, encoding='utf8'), bytes(message, encoding='utf-8'), digestmod='sha256')
        d = mac.digest()
        return base64.b64encode(d)    
    
    # set request header
    def get_header(self,api_key, sign, passphrase):
        header = dict()
        header[CONTENT_TYPE] = APPLICATION_JSON
        header[OK_ACCESS_KEY] = api_key
        header[OK_ACCESS_SIGN] = sign
        header[OK_ACCESS_TIMESTAMP] = self.timestamp()
        header[OK_ACCESS_PASSPHRASE] = passphrase
        return header    
    
    def parse_params_to_str(self,params):
        url = '?'
        for key, value in params.items():
            url = url + str(key) + '=' + str(value) + '&'    
        return url[0:-1]    
    
    def _post(self,request_path,data):
        """"""
        url = self.base_url + request_path + self.parse_params_to_str(data)
        header = self.get_header(self.api_key, self.signature( 'POST', request_path,data,self.secret_key), self.passphrase)
        body = json.dumps(data)
        return requests.post(url,json=body,headers=header,timeout=3)
    
    #----------------------------------------------------------------------
    def _get(self,request_path,params):
        """"""
        header = self.get_header(self.api_key, self.signature( 'GET', request_path,params,self.secret_key), self.passphrase)
        url = self.base_url + request_path
        return requests.get(url, headers=header,timeout=3)
    
    #----------------------------------------------------------------------
    def getCurrencies(self):
        """"""
        request_path = '/api/account/v3/currencies'
        params = ''
        response = self._get(request_path, params)
        return response.json()
    
    def getWallet(self,currency=''):
        """"""
        request_path = ''
        if not currency:
            request_path = '/api/account/v3/wallet'
        else:
            request_path = '/api/account/v3/wallet/' + currency
        params = ''
        response = self._get(request_path, params)
        return response.json()  
    
    def getBook(self,product_id):
        request_path = '/api/spot/v3/products/'+product_id+'/book'
        params = ''
        response = self._get(request_path, params)
        return response.json()          
    
    def getAccounts(self,currency=''):
        request_path = ''
        if not currency:
            request_path = '/api/spot/v3/accounts'
        else:
            request_path = '/api/spot/v3/accounts/' + currency  
        params = ''
        response = self._get(request_path, params)
        return response.json()     
    
    def getProducts(self):
        request_path = '/api/spot/v3/products'
        params = ''
        response = self._get(request_path, params)
        return response.json()         
    
    def postOrders(self,side='buy',product_id='BTC-USDT',size = '1',price='10',client_oid=''):
        request_path = '/api/spot/v3/orders'
        data = {'type':'limit','side':side,'product_id':product_id,'size':size,'client_oid':client_oid,'price':'0','funds':'','system_type':'1'}
        response = self._post(request_path, data)
        return response.json()          
        
        
if __name__ == "__main__":
    oktop = Oktop()
    #print(oktop.getCurrencies())
    #print(oktop.getWallet('LTC'))
    #print(oktop.getAccounts())
    print(oktop.getBook('BTC-USDT'))
    #print(oktop.getProducts())
    #print(oktop.postOrders(product_id='DASH-BTC'))
 

    
