import subprocess
import os
import time
import queue
import threading
import playsound
#
class Utility:
            
    # get first part of symbol , get btc from btcusdt, only process usdt
    @staticmethod
    def getFirstSymbol(symbol):
        symbol = symbol.lower()
        if symbol.endswith("usdt"):
            symbol = symbol[:-4]
        else:
            symbol = symbol
        return symbol

    @staticmethod
    def getFirstSymbols(symbols):
        res = []
        for symbol in symbols:
            res.append(__class__.getFirstSymbol(symbol))
        return list(set(res))

    #store the  same dir as this file
    @staticmethod
    def prepareSymbolFiles(symbols):
        for symbol in symbols:
            lc = symbol.lower()
            __class__.speakToFile(lc,gender='m')
            __class__.speakToFile(lc,gender='f')

    @staticmethod
    def speakToFile(symbol,gender='m'):
        fileName = os.path.join(os.path.dirname(__file__), symbol+"_"+gender+".mp3")
        if os.path.exists(fileName) :
            return "exist";
        else:
            print(fileName)
            espeak_command = ['espeak', '-v', f'en-us+{gender}2',  '-w', fileName, symbol]
            subprocess.run(espeak_command)
            return "generated"

# Use the `speak()` function to add speech tasks to the queue
    _instance = None  # Private class variable to hold the single instance

    def __new__(cls):
        # Implementing Singleton logic in __new__
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.mp3_queue = queue.Queue()  # Initialize the queue
            cls._instance.start_player_thread()  # Start the player thread
        return cls._instance

    @staticmethod
    def play_mp3(file_path):
        Utility()._instance.mp3_queue.put(file_path)  # Put file_path into the queue

    @staticmethod
    def play_mp3(file_path):
        Utility()._instance.mp3_queue.put(file_path)
    
    def mp3_player(self):
        while True:
            # Get the next mp3 task from the queue
            task = self.mp3_queue.get()
            if os.path.exists(task) :
                playsound.playsound(task)
            else:
                print("file not found:",task)
    
    def start_player_thread(self):
        worker_thread = threading.Thread(target=self.mp3_player)
        worker_thread.start()  # Start the player thread
    
