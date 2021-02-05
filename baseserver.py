#!/usr/bin/env python3

import json
import logging
import time
from http.server import BaseHTTPRequestHandler, HTTPServer


# HTTPRequestHandler class
class testHTTPServer(BaseHTTPRequestHandler):

    # GET
    def do_GET(self):
        # Send response status code
        self.send_response(200)

        # Send headers
        self.send_header('Content-type','text/html')
        self.end_headers()

        # Send message back to client
        my_timedate = time.strftime('%H:%M %Z, %d %B %Y')
        message = '<h3>Hello world!</h3><p>{0}</p>'.format(my_timedate)
        # Write content as utf-8 data
        self.wfile.write(bytes(message, "utf8"))
        return

    # POST
    def do_POST(self):
        logging.warning('\n====== New message received! ======\n')
        headers = self.headers
        logging.warning('\n{0}'.format(headers))
        length = int(self.headers['Content-Length'])
        #post_data = str(self.rfile.read(length).decode('utf-8'))
        post_dict = json.loads(str(self.rfile.read(length).decode('utf-8')))
        #        logging.warning('\n{0}\n'.format(post_data))
        json_data = json.dumps(post_dict, sort_keys=True, indent=4)
        logging.warning('\n{0}\n'.format(json_data))
        msg_dict = json.loads(post_dict['Message'])
        msg_json = json.dumps(msg_dict, sort_keys=True, indent=4)
        logging.warning('\nMessage:\n{0}\n'.format(msg_json))
        logging.warning('\n====== End of message. ======\n')

        return

def run():
    print('\nstarting server...')

    # Server settings
    server_address = ('127.0.0.1', 3131)
    httpd = HTTPServer(server_address, testHTTPServer)
    print('running server...\n')
    httpd.serve_forever()


run()
