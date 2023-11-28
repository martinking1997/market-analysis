# market-analysis
This project records some auxiliary analysis tools for cryptocurrency transactions in development.

Currently not yet perfect, continuously updating

Currently, only Binance exchange data reading is supported.

Support two methods: polling (large time period, generally greater than 5m) and websocket (small time period, generally used for less than 5m).

Support proxy methods, including the commonly used socks5h method.

Male (multi) and female (short) voice prompts supporting currencies, as well as drumbeats indicating buy signals (positive) and bullish tones indicating sell signals (negative);

Support macd indicators, and additional indicators will be added as needed in the future.

#Requirements
* binance_connector==3.4.0
* numpy==1.21.5
* pandas==1.3.5
* playsound==1.3.0
* python_binance==1.0.19
* pyttsx3==2.90
* pytz==2022.1
* TA_Lib==0.4.28
* tzlocal==5.1
* websocket_client==1.6.4

Dependencies can be installed using the following command:

pip install -r requirements.txt
#Usage
Set some parameters in the config.py file.
If you use Proxy, set it to your configuration.
```shell
API_KEY = "your api key from binance"
API_SECRET = "your api secret from binance"
PROXIES = {
        'http': "socks5h://127.0.0.1:12345",
        'https': "socks5h://127.0.0.1:12345" }
```
If you don't use Proxy, just set :

```shell
PROXIES = { }
```
The LargePeriod.py file uses a polling method, where coin pairs and cycles can be set.

The SmallPeriod.py file uses websockets  method, where coin pairs and cycles can be set.

