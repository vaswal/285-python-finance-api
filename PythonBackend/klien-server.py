#!/usr/bin/env python3

from http.server import BaseHTTPRequestHandler, HTTPServer
from json import dumps
import json
import yfinance as yf
import pytz
from datetime import datetime, timezone

""" The HTTP request handler """
class RequestHandler(BaseHTTPRequestHandler):

  def _send_cors_headers(self):
      """ Sets headers required for CORS """
      self.send_header("Access-Control-Allow-Origin", "*")
      self.send_header("Access-Control-Allow-Methods", "GET,POST,OPTIONS")
      self.send_header("Access-Control-Allow-Headers", "x-api-key,Content-Type")

  def send_dict_response(self, d):
      """ Sends a dictionary (JSON) back to the client """
      self.wfile.write(bytes(dumps(d), "utf8"))

  def do_OPTIONS(self):
      self.send_response(200)
      self._send_cors_headers()
      self.end_headers()

  def do_GET(self):
      self.send_response(200)
      self._send_cors_headers()
      self.end_headers()

      response = {}
      response["status"] = "GET OK"
      self.send_dict_response(response)

  def do_POST(self):
      self.send_response(200)
      self._send_cors_headers()
      self.send_header("Content-Type", "application/json")
      self.end_headers()

      dataLength = int(self.headers["Content-Length"])
      data = self.rfile.read(dataLength)

      print(data)
      content = json.loads(data)
      response = {}

      try:
          ticker = content["ticker"]

          utc_dt = datetime.now(timezone.utc)
          PST = pytz.timezone('US/Pacific')
          print("{} PST".format(utc_dt.astimezone(PST)))

          stock = yf.Ticker(ticker.upper())
          print("stock")
          print(stock)

          # get stock info

          stock_info = stock.info
          name = stock_info["longName"]
          stock_price = stock_info["regularMarketPrice"]

          print("name: " + name)

          # get historical market data
          hist = stock.history(period="1d")

          print("hist")
          print(hist)
          open_price = None
          close_price = None

          for index, row in hist.iterrows():
              open_price = row['Open']
              close_price = row['Close']

          value_change = close_price - open_price
          percent_change = (value_change / open_price) * 100

          print("value_change: ", str('%.2f' % value_change))
          print("percent_change: ", str('%.2f' % percent_change))


          response["status"] = "POST OK"
          response["ans"] = "{} PST".format(utc_dt.astimezone(PST)) + "\n\n" + \
                            name + "\n\n" + \
                            "{} {} {}".format(stock_price, ('%.2f' % value_change), ('%.2f' % percent_change))
          response["code"] = "200"
      except ValueError as value_error:
          print(value_error.__doc__)
          print(type(value_error).__name__)
          response["code"] = "406"
          response["message"] = "Invalid ticker, please enter valid ticker"
      except ConnectionError as connection_error:
          print(connection_error.__doc__)
          print(type(connection_error).__name__)
          response["code"] = "500"
          response["message"] = "Network error, please check internet connection"
      except IndexError as index_error:
          print(index_error.__doc__)
          print(type(index_error).__name__)
          response["code"] = "406"
          response["message"] = "Invalid ticker, please enter valid ticker"
      except KeyError as key_error:
          print(key_error.__doc__)
          print(type(key_error).__name__)
          response["code"] = "406"
          response["message"] = "Invalid ticker, please enter valid ticker"
      except Exception as e:
          print(e.__doc__)
          print(type(e).__name__)
          self.send_dict_response("ERROR")
      finally:
        self.send_dict_response(response)





print("Starting server")
#httpd = HTTPServer(("ec2-34-217-19-29.us-west-2.compute.amazonaws.com", 8080), RequestHandler)
httpd = HTTPServer(("localhost", 7070), RequestHandler)
print("Hosting server on port 7070")
httpd.serve_forever()