import subprocess, threading, sys
from os import path

cwd = path.abspath(path.dirname(__file__))


def start_tweepy():
    subprocess.call([sys.executable, path.join(cwd, 'TweepyStreaming.py')])


def start_spark():
    subprocess.call(["spark-submit", path.join(cwd, 'SparkStreaming.py')])


def start_api():
    subprocess.call([sys.executable, path.join(cwd, 'webApi/run.py')])


# Creata a thread for each of the programs to run in parallel
tweepy = threading.Thread(target=start_tweepy)
spark = threading.Thread(target=start_spark)
api = threading.Thread(target=start_api)

tweepy.start()
spark.start()
api.start()
