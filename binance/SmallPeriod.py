from  monitor.MonitorSymbolWithWS import MonitorSymbolWithWS
import threading
import config
if __name__ == '__main__' :

        mlink =MonitorSymbolWithWS(api_key= config.API_KEY, api_secret=config.API_SECRET,  symbol='MATICUSDT' , timeframe='1m',
               proxy_type = 'socks5h', proxy_host = '127.0.0.1', proxy_port = 12345)
        mlink_thread = threading.Thread(target= mlink.start)
        mlink_thread.start()

        mm =MonitorSymbolWithWS(api_key= config.API_KEY, api_secret=config.API_SECRET,  symbol='SOLUSDT' , timeframe='1m',
                proxy_type = 'socks5h', proxy_host = '127.0.0.1', proxy_port = 12345)
        mMana_thread = threading.Thread(target= mm.start)
        mMana_thread.start()

