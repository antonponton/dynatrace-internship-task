from http.server import BaseHTTPRequestHandler, HTTPServer
import urllib.request
import json
import re
from enum import Enum

hostname = "localhost"
serverport = 8000

class OPERATION(str, Enum):
    GET_AVERAGE_EXCHANGE_RATE = 1
    GET_MAX_MIN_EXCHANGE_RATE = 2
    GET_MAJOR_DIFFERENCE = 3
    UNKWONW = 4

def getOperationType(url):
    if re.findall("[a]+/(\w{3}/\d{4}\-(0[1-9]|1[012])\-(0[1-9]|[12][0-9]|3[01])/)", url):
        operation_type = OPERATION.GET_AVERAGE_EXCHANGE_RATE
        return operation_type
    elif re.findall("[a]+/(\w{3}/last/[0-9]|[1-9][0-9]|1[0-9][0-9]|2[0-4][0-9]|25[0-5])", url):
        operation_type = OPERATION.GET_MAX_MIN_EXCHANGE_RATE
        return operation_type
    elif re.findall("[c]+/(\w{3}/last/[0-9]|[1-9][0-9]|1[0-9][0-9]|2[0-4][0-9]|25[0-5])", url):
        operation_type = OPERATION.GET_MAJOR_DIFFERENCE
        return operation_type
    else:
        operation_type = OPERATION.UNKWONW
        return operation_type

class MyServer(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("content-type", "text/html")
        self.end_headers()

        serviceurl = "http://api.nbp.pl/api/"
        url = serviceurl + self.path

        try:
            datahandle = urllib.request.urlopen(url)
        except Exception as exc :
            print("Error:", exc)
            self.wfile.write(bytes(str(exc), "utf-8"))
            return
        

        data = datahandle.read().decode()

        js = json.loads(data)

        operation_type = getOperationType(url)

        if operation_type == OPERATION.GET_AVERAGE_EXCHANGE_RATE:
            currency = js["currency"]
            mid = js["rates"][0]["mid"]

            msg = "Average exchange rate for " + currency + " : " + str(mid)
            print(msg)
            self.wfile.write(bytes(msg, "utf-8"))

        elif operation_type == OPERATION.GET_MAX_MIN_EXCHANGE_RATE:
            rates = js["rates"]
            mids = []
            for i in rates:
                mids.append(i["mid"])
            
            msg = "Max average exchange rate: " + str(max(mids)) + " Min average exchange rate: " + str(min(mids))
            print(msg)
            self.wfile.write(bytes(msg, "utf-8"))
        
        elif operation_type == OPERATION.GET_MAJOR_DIFFERENCE:
            differences = []
            rates = js["rates"]
            for rate in rates:
                differences.append(abs((rate["bid"]-rate["ask"])))
            msg = "Major difference between the buy and the ask rate: " + str(max(differences))
            print(msg)
            self.wfile.write(bytes(msg, "utf-8"))

        elif operation_type == OPERATION.UNKWONW:
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