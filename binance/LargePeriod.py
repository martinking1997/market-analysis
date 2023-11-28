from monitor.MonitorSymbolByPolling import MonitorSymbolByPolling
from monitor.Utility import Utility
import config

if __name__ == '__main__' :
        symbols = {"BTCUSDT","ETHUSDT","LINKUSDT","SOLUSDT","MATICUSDT","GASUSDT","MANAUSDT"}
        p1= Utility.getFirstSymbols(symbols)
        Utility.prepareSymbolFiles(p1)

        for symbol in symbols:
                link = MonitorSymbolByPolling(api_key= config.API_KEY, api_secret=config.API_SECRET,  symbol=symbol , timeframe='5m',
                proxies = config.PROXIES)
                link.start()
