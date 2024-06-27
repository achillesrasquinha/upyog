import upyog as upy

class SalesforceClient(upy.AsyncBaseClient):
    pass

class SuperSF(upy.SuperAsyncClient):
    client = SalesforceClient