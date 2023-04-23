from http.server import BaseHTTPRequestHandler, HTTPServer
import urllib.request
import json
import re

hostname = "localhost"
serverport = 8000

class MyServer(BaseHTTPRequestHandler):
    def do_GET(self):

        self.send_response(200)
        self.send_header("content-type", "text/html")
        self.end_headers()

        # get an URL address
        serviceurl = "http://api.nbp.pl/api/"
        url = serviceurl + self.path

        # get data from API
        datahandle = urllib.request.urlopen(url)
        data = datahandle.read().decode()
        try:
            js = json.loads(data)
        except:
            js = None
        if not js:
            print(' Failure to retrieve ')
            print(data)
        
        # specify operation endpoint
        operation_1 = ''
        operation_2 = ''
        operation_3 = ''

        operation_1 = re.findall('[a]/(\w{3}/\d{4}\-(0[1-9]|1[012])\-(0[1-9]|[12][0-9]|3[01])/)', url)
        operation_2 = re.findall('[a]/(\w{3}/last/[0-9]|[1-9][0-9]|1[0-9][0-9]|2[0-4][0-9]|25[0-5])', url)
        operation_3 = re.findall('[c]/(\w{3}/last/[0-9]|[1-9][0-9]|1[0-9][0-9]|2[0-4][0-9]|25[0-5])', url)

        # perform operations
        if operation_1:
            currency = js['currency']
            mid = js['rates'][0]['mid']

            print("Average exchange rate for " + currency + " : " + str(mid))
            self.wfile.write(bytes("Average exchange rate for " + currency + " : " + str(mid), "utf-8"))

        elif operation_2:
            
            rates = js['rates']
            mids = []
            for i in rates:
                mids.append(i['mid'])
            print("Max average exchange rate: " + str(max(mids)) + " Min average exchange rate: " + str(min(mids)))
            self.wfile.write(bytes("Max average exchange rate: " + str(max(mids)) + " Min average exchange rate: " + str(min(mids)), "utf-8"))
        
        elif operation_3:
            differences = []
            rates = js['rates']
            for i in rates:
                differences.append(abs((i['bid']-i['ask'])))
            print("Major difference between the buy and the ask rate: " + str(max(differences)))
            self.wfile.write(bytes("Major difference between the buy and the ask rate: " + str(max(differences)), "utf-8"))

        else:
            print("Wrong URL")
            self.wfile.write(bytes("Wrong URL", "utf-8"))

webServer = HTTPServer((hostname, serverport), MyServer)
print("Server started at http://%s:%s" % (hostname, serverport))

try:
    webServer.serve_forever()
except KeyboardInterrupt:
    print("Exiting server")
except Exception as exc :
    print("Error: \n")
    print(exc)

webServer.server_close()
print("Server closed.")