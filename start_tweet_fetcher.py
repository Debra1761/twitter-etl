import subprocess
import os

print('starting tweet fetcher..')
subprocess.Popen(["python3.7", "fetch_tweets.py", "&"])