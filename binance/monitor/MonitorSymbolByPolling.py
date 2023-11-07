from binance.client import Client
import pandas as pd
import talib
import numpy as np
import playsound,pytz
import datetime,time, threading
import os
from tzlocal import get_localzone
import pyttsx3

# Initialize the Binance client

# now supoorts macd, one symbol pair, binance, 
# it is better for timeframe >= 1h

class MonitorSymbolByPolling:
    toSeconds={ '1m': 60,
            '5m': 300,
            '15m': 900,
            '30m': 1800,
            '1h':3600,
            '4h':14400,
            '1d':86400 }

    def __init__(self, api_key =  None, api_secret = None, 
            symbol =  'BTCUSDT', timeframe =  '1h',
            proxy_type = None, proxy_host = None, proxy_port  = None):

        self.api_key = api_key
        self.api_secret = api_secret 

        self.proxy_type = proxy_type
        self.proxy_host = proxy_host
        self.proxy_port = proxy_port

        self.symbol = symbol
        self.timeframe = timeframe
        self.proxy_port = proxy_port
        
        self.engine = pyttsx4.init()
        # 'https': 'socks5h://127.0.0.1:12345'
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
        #print(type(df.iloc[-1]['timestamp']))

        df.set_index('timestamp', inplace=True)

        return df

    def checkMacdCondition(self,m,s):
        res = ''

        if m.iloc[-1] < 0 and m.iloc[-1] >= m.iloc[-2] and m.iloc[-1]>= s.iloc[-1]:
            playsound.playsound(os.path.join(os.path.dirname(__file__), 'zhangu.mp3'))
            res = res + 'macd Underwater GOLDEN fork'

        if m.iloc[-1] > 0 and m.iloc[-1] <= m.iloc[-2] and m.iloc[-1] <= s.iloc[-1] :
            playsound.playsound(os.path.join(os.path.dirname(__file__), 'mingjin.mp3'))
            res = res + "macd water DEAD fork"

        return res 
    #get the first symbol of the symbol pair, i.e. get BTC from BTCUSDT
    def getSymbol1(self):
        if self.symbol.endswith("USDT"):
            symbol = self.symbol[:-4]
        else:
            symbol = self.symbol
        return symbol

    # Define the callback function for WebSocket data
    def on_timer(self):
        historical_data = self._historical_data
        
        tdf = self.fetch_binance_futures_data( symbol=self.symbol, timeframe = self.timeframe, limit=500)
        historical_data = pd.concat([tdf, historical_data.loc[~historical_data.index.isin(tdf.index)]])
        #print(f"sorted ? {historical_data.index.is_monotonic_increasing}")
        historical_data = historical_data.sort_index(ascending=True)
        print(".",end="",flush=True)
        if len(historical_data) > 20000 :
            historical_data = historical_data.tail(10000)

        macd, signal, _ = talib.MACD( historical_data['c'].astype(float) , fastperiod=12, slowperiod=26, signalperiod=9)
        historical_data['macd'] = macd
        historical_data['signal']= signal

        res = self.checkMacdCondition(historical_data['macd'],historical_data['signal'] )
        #print(f"\nhere {historical_data.tail(3)}")
        #t = historical_data.tail(1)
        if res != '':
            self.engine.say(self.getSymbol1())
            self.engine.runAndWait()
            print( "\n!!!:",self.symbol," ",self.timeframe, " ",  res ," \a ", datetime.datetime.fromtimestamp(float(historical_data['t'].iloc[-1])/1000)," ", historical_data['c'].iloc[-1], 
                    " macd:", "{:.2f}".format(historical_data['macd'].iloc[-1]), " signal:", "{:.2f}".format(historical_data['signal'].iloc[-1]) ) 
        self._historical_data = historical_data

        #calculate next timer based on binance server time, time frame, and the last row's close time
        server_time = self.client.get_server_time()['serverTime']
        ctime = time.time()
        #here get the second last, because the last is always not closed data.
        thelasttime = float(historical_data.index[-2].timestamp())
        ntime =int( thelasttime + 2 * self.toSeconds[self.timeframe] - ctime)
        if ntime > 0 :
            timer = threading.Timer( ntime, self.on_timer)
            timer.start()
        else:
            print(f"strange, the next time is <= 0, server_time: {server_time} ctime: {ctime} the last time: {thelasttime}")
# Subscribe to the WebSocket stream
    def start(self):
        historical_data = self.fetch_binance_futures_data( symbol=self.symbol, timeframe = self.timeframe, limit=500)
        historical_data['macd'] = None
        historical_data['signal'] = None
        #print(tt.to_string(index_format='%Y-%m-%d %H:%M:%S%z'))
        self._historical_data = historical_data
        print("start fetch data of ",self.symbol,' ', self._historical_data.tail(1))
        self.on_timer()
        
