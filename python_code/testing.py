import requests

# for x in range(1):
url = 'https://min-api.cryptocompare.com/data/histohour?fsym=ETH&tsym=USD&limit=24'
response = requests.post(url, data=data)





# import urllib.request, urllib.parse, urllib.error
# # from bs4 import BeautifulSoup
# # import re
# import ssl
#
# ctx = ssl.create_default_context()
# ctx.check_hostname = False
# ctx.verify_mode = ssl.CERT_NONE
#
# url = input('Enter -')
# if len(url) < 1 : url = 'https://min-api.cryptocompare.com/data/histohour?fsym=ETH&tsym=USD&limit=24'
# fhand = urllib.request.urlopen(url, context=ctx).read()
#
#



#
# import socket
#
# sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# sock.connect(('min-api.cryptocompare.com', 80))
# cmd = 'GET https://min-api.cryptocompare.com/data/histohour?fsym=ETH&tsym=USD&limit=24 HTTP/1.0\r\n\r\n'.encode()
# sock.send(cmd)
#
# transmitted = 0
#
# while True:
#     data = sock.recv(512)
#     if len(data) <1 : break
#     transmitted += len(data)
#     print(data.decode(), end = '')
#
# print(transmitted)
#
# sock.close()

# 86400 seconds in a day
# Need to offset by this number every time
# crypto trading is 24/7

#current price

# https://min-api.cryptocompare.com/data/price?fsym=ETH&tsyms=BTC,USD,EUR


#historical data

# https://min-api.cryptocompare.com/data/histohour?fsym=ETH&tsym=USD&limit=24
