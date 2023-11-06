from monitor.MonitorSymbolByPolling import MonitorSymbolByPolling
import config

if __name__ == '__main__' :
        link =MonitorSymbolByPolling(api_key= config.API_KEY, api_secret=config.API_SECRET,  symbol='LINKUSDT' , timeframe='5m',
                proxy_type = 'socks5h', proxy_host = '127.0.0.1', proxy_port = 12345)
        link.start()

        sol =MonitorSymbolByPolling(api_key= config.API_KEY, api_secret=config.API_SECRET,  symbol='SOLUSDT' , timeframe='5m',
                proxy_type = 'socks5h', proxy_host = '127.0.0.1', proxy_port = 12345)
        sol.start()

        sol =MonitorSymbolByPolling(api_key= config.API_KEY, api_secret=config.API_SECRET,  symbol='BTCUSDT' , timeframe='5m',
                proxy_type = 'socks5h', proxy_host = '127.0.0.1', proxy_port = 12345)
        sol.start()

        sol =MonitorSymbolByPolling(api_key= config.API_KEY, api_secret=config.API_SECRET,  symbol='MANAUSDT' , timeframe='5m',
                proxy_type = 'socks5h', proxy_host = '127.0.0.1', proxy_port = 12345)
        sol.start()

        sol =MonitorSymbolByPolling(api_key= config.API_KEY, api_secret=config.API_SECRET,  symbol='MATICUSDT' , timeframe='5m',
                proxy_type = 'socks5h', proxy_host = '127.0.0.1', proxy_port = 12345)
        sol.start()

