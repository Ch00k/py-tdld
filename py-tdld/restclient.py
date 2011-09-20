from urllib2 import Request, urlopen
from urllib import urlencode, unquote_plus
import os
from time import time
from re import sub
import json
from hashlib import md5


USEREMAIL = 'me@ex.com'
USERPASSWORD = '123qwe'
APPID = 'py-tdld'
APPTOKEN = 'token'


class BaseClient():
    def __init__(self, useremail, userpassword):
        userid = self._get_userid(appid = APPID,
                                  apptoken = APPTOKEN,
                                  useremail = USEREMAIL,
                                  userpassword = USERPASSWORD)
        if os.path.exists(os.path.expanduser('~/.tdld/state')):
            if int(time()) - os.stat(os.path.expanduser('~/.tdld/state')).st_mtime > 14400:
                self._auth(userid = userid,
                           userpassword = USERPASSWORD,
                           appid = APPID,
                           apptoken = APPTOKEN)
        else:
            self._auth(userid = userid,
                       userpassword = USERPASSWORD,
                       appid = APPID,
                       apptoken = APPTOKEN)
            
    def _get_userid(self, appid, apptoken, useremail, userpassword):
        url_params = {
                      'appid': appid,
                      'email': useremail,
                      'pass': userpassword,
                      'sig': md5(useremail + apptoken).hexdigest()
                      }
        query_string = '?%s' % (urlencode(url_params))
        url = 'https://api.toodledo.com/2/account/lookup.php%s' % (query_string)
        print url
        try:
            request = Request(url = url)
            response = urlopen(request)
        except IOError, e:
            if hasattr(e, 'reason'):
                print 'We failed to reach a server.'
                print 'Reason: ', e.reason
            elif hasattr(e, 'code'):
                print 'The server couldn\'t fulfill the request.'
                print 'Error code: ', e.code
        else:        
             userid = json.loads(response.read())
        if 'errorCode' in userid:
            print 'Error occurred. Code %s: %s' % (userid['errorCode'], userid['errorDesc'])
        else:
            return userid['userid']        

    def _auth(self, userid, userpassword, appid, apptoken, vers=None, device=None, _os=None):
        url_params = {
                      'userid': userid,
                      'appid': appid,
                      'vers': vers if vers is not None else '',
                      'device': device if device is not None else '',
                      'os': _os if _os is not None else '',
                      'sig': md5(userid + apptoken).hexdigest()
                      }
        query_string = '?%s' % (urlencode(url_params))
        url = 'https://api.toodledo.com/2/account/token.php%s' % (query_string)
        try:
            request = Request(url = url)
            response = urlopen(request)
        except IOError, e:
            if hasattr(e, 'reason'):
                print 'We failed to reach a server.'
                print 'Reason: ', e.reason
            elif hasattr(e, 'code'):
                print 'The server couldn\'t fulfill the request.'
                print 'Error code: ', e.code
        else:        
             session_token = json.loads(response.read())
        if 'errorCode' in session_token:
            print 'Error occurred. Code %s: %s' % (session_token['errorCode'], session_token['errorDesc'])
        else:
            print session_token['token']
            key = md5(md5(userpassword).hexdigest() + apptoken + session_token['token']).hexdigest()
            print key
            if not os.path.exists(os.path.expanduser('~/.tdld')):
                os.makedirs(os.path.expanduser('~/.tdld'))
            statefile = open(os.path.expanduser('~/.tdld/state'), 'w')
            statefile.write(key)
        
    def _get_account_info(self):
        account_info, method = self.get(baseurl = 'http://api.toodledo.com/2/account/get.php', ssl = False)
        print account_info, method
        
        return account_info, method

    def get(self, baseurl, url_params=None, ssl=False):
        url_params = url_params or {}
        url_params['key'] = open(os.path.expanduser('~/.tdld/state')).read()
        query_string = '?%s' % (urlencode(url_params))
        if not ssl:
            url = '%s%s' % (baseurl, query_string)
        else:
            url = '%s%s' % (sub('http://', 'https://', baseurl), query_string)
        print url
        try:
            request = Request(url = url)
            response = urlopen(request)
        except IOError, e:
            if hasattr(e, 'reason'):
                print 'We failed to reach a server.'
                print 'Reason: ', e.reason
            elif hasattr(e, 'code'):
                print 'The server couldn\'t fulfill the request.'
                print 'Error code: ', e.code
        else:        
            return response.read(), request.get_method()
        
    def post(self, baseurl, body, ssl=False):
        if not ssl:
            url = baseurl
        else:
            url = sub('http://', 'https://', baseurl)
        print url
        key = {'key': open(os.path.expanduser('~/.tdld/state')).read()}
        data = sub(r'\'', '"', sub(r'\s', '', unquote_plus(urlencode(dict(key, **body)))))
        try:
            request = Request(url = url,
                              data = data)
            print request.get_data()
            response = urlopen(request)
        except IOError, e:
            if hasattr(e, 'reason'):
                print 'We failed to reach a server.'
                print 'Reason: ', e.reason
            elif hasattr(e, 'code'):
                print 'The server couldn\'t fulfill the request.'
                print 'Error code: ', e.code
        else:        
            return response.read(), request.get_method()
        
        
if __name__ == '__main__':
    
    #s, method = RESTClient().httprequest('http', 'toodledo.com', '/info', '', '')
    #print s, method
    
    s = BaseClient(USEREMAIL, USERPASSWORD)
    s._get_account_info()
    
    