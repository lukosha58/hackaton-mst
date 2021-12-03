import threading
import time

def rating():
    score = 100
    while (score != 0):
        score -= 2 
        time.sleep(5)
t = threading.Timer(120.0,rating)
t.start()
