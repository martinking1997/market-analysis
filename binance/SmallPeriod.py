from  monitor.MonitorSymbolWithWS import MonitorSymbolWithWS
from monitor.Utility import Utility
import threading
import config
if __name__ == '__main__' :
        symbols = {"SOLUSDT", "LINKUSDT","GASUSDT","BTCUSDT","ETHUSDT"}
        p1= Utility.getFirstSymbols(symbols)
        Utility.prepareSymbolFiles(p1)

        for symbol in symbols :
                mlink =MonitorSymbolWithWS(api_key= config.API_KEY, api_secret=config.API_SECRET,  symbol=symbol , timeframe='1m',
                        proxies=config.PROXIES )
                mlink_thread = threading.Thread(target= mlink.start)
                mlink_thread.start()

