# -*- coding: UTF-8 -*-
__author__ = "YU CHU DENG"

import sys
import time
"""
# 第一步:
#  停車位資訊顯示  轉成網頁
# http://127.0.0.1:8888/?action=parkingall 

# 第二步:
# 顯示新竹市停車位資料 

# 第三步:
# 做一個 html 網頁, 點選後 a  link  顯示 全部的區域
# HTTP_paking

# 第四步:
# 點選 link ,  顯示尚有車位的停車場
# http://127.0.0.1:8888/?action=parking&a=car
# http://127.0.0.1:8888/?action=parking&a=scooter

# HTML + Javascript + PHP/ASP + Python

"""

import socketserver as socketserver
import http.server
from http.server import SimpleHTTPRequestHandler as RequestHandler
from urllib.parse import urlparse,unquote
import subprocess

class MyHandler(RequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html; charset=utf-8')
        self.end_headers()

        html = '我收到資料 '
        print(self.path)                   # /?name=powenko&passsword=abc
        query = urlparse(self.path).query  #  'name=powenko&passsword=abc'
        if query!="":
           dict2 = dict(qc.split("=") for qc in query.split("&"))
           try:
                action = dict2["action"].lower()   #這個程式的a ; "a"為網址上的a
                #print(action)

                if action=="parkingall":
                    # html ="顯示新竹市停車位所有資料"
                    html = subprocess.check_output(['python', '新竹市剩餘停車位_parkingall.py'])
                    self.wfile.write(html)
                    return

                a = dict2["a"].lower()
                if action=="parking":
                    # html ="顯示新竹市汽機車剩餘停車位"
                    html = subprocess.check_output(['python', '新竹市剩餘停車位_parking.py',a])
                    # python 07HTTP_JSON-openData-UbikeBysarea.py  龜山區
                    self.wfile.write(html)
                    return

           except:
                html=html+"沒有資料"
        html = html.encode("utf-8")
        self.wfile.write(html)


port = 8888

print('Server listening on port %s' % port)
socketserver.TCPServer.allow_reuse_address = True
httpd = socketserver.TCPServer(('0.0.0.0', port), MyHandler)
try:
    httpd.serve_forever()
except:
    print("Closing the server.")
    httpd.server_close()
    raise
