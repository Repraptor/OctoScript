import sys
import urllib2
import json
import cookielib
import urllib

ensure_api_enabled = 'Ensure that config.yaml has proper API configuration, for example:\napi:\n  enabled: true\n  key: ABC'

class Printer(object):
    def __init__(self, address, port=5000, username=None, password=None, apikey=None):
        self.address = str(address)
        self.port = int(port)

        self.username = username
        self.password = password
        d=urllib2.urlopen("http://www.google.co.uk")
        #print 'cookies: ', [i[1] for i in d.headers if "Set-Cookie" in d.headers.keys()]
        print 'cookies: ', dict(d.headers)['set-cookie']
        try:
            req=urllib2.Request('http://%s%s/ajax/login' % (self.address, '' if self.port == 80 else ':%s' % (self.port)), urllib.urlencode({'user': self.username, 'pass': self.password}), { 'User-Agent' : 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)' })
            d=urllib2.urlopen(req)
        except:
            print 'Wrong username and/or password'
        print 'login cookies: ', dict(d.headers)['set-cookie']
        self.apikey = apikey
        self.cookie = dict(d.headers)['set-cookie']
        print 'cookie: ', self.cookie
        state_json = '{}'
        if self.apikey:
            try:
                state_json = urllib2.urlopen('http://%s%s/api/state?apikey=%s' % (self.address, '' if self.port == 80 else ':%s' % (self.port), self.apikey), timeout=2).read()
            except urllib2.HTTPError:
                print 'Invalid APIKey and/or API not enabled'
                print ensure_api_enabled
        else:
            try:
                state_json = urllib2.urlopen('http://%s%s/api/state' % (self.address, '' if self.port == 80 else ':%s' % (self.port)), timeout=2).read()
            except urllib2.HTTPError:
                print 'APIKey required and/or API not enabled'
                print ensure_api_enabled
        print state_json
        self.state = json.loads(state_json)
        
    def __repr__(self):
        return 'OctoPrint at http://%s%s' % (self.address, '' if self.port == 80 else ':%s' % (self.port))

    def update_state(self):
        pass

def main(args):
    print len(args)
    args = args[1:]
    printer = Printer(*args)
    print printer

if __name__ == '__main__':
    main(sys.argv)
