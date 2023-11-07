from binance.client import Client
import pandas as pd
import talib
import datetime,time
import numpy as np
from tzlocal import get_localzone
import json
import playsound
import threading
import websocket
import os
import pyttsx3

# now supoorts macd, one symbol pair, binance, 

class MonitorSymbolWithWS:

    def __init__(self, api_key =  None, api_secret = None, 
            symbol =  'BTCUSDT', timeframe =  '5m',
            proxy_type = None, proxy_host = None, proxy_port  = None):

        self.api_key = api_key
        self.api_secret = api_secret 

        self.proxy_type = proxy_type
        self.proxy_host = proxy_host
        self.proxy_port = proxy_port

        self.symbol = symbol
        self.timeframe = timeframe

        if proxy_type == None: 
            self.client = Client(api_key, api_secret)
        else:
            proxies = {
                'http': proxy_type+'://'+ proxy_host + ':' + str(proxy_port),
                'https': proxy_type+'://'+ proxy_host + ':' + str(proxy_port)
            }   
            self.client = Client(api_key, api_secret,{'proxies': proxies})

    # Function to fetch historical OHLCV data
    def fetch_binance_futures_data( self, symbol: str, timeframe: str, limit:int = 500):
        klines = self.client.futures_klines(symbol=symbol, interval=timeframe, limit=limit)
        
        df = pd.DataFrame(klines, columns=['timestamp', 'o', 'h', 'l', 'c', 'v', 't', 'q', 'n','V','Q','T'] )
        
        df['timestamp'] = pd.to_datetime(df['t'], unit='ms')
        df.set_index('timestamp', inplace=True)

        return df

    #get the first symbol of the symbol pair, i.e. get BTC from BTCUSDT
    def getSymbol1(self):
        if self.symbol.endswith("USDT"):
            symbol = self.symbol[:-4]
        else:
            symbol = self.symbol
        return symbol

    def checkMacdCondition(self,m,s):
        res = ''

        if m.iloc[-1] < 0 and m.iloc[-1] >= m.iloc[-2] and m.iloc[-1]>= s.iloc[-1]:
            playsound.playsound(os.path.join(os.path.dirname(__file__), "zhangu.mp3"))
            res = res + 'macd Underwater GOLDEN fork'

        if m.iloc[-1] > 0 and m.iloc[-1] <= m.iloc[-2] and m.iloc[-1] <= s.iloc[-1] :
            playsound.playsound(os.path.join(os.path.dirname(__file__), "mingjin.mp3"))
            res = res + "macd water DEAD fork"

        return res 
            
    # Define the callback function for WebSocket data
    def on_message(self,ws,msg):
        historical_data = self._historical_data
        data = json.loads(msg)
        kline = data['k']
        print(".",end="",flush=True)

        if kline['x'] :
            #get a closed kline
            print("#",end="",flush=True)

            #Avoid excessive data volume over time. 10,000 is enough. 
            if len(historical_data) > 20000 :
                historical_data = historical_data.tail(10000)

            timestamp = pd.to_datetime(kline['T'], unit='ms')

            #the kline['T'] is close time. but histotical_data['t'] is closed time. open time is not used here. too strange... now do not use T, only store open time.
            historical_data.loc[timestamp] = {'o':kline['o'], 'h': kline['h'], 'l': kline['l'], 'c': float(kline['c']), 'v': kline['v'], 't': kline['T'], 'q': kline['q'], 'n': kline['n'], 'V': kline['V'],'Q': kline['Q'],'T': kline['t']}


            macd, signal, _ = talib.MACD( historical_data['c'].astype(float) , fastperiod=12, slowperiod=26, signalperiod=9)

            historical_data['macd'] = macd
            historical_data['signal']= signal

            res = self.checkMacdCondition(historical_data['macd'],historical_data['signal'] )

            if res != '':
                engine = pyttsx3.init()
                engine.say(self.getSymbol1())
                engine.runAndWait()
                print( "\n!!!:",self.symbol," ",self.timeframe, " ",  res ," \a ", datetime.datetime.fromtimestamp(float(historical_data['t'].iloc[-1])/1000)," ", historical_data['c'].iloc[-1],
                    " macd:", "{:.2f}".format(historical_data['macd'].iloc[-1]), " signal:", "{:.2f}".format(historical_data['signal'].iloc[-1]) )

            self._historical_data = historical_data

    def on_open(self,ws):
        print('\nopened connection for ', self.symbol, ' ', self.timeframe, ' at ', datetime.datetime.fromtimestamp(time.time()))

    def on_error(self,ws,err):
        print(err)

    def on_close(self,ws,status,msg) :
        print(f"\nclosed connection {msg}", self.sybol,' ',self.timeframe,' at ', tdatetime.datetime.fromtimestamp(time.time()))

# Subscribe to the WebSocket stream
    def start(self):
        historical_data = self.fetch_binance_futures_data( symbol=self.symbol, timeframe = self.timeframe, limit=500)
        historical_data['macd'] = None
        historical_data['signal'] = None

        self._historical_data = historical_data

        ws = websocket.WebSocketApp(f'wss://fstream.binance.com/ws/{self.symbol.lower()}@kline_{self.timeframe}', on_open=self.on_open, on_close=self.on_close, on_message=self.on_message, on_error=self.on_error)
        if self.proxy_type == None:
            ws.run_forever()
        else:
            ws.run_forever(proxy_type='socks5h',http_proxy_host="127.0.0.1", http_proxy_port='12345')

        print('starting ',self.symbol,' ', self.timeframe)

