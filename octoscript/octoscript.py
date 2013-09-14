import sys
import urllib2
import json
import cookielib
import urllib
from MultipartPostHandler import MultipartPostHandler

cookies = cookielib.LWPCookieJar()
handlers = [
    urllib2.HTTPHandler(),
    urllib2.HTTPSHandler(),
    urllib2.HTTPCookieProcessor(cookies),
    MultipartPostHandler()
    ]
opener = urllib2.build_opener(*handlers)
ensure_api_enabled = 'Ensure that config.yaml has proper API configuration, for example:\napi:\n  enabled: true\n  key: ABC'

class Printer(object):
    def __init__(self, address, port=5000, username=None, password=None, apikey=None):
        self.address = str(address)
        self.port = int(port)

        self.username = username
        self.password = password
        #d=urllib2.urlopen("http://www.google.co.uk")
        #print 'cookies: ', [i[1] for i in d.headers if "Set-Cookie" in d.headers.keys()]
        #print 'cookies: ', dict(d.headers)['set-cookie']
        try:
            req=urllib2.Request('http://%s%s/ajax/login' % (self.address, '' if self.port == 80 else ':%s' % (self.port)), urllib.urlencode({'user': self.username, 'pass': self.password}), { 'User-Agent' : 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)' })
            d=opener.open(req)
            print 'COOKIES: ', cookies
        except:
            print 'Wrong username and/or password'
        #print 'login cookies: ', dict(d.headers)['set-cookie']
        self.apikey = apikey
        self.cookie = cookies
        #print 'cookie: ', self.cookie
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

    def update_cookie(self):
        try:
            req=urllib2.Request('http://%s%s/ajax/login' % (self.address, '' if self.port == 80 else ':%s' % (self.port)), urllib.urlencode({'user': self.username, 'pass': self.password}), { 'User-Agent' : 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)' })
            d=opener.open(req)
            print 'COOKIES: ', cookies
        except:
            print 'Wrong username and/or password'
        self.cookie = cookies

    def update_state(self):
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

    def connect(self, dev='AUTO', baud='AUTO'):
        req=urllib2.Request('http://%s%s/ajax/control/connection' % (self.address, '' if self.port == 80 else ':%s' % (self.port)), urllib.urlencode({'command': 'connect', 'port': dev, 'baudrate': baud}), { 'User-Agent' : 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)' })
        d=opener.open(req)
        
        return d.read()

    def disconnect(self):
        req=urllib2.Request('http://%s%s/ajax/control/connection' % (self.address, '' if self.port == 80 else ':%s' % (self.port)), urllib.urlencode({'command': 'disconnect'}), { 'User-Agent' : 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)' })
        d=opener.open(req)
        
        return d.read()

    def gcode(self, gcode):
        req=urllib2.Request('http://%s%s/ajax/control/command' % (self.address, '' if self.port == 80 else ':%s' % (self.port)), urllib.urlencode({'command': gcode}), { 'User-Agent' : 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)' })
        d=opener.open(req)
        
        return d.read()    

    def upload(self, filename):
        req=urllib2.Request('http://%s%s/ajax/gcodefiles/upload' % (self.address, '' if self.port == 80 else ':%s' % (self.port)),{'gcode_file': open(filename)}, { 'User-Agent' : 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)' })
        d=opener.open(req)
        
        return d.read()  

    def delete(self, filename):
        req=urllib2.Request('http://%s%s/ajax/gcodefiles/upload' % (self.address, '' if self.port == 80 else ':%s' % (self.port)), urllib.urlencode({'filename': filename}), { 'User-Agent' : 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)' })
        d=opener.open(req)
        
        return d.read() 

    def list(self):
        req=urllib2.Request('http://%s%s/ajax/gcodefiles' % (self.address, '' if self.port == 80 else ':%s' % (self.port)), None, { 'User-Agent' : 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)' })
        d=opener.open(req)
        
        return d.read()

    def print_file(self, filename):
        req=urllib2.Request('http://%s%s/ajax/gcodefiles/load' % (self.address, '' if self.port == 80 else ':%s' % (self.port)), urllib.urlencode({'filename': filename, 'print': 'true'}), { 'User-Agent' : 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)' })
        d=opener.open(req)
        
        return d.read()

    def load(self, filename):
        req=urllib2.Request('http://%s%s/ajax/gcodefiles/load' % (self.address, '' if self.port == 80 else ':%s' % (self.port)), urllib.urlencode({'filename': filename, 'print': 'false'}), { 'User-Agent' : 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)' })
        d=opener.open(req)
        
        return d.read()

    def start(self):
        req=urllib2.Request('http://%s%s/ajax/control/job' % (self.address, '' if self.port == 80 else ':%s' % (self.port)), urllib.urlencode({'command': 'start'}), { 'User-Agent' : 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)' })
        d=opener.open(req)
        
        return d.read()

    def cancel(self):
        req=urllib2.Request('http://%s%s/ajax/control/job' % (self.address, '' if self.port == 80 else ':%s' % (self.port)), urllib.urlencode({'command': 'cancel'}), { 'User-Agent' : 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)' })
        d=opener.open(req)
        
        return d.read()

    def pause(self):
        req=urllib2.Request('http://%s%s/ajax/control/job' % (self.address, '' if self.port == 80 else ':%s' % (self.port)), urllib.urlencode({'command': 'pause'}), { 'User-Agent' : 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)' })
        d=opener.open(req)
        
        return d.read()

def main(args):
    print len(args)
    args = args[1:]
    printer = Printer(*args)
    print printer
    print printer.connect()
    print printer.disconnect()
    print printer.gcode('')
    print printer.upload('test.gcode')
    print printer.list()

if __name__ == '__main__':
    main(sys.argv)
